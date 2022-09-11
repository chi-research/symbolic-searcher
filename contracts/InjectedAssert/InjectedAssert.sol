// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.17;

interface IERC20 {
    function balanceOf(address owner) external view returns (uint);
}

contract InjectedAssert {
     function get() public {
        assert(IERC20(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2).balanceOf(0xe87e7073eC3021866553F0CdD73067A5AECc8e50) <= 0);
    }
}
