# Setup
Install `hevm` and `seth` by following the dapptools installation instructions outlined in https://github.com/dapphub/dapptools. Specifially, make sure you install Nix and then call:
```
nix-env -iA hevm -f $(curl -sS https://api.github.com/repos/dapphub/dapptools/releases/latest | jq -r .tarball_url)

nix-env -iA seth -f $(curl -sS https://api.github.com/repos/dapphub/dapptools/releases/latest | jq -r .tarball_url)
```

Export environment variables `ETH_RPC_URL` and `ETHERSCAN_API_KEY`. For example:
```
export ETH_RPC_URL=https://mainnet.infura.io/...
export ETHERSCAN_API_KEY=...
```

# Commands
The main point of entry for bytecode injection is `run.py`. The end-to-end workflow is as follows:


```
# Compile our independent assertion bytecode
solc --bin-runtime -o contracts/InjectedAssert contracts/InjectedAssert/InjectedAssert.sol  --overwrite

# Read bytecode of target contract
seth code 0xa4004b352fcbb913f0ddaba2454e7ff9cb64bdf6 > DeployedGetter.bin-runtime

# Run bytecode injection
python run.py --base_bin_fname DeployedGetter.bin-runtime --inject_bin_fname contracts/InjectedAssert/InjectedAssert.bin-runtime --output_bin_fname BytecodeInjecterOutput.bin-runtime

# Run symbolic execution on output bytecode
CONTRACT_ADDR=0xa4004b352fcbb913f0ddaba2454e7ff9cb64bdf6
hevm symbolic \
  --rpc $ETH_RPC_URL \
  --address $CONTRACT_ADDR \
  --sig "get()"\
  --get-models \
  --show-tree \
  --storage-model ConcreteS \
  --code $(cat BytecodeInjecterOutput.bin-runtime) \
  --block 10741412 \
```

You should get the following output
```
Assertion violation found.
Calldata:
0x6d4ce63c
get()
Caller:
0xEDd764AAa77C2148782cE5bcb8a3ADA80D932942
Callvalue:
0
├ 0           IsZero(IsZero(CallValue))
│             Revert
│             
└ 1           IsZero(IsZero(CallValue))
  ├ 0         IsZero(0xffffffffffffffffffffffffffffffffffffffff and CALLER == 0xffffffffffffffffffffffffffffffffffffffff and 0xffffffffffffffffffffffffffffffffffffffff and 0xedd764aaa77c2148782ce5bcb8a3ada80d932942 / 0x100 ** 0x0)
  │           Revert("no-getter")
  │           
  └ 1         IsZero(0xffffffffffffffffffffffffffffffffffffffff and CALLER == 0xffffffffffffffffffffffffffffffffffffffff and 0xffffffffffffffffffffffffffffffffffffffff and 0xedd764aaa77c2148782ce5bcb8a3ada80d932942 / 0x100 ** 0x0)
    ├ 0       IsZero(IsZero(0xffffffff and Timestamp + not 0xffffffff and 0x5f47674200000000000f2060b210d5af29ee0000000000000001012e41e74cc0 / 0x100000000000000000000000000000000000000000000000000000000 and 0xffffffff))
    │ └ 0     IsZero(IsZero(CallValue))
    │         Revert0x4e487b710000000000000000000000000000000000000000000000000000000000000001
    │         
    └ 1       IsZero(IsZero(0xffffffff and Timestamp + not 0xffffffff and 0x5f47674200000000000f2060b210d5af29ee0000000000000001012e41e74cc0 / 0x100000000000000000000000000000000000000000000000000000000 and 0xffffffff))
      └ 0     IsZero(IsZero(IsZero(IsZero(0xffffffff and Timestamp + not 0xffffffff and 0x5f47674200000000000f2060b210d5af29ee0000000000000001012e41e74cc0 / 0x100000000000000000000000000000000000000000000000000000000 and 0xffffffff))))
        └ 0   IsZero(IsZero(CallValue))
              Revert0x4e487b710000000000000000000000000000000000000000000000000000000000000001
```
which demonstrates that the symbolic executor has found the correct caller address to extract value with the `get()` call.

# Additional Details about hevm
In our example, we injected a custom assert to the `get()` call of a deployed Mainnet contract https://etherscan.io/address/0xa4004b352fcbb913f0ddaba2454e7ff9cb64bdf6.

1. First, test `hevm symbolic` on the deployed bytecode without any modifications.
```
hevm symbolic --rpc $ETH_RPC_URL --address 0xa4004b352fcbb913f0ddaba2454e7ff9cb64bdf6 --sig "get()" --get-models --show-tree --storage-model ConcreteS --block 10741412
```
You should get the following output:
```
$ hevm symbolic --rpc $ETH_RPC_URL --address 0xa4004b352fcbb913f0ddaba2454e7ff9cb64bdf6 --sig "get()" --get-models --show-tree --storage-model ConcreteS --block 10741412
checking postcondition...
Q.E.D.
Explored: 11 branches without assertion violations
├ 0         IsZero(IsZero(CallValue))
│           Revert
│           
└ 1         IsZero(IsZero(CallValue))
  ├ 0       IsZero(0xffffffffffffffffffffffffffffffffffffffff and CALLER == 0xffffffffffffffffffffffffffffffffffffffff and 0xffffffffffffffffffffffffffffffffffffffff and 0xedd764aaa77c2148782ce5bcb8a3ada80d932942 / 0x100 ** 0x0)
  │         Revert("no-getter")
  │         
  └ 1       IsZero(0xffffffffffffffffffffffffffffffffffffffff and CALLER == 0xffffffffffffffffffffffffffffffffffffffff and 0xffffffffffffffffffffffffffffffffffffffff and 0xedd764aaa77c2148782ce5bcb8a3ada80d932942 / 0x100 ** 0x0)
    ├ 0     IsZero(IsZero(0xffffffff and Timestamp + not 0xffffffff and 0x5f47674200000000000f2060b210d5af29ee0000000000000001012e41e74cc0 / 0x100000000000000000000000000000000000000000000000000000000 and 0xffffffff))
    │       Stop
    │       0x0 => 0x2cde6be34a59ff01aa532d56956a3c339c26322
    │       0x2 => 0xedd764aaa77c2148782ce5bcb8a3ada80d932942
    │       0x3 => 0x1e87e7073ec3021866553f0cdd73067a5aecc8e50
    │       
    └ 1     IsZero(IsZero(0xffffffff and Timestamp + not 0xffffffff and 0x5f47674200000000000f2060b210d5af29ee0000000000000001012e41e74cc0 / 0x100000000000000000000000000000000000000000000000000000000 and 0xffffffff))
      └ 0   IsZero(IsZero(IsZero(IsZero(0xffffffff and Timestamp + not 0xffffffff and 0x5f47674200000000000f2060b210d5af29ee0000000000000001012e41e74cc0 / 0x100000000000000000000000000000000000000000000000000000000 and 0xffffffff))))
            Stop
            0x0 => 0x2cde6be34a59ff01aa532d56956a3c339c26322
            0x2 => 0xedd764aaa77c2148782ce5bcb8a3ada80d932942
            0x3 => 0x1e87e7073ec3021866553f0cdd73067a5aecc8e50
            

-- Branch (1/11) --
....
```
2. To run `hevm` on a locally compiled contract, first compile the contract into bytecode.
```
solc --bin-runtime -o . Getter.sol  --overwrite
```






## Injecting custom asserts to 
1. Compile our custom `InjectedAssert
```
sh -v hevm_exec.sh
```
TODO: amychou
