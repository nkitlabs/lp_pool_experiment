from brownie import accounts, chain, web3, chain
import brownie
import pytest


def test_withdraw(alice, lp_pool, mock_lp_token, mock_mir_token):
    # shift the time to start the pool
    chain.sleep(10)

    # setup
    stake_amount = 40
    mock_lp_token.mint(alice, stake_amount, {"from": alice})
    mock_lp_token.approve(lp_pool.address, stake_amount, {"from": alice})
    mock_mir_token.mint(lp_pool.address, 1000000000, {"from": alice})

    # alice stakes
    lp_pool.stake(stake_amount, {"from": alice})

    assert mock_lp_token.balanceOf(lp_pool.address) == stake_amount, (
        f'wrong setup: incorrect balanceOf(lp_pool); expect {stake_amount},'
        f'got {mock_lp_token.balanceOf(lp_pool.address)}'
    )

    assert mock_lp_token.balanceOf(alice) == 0, (
        f'wrong setup: incorrect balanceOf(alice); expect {0},'
        f'got {mock_lp_token.balanceOf(alice)}'
    )

    # check withdraw
    chain.sleep(1)
    withdraw_amount = 20
    lp_pool.withdraw(withdraw_amount, {"from": alice})

    assert mock_lp_token.balanceOf(lp_pool.address) == stake_amount - withdraw_amount, (
        f'incorrect balanceOf(lp_pool); expect {stake_amount - withdraw_amount},'
        f'got {mock_lp_token.balanceOf(lp_pool.address)}'
    )

    assert mock_lp_token.balanceOf(alice) == withdraw_amount, (
        f'incorrect balanceOf(alice); expect {withdraw_amount},'
        f'got {mock_lp_token.balanceOf(alice)}'
    )
