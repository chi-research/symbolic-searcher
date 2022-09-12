import argparse
import re
import logging

STOP_CODE = "00"
JUMPDEST_CODE = "5b"
PUSH2_CODE = "61"
REVERT_CODE = "fd"


class BytecodeInjecter:
    def __init__(self, base_bin, inject_bin):
        self.base_bin = self.process_bin_str(base_bin)
        self.inject_bin = self.process_bin_str(inject_bin)

        invalid_i = self.inject_bin.find(REVERT_CODE + "fe")
        if invalid_i != -1: 
            self.inject_bin = self.inject_bin[:invalid_i+2]

        # Split bin into two-character bytes
        self.base_bytes = [
            self.base_bin[i:i+2] for i in range(0, len(self.base_bin), 2)
        ]
        self.inject_bytes = [
            self.inject_bin[i:i+2] for i in range(0, len(self.inject_bin), 2)
        ]

        self.L = len(self.base_bytes)
        self.K = len(self.inject_bytes)
        self.debug_print()
        
        self.stop_sections = self.get_stop_sections_in_base_bytes()[:2]
        print("stop_sections", self.stop_sections)
        self.valid_jumpdests = self.get_valid_jumpdests_in_inject_bytes()
        print("valid jumpdests", self.valid_jumpdests)

    def process_bin_str(self, bin_str):
        bin_str = bin_str.strip()
        if bin_str[:2] == "0x":
            bin_str = bin_str[2:]

        # Truncate 32-byte metadata hash
        # bin_str = bin_str[:-64]

        # Search for "REVERT INVALID" opcodes and truncate
        """
        invalid_i = bin_str.find(REVERT_CODE + "fe")
        if invalid_i != -1: 
            bin_str = bin_str[:invalid_i+2]
        """

        return bin_str

    def get_stop_sections_in_base_bytes(self):
        """
        Returns list of indices (i, j) corresponding to sections of
        (JUMPDEST ... STOP) in base_bytes

        Returns: List[Tuple[Int, Int]]
        """
        stop_sections = []
        last_jumpdest = -1
        last_pushx = -1
        last_x = -1
        i = 0
        while i < self.L:
            opcode = self.base_bytes[i]
            if opcode == JUMPDEST_CODE:
                last_jumpdest = i
            elif opcode[0] == '6' or opcode[0] == '7':
                # Corresponds to JUMPX instruction, so jump forward
                opcode_val = int("0x" + opcode, 16) # Eval in base 10
                last_pushx = i
                last_x = opcode_val - 0x60 + 1
                i += last_x
            elif (
                opcode == STOP_CODE
                and last_jumpdest != -1
                and (i == self.L-1 or self.base_bytes[i+1] != STOP_CODE)
                and (self.base_bytes[i-1] != STOP_CODE)
            ):
                stop_sections.append((last_jumpdest, i))
            i += 1

        return stop_sections

    def get_valid_jumpdests_in_inject_bytes(self):
        """
        Returns list of tuples (i, occurrences = [j1, j2...]) for all indices
        i where there is a JUMPDEST at index i of inject_bytes and all
        occurrences of string "PUSH2 <JUMPDEST_LOC>" in inject_bin

        Returns: List[Tuple[Int, List]]
        """
        valid_jumpdests = []
        for i in range(self.K):
            if self.inject_bytes[i] == JUMPDEST_CODE: #0x5b
                # Get the current location in hex
                jumpdest_loc = self.format_hex_loc(i)
                push_jumpdest_instr = PUSH2_CODE + jumpdest_loc # PUSH2 <JUMPDEST_LOC>

                # ========= DEBUG =========
                print("Found jumpdest at loc", i, "=", jumpdest_loc)
                # ========= DEBUG =========
                
                occurrences = [
                    m.start() for m in re.finditer(push_jumpdest_instr, self.inject_bin)
                ]
                if len(occurrences) > 0:
                    valid_jumpdests.append((i, occurrences))
                else:
                    # ========= DEBUG =========
                    print("Did not find valid push instruction for", i)
                    # ========= DEBUG =========

        return valid_jumpdests

    def build_mod_bin(self):
        concat_bin = self.base_bin[:]

        curr_inject_offset = self.L
        inject_offsets = []

        # Append inject_bin once for each (JUMPDEST...STOP) section of base_bin
        for i in range(len(self.stop_sections)):
            inject_offsets.append(curr_inject_offset)
            a, b = self.stop_sections[i]
            
            # Get modified inject_bin where each jump location is offset
            # by the current inject_offset
            mod_inject_bin = self.replace_jumplocs_with_offsets(
                self.inject_bin, self.valid_jumpdests, curr_inject_offset + b-a
            )
            snippet = self.base_bin[2*a:2*b]
            print("Append snippet ", snippet)
            injection = self.base_bin[2*a:2*b] + mod_inject_bin
            print("Injection ", injection)

            concat_bin += injection
            curr_inject_offset = len(concat_bin) // 2

        # Modify base_bin to jump to inject_offsets
        mod_base_bin = self.base_bin[:]
        for i in range(len(self.stop_sections)):
            a, b = self.stop_sections[i] # (JUMPDEST_ind, STOP_ind)
            mod_base_bin = self.replace_hex_index(mod_base_bin, a, inject_offsets[i])

        return mod_base_bin + concat_bin[2 * self.L:]

    def replace_hex_index(self, bytestring, find_index, replace_index):
        """
        Modify a hex bytestring to replace 2-byte hex find_index with
        2-byte hex replace_index

        Returns: str
        """
        find_hex = self.format_hex_loc(find_index)
        replace_hex = self.format_hex_loc(replace_index)
        print("replace_hex_index", find_hex, ">>", replace_hex)
        return bytestring.replace(find_hex, replace_hex)

    def replace_jumplocs_with_offsets(self, bytestring, valid_jumpdests, offset_value): 
        """
        Return a modified bytestring where valid jump locations are offset

        Returns: str
        """
        mod_bytestring = bytestring[:]
        for _, jump_occurrences in valid_jumpdests:
            print("Replacing", jump_occurrences)
            for j in jump_occurrences:
                original_loc_hex = bytestring[j+2:j+6]
                original_loc = int(original_loc_hex, 16)
                new_loc = original_loc + offset_value
                new_loc_hex = self.format_hex_loc(new_loc)

                ########## DEBUG ##########
                print("Replacing index", j+2, ": ", original_loc_hex, ">>", new_loc_hex)
                ########## DEBUG ##########
                print(mod_bytestring[j+2:j+6])
                mod_bytestring = (
                    mod_bytestring[:j+2] +
                    new_loc_hex +
                    mod_bytestring[j+6:]
                )   
                print(mod_bytestring[j+2:j+6])

        return mod_bytestring 

    def format_hex_loc(self, index):
        """
        Returns index formatted as 2-byte hex string location, e.g. "05ac"

        Returns: 4-character str
        """
        return "{0:#0{1}x}".format(index,6)[2:]

    def debug_print(self):
        print("========== DEBUG ==========")
        print("Base bin = ", self.base_bin)
        print("Inject bin = ", self.inject_bin)
        print("L = ", self.L)
        print("K = ", self.K)

parser = argparse.ArgumentParser()
parser.add_argument(
    '--base_bin_fname',
    dest='base_bin_fname',
    help="Input filename containing original bin-runtime bytecode",
    # default="DeployedGetter.bin-runtime"
    default="contracts/DarkForestGetter/Getter.bin-runtime"
)
parser.add_argument(
    '--inject_bin_fname',
    dest='inject_bin_fname',
    help="Input filename containing to-be-injected bin-runtime bytecode",
    default="contracts/InjectedAssert/InjectedAssert.bin-runtime"
)
parser.add_argument(
    '--output_bin_fname',
    dest='output_bin_fname',
    help="Input filename for output bin-runtime bytecode",
    default="BytecodeInjecterOutput.bin-runtime"
)

args = parser.parse_args()

f = open(args.base_bin_fname)
base_bin_str = f.read()
f.close()

f = open(args.inject_bin_fname)
inject_bin_str = f.read()
f.close()

injecter = BytecodeInjecter(base_bin_str, inject_bin_str)
f = open(args.output_bin_fname, "w")
mod_bin_str = injecter.build_mod_bin()
f.write(mod_bin_str)
f.close()
