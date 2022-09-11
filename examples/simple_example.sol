// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.4.24;
contract Simple {
    function f(uint a) payable public {
        assert (a != 65);
    }
}
