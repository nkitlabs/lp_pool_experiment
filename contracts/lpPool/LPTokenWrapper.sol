// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.3;

import 'OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/utils/Math/SafeMath.sol';
import 'OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/token/ERC20/utils/SafeERC20.sol';

contract LPTokenWrapper {
  using SafeMath for uint;
  using SafeERC20 for IERC20;

  IERC20 public lpt;

  uint private _totalSupply;
  mapping(address => uint) private _balances;

  function totalSupply() public view returns (uint) {
    return _totalSupply;
  }

  function balanceOf(address account) public view returns (uint) {
    return _balances[account];
  }

  function stake(uint amount) public virtual {
    _totalSupply = _totalSupply.add(amount);
    _balances[msg.sender] = _balances[msg.sender].add(amount);
    lpt.safeTransferFrom(msg.sender, address(this), amount);
  }

  function withdraw(uint amount) public virtual {
    _totalSupply = _totalSupply.sub(amount);
    _balances[msg.sender] = _balances[msg.sender].sub(amount);
    lpt.safeTransfer(msg.sender, amount);
  }
}
