// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.3;

import 'OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/token/ERC20/ERC20.sol';

contract MockERC20 is ERC20 {
  constructor(string memory name, string memory symbol) ERC20(name, symbol) {}

  function mint(address to, uint amount) public {
    _mint(to, amount);
  }
}
