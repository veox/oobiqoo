#

import pytest
from ethereum.tester import TransactionFailed

import time

# =============================================================================
# HELPERS

def deploy(chain, owner=None):
    if owner is None:
        owner = chain.web3.eth.coinbase

    oo, txhash = chain.provider.deploy_contract('oo', deploy_transaction={'from': owner})
    txreceipt = chain.wait.for_receipt(txhash)

    # FIXME: should be done in one go with deploying!
    txhash = oo.transact().init()
    txreceipt = chain.wait.for_receipt(txhash)

    assert oo.address != 0
    assert oo.address != owner

    return oo

def wait_n_blocks(chain, nblocks=1):
    '''Rattle the chain.'''
    waituntil = chain.web3.eth.getBlock('latest')['number'] + nblocks
    chain.wait.for_block(block_number=waituntil)
    return

# =============================================================================
# TESTS

def test_deployment(chain):
    oo = deploy(chain, owner=chain.web3.eth.coinbase)
    return

# =============================================================================
# TESTS: read-only

def test_f_get_owner(chain):
    oo = deploy(chain)
    assert oo.call().owner() == chain.web3.eth.coinbase
    return

def test_f_get_name(chain):
    oo = deploy(chain)
    assert oo.call().name() == 'oo'
    return

def test_f_get_symbol(chain):
    oo = deploy(chain)
    assert oo.call().symbol() == ('oo.' + str.lower(chain.web3.eth.coinbase[2:]))
    return

def test_f_get_decimals(chain):
    oo = deploy(chain)
    assert oo.call().decimals() == 0
    return

def test_f_get_total_supply(chain):
    oo = deploy(chain)
    assert oo.call().totalSupply() == 0
    return

def test_f_get_default_approval_duration(chain):
    oo = deploy(chain)
    assert oo.call().get_default_approval_duration() == 60*60*24*7
    return

def test_f_get_balance(chain):
    oo = deploy(chain)
    assert oo.call().balanceOf(chain.web3.eth.coinbase) == 0
    return

def test_f_get_mintable(chain):
    oo = deploy(chain)

    # mintable a bit after deployment (likely 1 block later)
    mintable1 = oo.call().get_mintable()

    wait_n_blocks(chain, 10)

    # mintable on block2
    mintable2 = oo.call().get_mintable()

    assert mintable2 > mintable1
    assert mintable2 <= 15 * waitnblocks

    return

# =============================================================================
# TESTS: read/write

@pytest.mark.incremental
class TestMinting(object):
    '''mint()'''
    def test_f_mint_owner(self, chain):
        oo = deploy(chain)

        owner = chain.web3.eth.coinbase

        # make sure there'll be something to mint
        wait_n_blocks(chain, 10)
        balance1 = oo.call().balanceOf(owner)
        mintable1 = oo.call().get_mintable()

        # after some time - still no balance, can mint
        assert balance1 == 0
        assert mintable1 > 0

        txhash = oo.transact({'from': owner}).mint()
        txreceipt = chain.wait.for_receipt(txhash)
        balance2 = oo.call().balanceOf(owner)
        mintable2 = oo.call().get_mintable()

        # got balance, there's less left to mint
        assert balance2 > 0
        assert mintable1 > mintable2 > 0

        # TODO: check event data

        return

    def test_f_mint_non_owner(self, chain):
        oo = deploy(chain)
        mallory = chain.web3.eth.accounts[1]

        # has no balance before minting
        assert oo.call().balanceOf(mallory) == 0

        # transaction gets reverted
        with pytest.raises(TransactionFailed):
            oo.transact({'from': mallory}).mint()

        # has no balance after mint() attempt
        assert oo.call().balanceOf(mallory) == 0

        # TODO: check no event emitted

        return

@pytest.mark.incremental
class TestBurning(object):
    '''burn()'''
    def test_f_burn_with_sufficient_balance(self, chain):
        oo = deploy(chain)
        owner = chain.web3.eth.coinbase
        amount = 1

        # make sure there's balance
        txhash = oo.transact({'from': owner}).mint()
        txreceipt = chain.wait.for_receipt(txhash)

        balance1 = oo.call().balanceOf(owner)
        assert balance1 > 0

        # burn some
        txhash = oo.transact({'from': owner}).burn(amount)
        txreceipt = chain.wait.for_receipt(txhash)

        balance2 = oo.call().balanceOf(owner)
        assert balance2 == (balance1 - amount)

        # TODO: check event data

        return

    def test_f_burn_with_insufficient_balance(self, chain):
        oo = deploy(chain)
        owner = chain.web3.eth.coinbase

        # make sure there's balance
        txhash = oo.transact({'from': owner}).mint()
        txreceipt = chain.wait.for_receipt(txhash)

        balance1 = oo.call().balanceOf(owner)
        assert balance1 > 0

        # try burning more than we've got (gets reverted)
        with pytest.raises(TransactionFailed):
            oo.transact({'from': owner}).burn(balance1 + 1)

        balance2 = oo.call().balanceOf(owner)
        assert balance2 == balance1

        #TODO: check no event emitted

        return

def test_f_transfer(chain):
    oo = deploy(chain)

    fromacct = chain.web3.eth.coinbase
    toacct = chain.web3.eth.accounts[1]
    amount = 42

    # make sure there'll be something to mint
    wait_n_blocks(chain, 10)

    oo.transact().mint()

    balance1 = oo.call().balanceOf(fromacct)
    oo.transact().transfer(toacct, amount)
    balance2 = oo.call().balanceOf(fromacct)

    assert oo.call().balanceOf(toacct) == amount
    assert (balance1 - balance2) == amount

    # TODO: check event data

    return
