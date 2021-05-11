from brownie import accounts, chain, web3, chain
import brownie
import pytest


def test_stake_pool_v2(alice, lp_pool_v2, mock_lp_token, mock_mir_token):
    # shift the time to start the pool
    chain.sleep(10)

    # check stake
    stake_amount = 40
    mock_lp_token.mint(alice, stake_amount, {"from": alice})
    mock_lp_token.approve(lp_pool_v2.address, stake_amount, {"from": alice})
    lp_pool_v2.stake(stake_amount, {"from": alice})

    assert mock_lp_token.balanceOf(lp_pool_v2.address) == stake_amount, (
        f'incorrect balanceOf(lp_pool_v2); expect {stake_amount},'
        f'got {mock_lp_token.balanceOf(lp_pool_v2.address)}'
    )

    assert mock_lp_token.balanceOf(alice) == 0, (
        f'incorrect balanceOf(alice); expect {0},'
        f'got {mock_lp_token.balanceOf(alice)}'
    )


def test_get_rewards_after_second_stake(alice, lp_pool_v2, mock_lp_token, mock_mir_token, REWARDS):
    # shift the time to start the pool
    chain.sleep(10)
    lp_pool_v2.notifyReward({"from": alice})

    # setup
    stake_amount = 40
    second_stake_amount = 20
    mock_lp_token.mint(
        alice,
        stake_amount + second_stake_amount,
        {"from": alice}
    )
    mock_lp_token.approve(
        lp_pool_v2.address,
        stake_amount + second_stake_amount,
        {"from": alice}
    )
    mock_mir_token.mint(lp_pool_v2.address, 1000000000, {"from": alice})
    amount_alice_should_get = 0

    # stake first time
    prev_time = chain.time()
    lp_pool_v2.stake(stake_amount, {"from": alice})
    total_supply_now = stake_amount

    assert mock_lp_token.balanceOf(lp_pool_v2.address) == stake_amount, (
        f'incorrect balanceOf(lp_pool_v2); expect {stake_amount},'
        f'got {mock_lp_token.balanceOf(lp_pool_v2.address)}'
    )

    assert mock_lp_token.balanceOf(alice) == second_stake_amount, (
        f'incorrect balanceOf(alice); expect {second_stake_amount},'
        f'got {mock_lp_token.balanceOf(alice)}'
    )

    # stake second time
    chain.sleep(86400)
    latest_time = chain.time()
    lp_pool_v2.stake(second_stake_amount, {"from": alice})
    amount_alice_should_get += (latest_time - prev_time) * \
        REWARDS[0] * stake_amount // (365*86400) // total_supply_now
    total_supply_now += second_stake_amount

    assert mock_lp_token.balanceOf(lp_pool_v2.address) == total_supply_now, (
        f'incorrect balanceOf(lp_pool_v2); expect {total_supply_now},'
        f'got {mock_lp_token.balanceOf(lp_pool_v2.address)}'
    )
    assert mock_lp_token.balanceOf(alice) == 0, (
        f'incorrect balanceOf(alice); expect {0},'
        f'got {mock_lp_token.balanceOf(alice)}'
    )
    assert abs(mock_mir_token.balanceOf(alice) - amount_alice_should_get) <= amount_alice_should_get//1000, (
        f'incorrect reward; expect {amount_alice_should_get},'
        f'got {mock_lp_token.balanceOf(alice)}'
    )
