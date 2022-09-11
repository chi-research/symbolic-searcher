// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.17;

interface IWETH {
    function balanceOf(address owner) external view returns (uint);
}

contract Test {
     function get() public {
        assert(IWETH(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2).balanceOf(0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045) <= 0);
    }
}