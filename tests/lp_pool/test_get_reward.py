from brownie import accounts, chain, web3, chain
import brownie
import pytest


def test_get_reward_one_user(alice, bob, lp_pool, mock_lp_token, mock_mir_token, REWARDS):
    # shift the time to start the pool
    chain.sleep(10)
    lp_pool.notifyReward({"from": alice})

    # setup
    stake_amount_alice = 40
    mock_lp_token.mint(alice, stake_amount_alice, {"from": alice})
    mock_lp_token.approve(lp_pool.address, stake_amount_alice, {"from": alice})
    mock_mir_token.mint(lp_pool.address, 1000000000, {"from": alice})
    total_supply_now = stake_amount_alice

    # alice stake
    prev_time = chain.time()
    lp_pool.stake(stake_amount_alice, {"from": alice})
    assert mock_lp_token.balanceOf(lp_pool.address) == stake_amount_alice, (
        f'wrong setup: incorrect balanceOf(lp_pool); expect {stake_amount_alice},'
        f'got {mock_lp_token.balanceOf(lp_pool.address)}'
    )

    assert mock_lp_token.balanceOf(alice) == 0, (
        f'wrong setup: incorrect balanceOf(alice); expect {0},'
        f'got {mock_lp_token.balanceOf(alice)}'
    )

    # check getReward from alice request.
    chain.sleep(86400)
    latest_time = chain.time()
    lp_pool.getReward({"from": alice})

    assert mock_lp_token.balanceOf(lp_pool.address) == stake_amount_alice, (
        f'incorrect balanceOf(lp_pool); expect {stake_amount_alice},'
        f'got {mock_lp_token.balanceOf(lp_pool.address)}'
    )

    expect_rewards = (
        (latest_time - prev_time) * REWARDS[0] * stake_amount_alice) // (365*86400) // total_supply_now
    assert abs(mock_mir_token.balanceOf(alice) - expect_rewards) <= expect_rewards // 1000, (
        f'incorrect balanceOf(alice); expect {expect_rewards},'
        f'got {mock_mir_token.balanceOf(alice)}'
    )


def test_get_reward_multiple_actions(alice, bob, lp_pool, mock_lp_token, mock_mir_token, REWARDS):
    # shift the time to start the pool
    chain.sleep(10)
    lp_pool.notifyReward({"from": alice})

    # setup
    stake_amount_alice = 40
    mock_lp_token.mint(alice, stake_amount_alice, {"from": alice})
    mock_lp_token.approve(lp_pool.address, stake_amount_alice, {"from": alice})
    stake_amount_bob = 60
    mock_lp_token.mint(bob, stake_amount_bob, {"from": bob})
    mock_lp_token.approve(lp_pool.address, stake_amount_bob, {"from": bob})
    mock_mir_token.mint(lp_pool.address, 10000000000, {"from": alice})
    amount_alice_should_get = 0

    # alice stakes
    prev_time = chain.time()
    lp_pool.stake(stake_amount_alice, {"from": alice})
    total_supply_now = stake_amount_alice

    assert mock_lp_token.balanceOf(lp_pool.address) == stake_amount_alice, (
        f'wrong setup: incorrect balanceOf(lp_pool); expect {stake_amount_alice},'
        f'got {mock_lp_token.balanceOf(lp_pool.address)}'
    )
    assert mock_lp_token.balanceOf(alice) == 0, (
        f'wrong setup: incorrect balanceOf(alice); expect {0},'
        f'got {mock_lp_token.balanceOf(alice)}'
    )

    # bob stakes
    chain.sleep(86400)
    latest_time = chain.time()
    amount_alice_should_get += (latest_time - prev_time) * \
        REWARDS[0] * stake_amount_alice // (365*86400) // total_supply_now
    prev_time = latest_time

    lp_pool.stake(stake_amount_bob, {"from": bob})
    total_supply_now += stake_amount_bob

    assert mock_lp_token.balanceOf(lp_pool.address) == stake_amount_alice + stake_amount_bob, (
        f'wrong setup: incorrect balanceOf(lp_pool); expect {stake_amount_alice + stake_amount_bob},'
        f'got {mock_lp_token.balanceOf(lp_pool.address)}'
    )

    assert mock_lp_token.balanceOf(bob) == 0, (
        f'wrong setup: incorrect balanceOf(bob); expect {0},'
        f'got {mock_lp_token.balanceOf(bob)}'
    )

    # check getReward from alice request.
    chain.sleep(86400)
    latest_time = chain.time()
    lp_pool.getReward({"from": alice})

    assert mock_lp_token.balanceOf(lp_pool.address) == total_supply_now, (
        f'incorrect balanceOf(lp_pool); expect {total_supply_now},'
        f'got {mock_lp_token.balanceOf(lp_pool.address)}'
    )

    amount_alice_should_get += (
        (latest_time - prev_time) * REWARDS[0] * stake_amount_alice) // (365*86400) // total_supply_now
    assert abs(mock_mir_token.balanceOf(alice) - amount_alice_should_get) <= amount_alice_should_get // 1000, (
        f'incorrect balanceOf(alice); expect {amount_alice_should_get},'
        f'got {mock_mir_token.balanceOf(alice)}'
    )
