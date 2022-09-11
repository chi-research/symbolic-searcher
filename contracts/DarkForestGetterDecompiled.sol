contract GetterDecompiled {
    function main() {
        memory[0x40:0x60] = 0x80;
        var var0 = msg.value;

        if (var0) { revert(memory[0x00:0x00]); }

        if (msg.data.length < 0x04) { revert(memory[0x00:0x00]); }

        var0 = msg.data[0x00:0x20] >> 0xe0;

        if (var0 == 0x5f76f6ab) {
            // Dispatch table entry for set(bool)
            var var1 = 0x0069;
            var var2 = 0x04;
            var var3 = msg.data.length - var2;

            if (var3 < 0x20) { revert(memory[0x00:0x00]); }

            set(var2, var3);
            stop();
        } else if (var0 == 0x6d4ce63c) {
            // Dispatch table entry for get()
            var1 = 0x0073;
            get();
            stop();
        } else { revert(memory[0x00:0x00]); }
    }

    function set(var arg0, var arg1) {
        arg0 = !!msg.data[arg0:arg0 + 0x20];

        if (msg.sender == storage[0x01] & 0xffffffffffffffffffffffffffffffffffffffff) {
            storage[0x03] = !!arg0 * 0x0100 ** 0x14 | (storage[0x03] & ~(0xff * 0x0100 ** 0x14));
            return;
        } else {
            var temp0 = memory[0x40:0x60];
            memory[temp0:temp0 + 0x20] = 0x08c379a000000000000000000000000000000000000000000000000000000000;
            var temp1 = temp0 + 0x04;
            var temp2 = temp1 + 0x20;
            memory[temp1:temp1 + 0x20] = temp2 - temp1;
            memory[temp2:temp2 + 0x20] = 0x09;
            var temp3 = temp2 + 0x20;
            memory[temp3:temp3 + 0x20] = 0x6e6f2d7365747465720000000000000000000000000000000000000000000000;
            var temp4 = memory[0x40:0x60];
            revert(memory[temp4:temp4 + (temp3 + 0x20) - temp4]);
        }
    }

    function get() {
        if (msg.sender != storage[0x02] & 0xffffffffffffffffffffffffffffffffffffffff) {
            var temp9 = memory[0x40:0x60];
            memory[temp9:temp9 + 0x20] = 0x08c379a000000000000000000000000000000000000000000000000000000000;
            var temp10 = temp9 + 0x04;
            var temp11 = temp10 + 0x20;
            memory[temp10:temp10 + 0x20] = temp11 - temp10;
            memory[temp11:temp11 + 0x20] = 0x09;
            var temp12 = temp11 + 0x20;
            memory[temp12:temp12 + 0x20] = 0x6e6f2d6765747465720000000000000000000000000000000000000000000000;
            var temp13 = memory[0x40:0x60];
            revert(memory[temp13:temp13 + (temp12 + 0x20) - temp13]);
        } else if (!!(storage[0x03] / 0x0100 ** 0x14 & 0xff) == !!0x01) {
            var var0 = storage[0x00] & 0xffffffffffffffffffffffffffffffffffffffff;
            var var1 = 0x89afcb44;
            var temp0 = memory[0x40:0x60];
            memory[temp0:temp0 + 0x20] = (var1 & 0xffffffff) << 0xe0;
            var temp1 = temp0 + 0x04;
            memory[temp1:temp1 + 0x20] = storage[0x03] & 0xffffffffffffffffffffffffffffffffffffffff;
            var var2 = temp1 + 0x20;
            var var3 = 0x40;
            var var4 = memory[var3:var3 + 0x20];
            var var5 = var2 - var4;
            var var6 = var4;
            var var7 = 0x00;
            var var8 = var0;
            var var9 = !address(var8).code.length;

            if (var9) { revert(memory[0x00:0x00]); }

            var temp2;
            temp2, memory[var4:var4 + var3] = address(var8).call.gas(msg.gas).value(var7)(memory[var6:var6 + var5]);
            var3 = !temp2;

            if (!var3) {
                var0 = memory[0x40:0x60];
                var1 = returndata.length;

                if (var1 >= 0x40) { return; }
                else { revert(memory[0x00:0x00]); }
            } else {
                var temp3 = returndata.length;
                memory[0x00:0x00 + temp3] = returndata[0x00:0x00 + temp3];
                revert(memory[0x00:0x00 + returndata.length]);
            }
        } else {
            var temp4 = memory[0x40:0x60];
            memory[temp4:temp4 + 0x20] = 0x08c379a000000000000000000000000000000000000000000000000000000000;
            var temp5 = temp4 + 0x04;
            var temp6 = temp5 + 0x20;
            memory[temp5:temp5 + 0x20] = temp6 - temp5;
            memory[temp6:temp6 + 0x20] = 0x08;
            var temp7 = temp6 + 0x20;
            memory[temp7:temp7 + 0x20] = 0x6e6f2d627265616b000000000000000000000000000000000000000000000000;
            var temp8 = memory[0x40:0x60];
            revert(memory[temp8:temp8 + (temp7 + 0x20) - temp8]);
        }
    }
}