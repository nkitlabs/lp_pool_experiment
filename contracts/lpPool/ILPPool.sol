// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.3;

import "OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/token/ERC20/IERC20.sol";

interface ILPPool {
    //================== Callers ==================//
    function mir() external view returns (IERC20);

    function startTime() external view returns (uint256);

    function totalReward() external view returns (uint256);

    function earned(address account) external view returns (uint256);

    //================== Transactors ==================//

    function stake(uint256 amount) external;

    function withdraw(uint256 amount) external;

    function exit() external;

    function getReward() external;
}