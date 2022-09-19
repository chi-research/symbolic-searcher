// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.17;

contract InjectedAssertETH {
     function get() public {
        assert(address(0xE462Eae2AEF5deFbcDdc43995b7f593e6F0ae22F).balance <= 574999214123497918071);
    }
}
