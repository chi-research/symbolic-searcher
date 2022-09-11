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
2. To run `hevm` on a locally compiled contract, you must first compile the contract into bytecode
```
solc --bin-runtime -o . Getter.sol  --overwrite
```






## Injecting custom asserts to 
1. Compile our custom `InjectedAssert
```
sh -v hevm_exec.sh
```
TODO: amychou
