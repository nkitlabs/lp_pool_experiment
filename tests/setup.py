from brownie import accounts, chain, web3, LPPool, LPPoolV2, MockERC20, chain
import brownie
import pytest


@pytest.fixture
def REWARDS():
    return [10 * 365 * 86400, 5 * 365 * 86400, 365 * 86400]


@pytest.fixture(scope="function")
def alice():
    return accounts[0]


@pytest.fixture(scope="function")
def bob():
    return accounts[1]


@pytest.fixture
def mock_lp_token(alice):
    contract = alice.deploy(MockERC20, "LP Test", "LPT")
    return contract


@pytest.fixture
def mock_mir_token(alice):
    contract = alice.deploy(MockERC20, "MIR Test", "MIRT")
    return contract


@pytest.fixture
def lp_pool(alice, mock_lp_token, mock_mir_token, REWARDS):
    contract = alice.deploy(LPPool, mock_mir_token.address,
                            mock_lp_token.address, chain.time()+5, REWARDS)
    contract.setRewardDistribution(alice, {"from": alice})
    return contract


@pytest.fixture
def lp_pool_v2(alice, mock_lp_token, mock_mir_token, REWARDS):
    contract = alice.deploy(LPPoolV2, mock_mir_token.address,
                            mock_lp_token.address, chain.time()+5, REWARDS)
    contract.setRewardDistribution(alice, {"from": alice})
    return contract
