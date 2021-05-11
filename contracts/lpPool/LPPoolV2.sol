// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.3;

import './ILPPool.sol';
import './LPTokenWrapper.sol';
import './IRewardDistributionRecipient.sol';
import 'OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/utils/math/Math.sol';

contract LPPoolV2 is ILPPool, LPTokenWrapper, IRewardDistributionRecipient {
  using SafeMath for uint;
  using SafeERC20 for IERC20;

  uint public constant DURATION = 365 days;

  // Immutable
  IERC20 public immutable override mir;
  uint public immutable override startTime;
  uint public immutable override totalReward;

  // Time
  uint public periodFinish;
  uint public lastUpdateTime;

  // Reward
  uint[] public rewards;
  uint public rewardRate;
  uint public rewardPerTokenStored;

  // Deflation
  uint public deflationCount = 0;

  mapping(address => uint) public userRewardPerTokenPaid;

  // Events
  event RewardNotified(uint reward);
  event RewardUpdated(uint reward);
  event Staked(address indexed user, uint amount);
  event Withdrawn(address indexed user, uint amount);
  event RewardPaid(address indexed user, uint reward);

  constructor(
    address _mir,
    address _lpt,
    uint _startTime,
    uint[] memory _rewards,
    uint _totalReward
  ) {
    require(_rewards.length > 0, 'LPPool: initReward should be greater than zero');
    require(
      _startTime > block.timestamp,
      'LPPool: startTime should be greater than current timestamp'
    );

    mir = IERC20(_mir);
    lpt = IERC20(_lpt);
    startTime = _startTime;
    rewards = _rewards;
    totalReward = _totalReward;
  }

  //================== Modifier ==================//

  modifier updateReward(address account) {
    rewardPerTokenStored = rewardPerToken();
    lastUpdateTime = lastTimeRewardApplicable();
    if (account != address(0)) {
      uint reward = earned(account);
      if (reward > 0) {
        mir.safeTransfer(account, reward);
        emit RewardPaid(account, reward);
      }
      userRewardPerTokenPaid[account] = rewardPerTokenStored;
    }
    _;
  }

  modifier checkHalve() {
    if (block.timestamp >= periodFinish && deflationCount < rewards.length.sub(1)) {
      deflationCount = deflationCount.add(1);
      rewardRate = currentReward().div(DURATION);
      periodFinish = block.timestamp.add(DURATION);
      emit RewardUpdated(currentReward());
    }
    _;
  }

  modifier checkStart() {
    require(block.timestamp >= startTime, 'not start');
    _;
  }

  //================== Callers ==================//

  function currentReward() public view returns (uint) {
    return rewards[deflationCount];
  }

  function lastTimeRewardApplicable() public view returns (uint) {
    return Math.min(block.timestamp, periodFinish);
  }

  function rewardPerToken() public view returns (uint) {
    if (totalSupply() == 0) {
      return rewardPerTokenStored;
    }
    return
      rewardPerTokenStored.add(
        lastTimeRewardApplicable().sub(lastUpdateTime).mul(rewardRate).mul(1e18).div(totalSupply())
      );
  }

  function earned(address account) public view override returns (uint) {
    return balanceOf(account).mul(rewardPerToken().sub(userRewardPerTokenPaid[account])).div(1e18);
  }

  //================== Transactors ==================//

  // stake visibility is public as overriding LPTokenWrapper's stake() function
  function stake(uint amount)
    public
    override(ILPPool, LPTokenWrapper)
    updateReward(msg.sender)
    checkHalve
    checkStart
  {
    require(amount > 0, 'Cannot stake 0');
    super.stake(amount);
    emit Staked(msg.sender, amount);
  }

  function withdraw(uint amount)
    public
    override(ILPPool, LPTokenWrapper)
    updateReward(msg.sender)
    checkHalve
    checkStart
  {
    require(amount > 0, 'Cannot withdraw 0');
    super.withdraw(amount);
    emit Withdrawn(msg.sender, amount);
  }

  function exit() external override {
    withdraw(balanceOf(msg.sender));
    getReward();
  }

  function getReward() public override updateReward(msg.sender) checkHalve checkStart {}

  function safeTransferMIRToken(address account, uint reward) internal virtual {
    mir.safeTransfer(account, reward);
    emit RewardPaid(account, reward);
  }

  function notifyReward() external override onlyRewardDistribution updateReward(address(0)) {
    rewardRate = currentReward().div(DURATION);
    lastUpdateTime = startTime;
    periodFinish = startTime.add(DURATION);
    emit RewardNotified(currentReward());
  }
}
