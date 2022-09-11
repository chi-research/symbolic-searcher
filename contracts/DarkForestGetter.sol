// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.17;

interface IGetter {
  function set(bool) external;
}

interface IPool {
  function burn(address to) external returns (uint amount0, uint amount1);
}

contract Getter is IGetter {
  IPool private pool;
  address private setter;
  address private getter;
  address private dest;
  bool private on;

  constructor(address pool_, address setter_, address getter_, address dest_) public {
    pool = IPool(pool_);
    setter = setter_;
    getter = getter_;
    dest = dest_;
  }

  function set(bool on_) public override {
    require(msg.sender == setter, "no-setter");
    on = on_;
  }

  function get() public {
    require(msg.sender == getter, "no-getter");
    require(on == true, "no-break");
    pool.burn(dest);
  }
}