// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.3;

import 'OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/access/Ownable.sol';

abstract contract IRewardDistributionRecipient is Ownable {
  address public rewardDistribution;

  function notifyReward() external virtual;

  modifier onlyRewardDistribution() {
    require(_msgSender() == rewardDistribution, 'Caller is not reward distribution');
    _;
  }

  function setRewardDistribution(address _rewardDistribution) external virtual onlyOwner {
    rewardDistribution = _rewardDistribution;
  }
}
