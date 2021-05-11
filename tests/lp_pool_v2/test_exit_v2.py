from brownie import accounts, chain, web3, chain
import brownie
import pytest


def test_exit_pool_v2(alice, bob, lp_pool_v2, mock_lp_token, mock_mir_token, REWARDS):
    # shift the time to start the pool
    chain.sleep(10)
    lp_pool_v2.notifyReward({"from": alice})

    # setup
    stake_amount_alice = 40
    mock_lp_token.mint(alice, stake_amount_alice, {"from": alice})
    mock_lp_token.approve(lp_pool_v2.address,
                          stake_amount_alice, {"from": alice})
    mock_mir_token.mint(lp_pool_v2.address, 1000000000, {"from": alice})
    total_supply_now = stake_amount_alice

    # alice stake
    prev_time = chain.time()
    lp_pool_v2.stake(stake_amount_alice, {"from": alice})
    assert mock_lp_token.balanceOf(lp_pool_v2.address) == stake_amount_alice, (
        f'wrong setup: incorrect balanceOf(lp_pool_v2); expect {stake_amount_alice},'
        f'got {mock_lp_token.balanceOf(lp_pool_v2.address)}'
    )

    assert mock_lp_token.balanceOf(alice) == 0, (
        f'wrong setup: incorrect balanceOf(alice); expect {0},'
        f'got {mock_lp_token.balanceOf(alice)}'
    )

    # check getReward from alice request.
    chain.sleep(86400)
    latest_time = chain.time()
    lp_pool_v2.exit({"from": alice})

    assert mock_lp_token.balanceOf(lp_pool_v2.address) == 0, (
        f'incorrect balanceOf(lp_pool_v2); expect {0},'
        f'got {mock_lp_token.balanceOf(lp_pool_v2.address)}'
    )

    assert mock_lp_token.balanceOf(alice) == stake_amount_alice, (
        f'incorrect balanceOf(lp_pool_v2); expect {stake_amount_alice},'
        f'got {mock_lp_token.balanceOf(alice)}'
    )

    expect_rewards = (
        (latest_time - prev_time) * REWARDS[0] * stake_amount_alice) // (365*86400) // total_supply_now
    assert abs(mock_mir_token.balanceOf(alice) - expect_rewards) <= expect_rewards//10000, (
        f'incorrect reward result; expect {expect_rewards},'
        f'got {mock_mir_token.balanceOf(alice)}'
    )
