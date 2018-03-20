#

# TODO: check all events are correctly emitted (or not, on failure)

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
    assert oo.call().owner() == owner

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
# TESTS: read-only (mostly testing for "function selector recognised")

def test_f_get_owner(chain):
    oo = deploy(chain)
    assert oo.call().owner() == chain.web3.eth.coinbase
    return

@pytest.mark.xfail(strict=True)
def test_f_get_name(chain):
    oo = deploy(chain)
    assert oo.call().name() == 'oo'
    return

@pytest.mark.xfail(strict=True)
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
    assert oo.call().get_default_approval_duration() == (60*60*24*7)
    return

def test_f_get_balance(chain):
    oo = deploy(chain)
    assert oo.call().balanceOf(chain.web3.eth.coinbase) == 0
    return

def test_f_get_mintable(chain):
    oo = deploy(chain)
    nblocks = 10

    # mintable a bit after deployment (likely 1 block later)
    mintable1 = oo.call().get_mintable()

    wait_n_blocks(chain, nblocks)

    # mintable on block2
    mintable2 = oo.call().get_mintable()

    assert mintable2 > mintable1
    assert mintable2 <= 15 * nblocks

    return

# NOTE: main tests in TestAprovals class!
def test_f_get_allowance(chain):
    oo = deploy(chain)
    owner = chain.web3.eth.coinbase
    alice = chain.web3.eth.accounts[1]
    assert oo.call().allowance(owner, alice) == 0
    return

def test_f_get_allowance_expires(chain):
    oo = deploy(chain)
    owner = chain.web3.eth.coinbase
    alice = chain.web3.eth.accounts[1]
    assert oo.call().get_allowance_expires(owner, alice) == 0
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
        supply1 = oo.call().totalSupply()

        # after some time - still no balance, can mint
        assert balance1 == 0
        assert mintable1 > 0
        assert supply1 == 0

        txhash = oo.transact({'from': owner}).mint()
        txreceipt = chain.wait.for_receipt(txhash)

        balance2 = oo.call().balanceOf(owner)
        mintable2 = oo.call().get_mintable()
        supply2 = oo.call().totalSupply()

        # got balance, there's less left to mint
        assert balance2 > 0
        assert mintable1 > mintable2 > 0
        assert supply2 == mintable1

        # TODO: check event data

        return

    def test_f_mint_non_owner(self, chain):
        oo = deploy(chain)
        mallory = chain.web3.eth.accounts[1]

        # has no balance before minting
        assert oo.call().balanceOf(mallory) == 0
        assert oo.call().totalSupply() == 0

        # transaction gets reverted
        with pytest.raises(TransactionFailed):
            oo.transact({'from': mallory}).mint()

        # has no balance after mint() attempt
        assert oo.call().balanceOf(mallory) == 0
        assert oo.call().totalSupply() == 0

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
        supply1 = oo.call().totalSupply()

        assert balance1 > 0
        assert supply1 == balance1

        # burn some
        txhash = oo.transact({'from': owner}).burn(amount)
        txreceipt = chain.wait.for_receipt(txhash)

        balance2 = oo.call().balanceOf(owner)
        supply2 = oo.call().totalSupply()

        assert balance2 == (balance1 - amount)
        assert supply2 == (supply1 - amount)

        # TODO: check event data

        return

    def test_f_burn_with_insufficient_balance(self, chain):
        oo = deploy(chain)
        owner = chain.web3.eth.coinbase

        # make sure there's balance
        txhash = oo.transact({'from': owner}).mint()
        txreceipt = chain.wait.for_receipt(txhash)

        balance1 = oo.call().balanceOf(owner)
        supply1 = oo.call().totalSupply()

        assert balance1 > 0
        assert supply1 == balance1

        # try burning more than we've got (gets reverted)
        with pytest.raises(TransactionFailed):
            oo.transact({'from': owner}).burn(balance1 + 1)

        balance2 = oo.call().balanceOf(owner)
        supply2 = oo.call().totalSupply()

        assert balance2 == balance1
        assert supply2 == supply1

        #TODO: check no event emitted

        return

def test_f_transfer(chain):
    oo = deploy(chain)
    owner = chain.web3.eth.coinbase
    alice = chain.web3.eth.accounts[1]
    amount = 42

    # make sure there's balance
    wait_n_blocks(chain, 10)
    oo.transact().mint()

    balance1 = oo.call().balanceOf(owner)
    oo.transact().transfer(alice, amount)
    balance2 = oo.call().balanceOf(owner)

    assert oo.call().balanceOf(alice) == amount
    assert (balance1 - balance2) == amount

    # TODO: check event data

    return

# =============================================================================
# TESTS: read/write allowances

def test_f_set_default_approval_duration(chain):
    oo = deploy(chain)
    dur = 42

    duration0 = oo.call().get_default_approval_duration()
    oo.transact().set_default_approval_duration(dur)
    duration1 = oo.call().get_default_approval_duration()

    assert duration0 != duration1
    assert oo.call().get_default_approval_duration() == dur

    return

@pytest.fixture(scope='function')
def oo(chain):
    '''Contract where two other accounts (other than owner) also have balance.'''
    oo = deploy(chain)
    ali = chain.web3.eth.accounts[1]
    bob = chain.web3.eth.accounts[2]
    amount = 10

    # make sure all of owner/ali/bob have balances
    wait_n_blocks(chain, 10)
    oo.transact().mint()
    oo.transact().transfer(ali, amount)
    oo.transact().transfer(bob, amount)

    return oo

FWORD = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
@pytest.fixture(scope='function',
                params=[
                    # from, to, allowance, transfer-amount
                    # TODO: add should-succeed as 0th item
                    [0, 1, 42,    1],
                    [1, 0, 42,    1],
                    [1, 2, 42,    1],
                    [0, 1, FWORD, 1],
                    [1, 0, FWORD, 1],
                    [1, 2, FWORD, 1],
                    [0, 1, 42,    FWORD],
                    [1, 0, 42,    FWORD],
                    [1, 2, 42,    FWORD],
                    [0, 1, FWORD, FWORD],
                    [1, 0, FWORD, FWORD],
                    [1, 2, FWORD, FWORD],
                ])
def xfer(chain, request):
    '''Parametrise cases to test: who sets who's allowance, what its size is, and
       TODO: how much is attempted to collect.'''
    return {'src': chain.web3.eth.accounts[request.param[0]],
            'dst': chain.web3.eth.accounts[request.param[1]],
            'all': request.param[2],
            'amt': request.param[3],
    }

@pytest.mark.incremental
class TestApprovals(object):
    def test_f_approve(self, chain, oo, xfer):
        '''Setting an allowance in general (not testing follow-up collection).'''
        src       = xfer['src'] # from
        dst       = xfer['dst'] # to
        allowance = xfer['all'] # allowance

        balance0src = oo.call().balanceOf(src)
        balance0dst = oo.call().balanceOf(dst)
        allowance0 = oo.call().allowance(src, dst)

        txhash = oo.transact({'from': src}).approve(dst, allowance)
        txreceipt = chain.wait.for_receipt(txhash)
        timestamp = chain.web3.eth.getBlock(txreceipt['blockHash'])['timestamp']

        # balances haven't changed
        assert oo.call().balanceOf(src) == balance0src
        assert oo.call().balanceOf(dst) == balance0dst
        # allowance has increased
        assert oo.call().allowance(src, dst) == (allowance0 + allowance)
        # allowance expiration time is in the future
        assert oo.call().get_allowance_expires(src, dst) >= timestamp

        return

    # TODO: some of the following might be better off as parametrised tests!

    def test_f_approve_timed(self, chain, oo, xfer):
        '''Setting an allowance with a specific expiration date, (not testing
           follow-up collection).'''
        src       = xfer['src'] # from
        dst       = xfer['dst'] # to
        allowance = xfer['all'] # allowance
        duration  = 42          # expires after

        balance0src = oo.call().balanceOf(src)
        balance0dst = oo.call().balanceOf(dst)
        allowance0 = oo.call().allowance(src, dst)
        expires0 = oo.call().get_allowance_expires(src, dst)
        timestamp0 = chain.web3.eth.getBlock('latest')['timestamp']

        txhash = oo.transact({'from': src}).approve_timed(dst, allowance, duration)
        txreceipt = chain.wait.for_receipt(txhash)

        balance1src = oo.call().balanceOf(src)
        balance1dst = oo.call().balanceOf(dst)
        allowance1 = oo.call().allowance(src, dst)
        expires1 = oo.call().get_allowance_expires(src, dst)
        timestamp1 = chain.web3.eth.getBlock(txreceipt['blockHash'])['timestamp']

        # balances haven't changed
        assert balance1src == balance0src
        assert balance1dst == balance0dst
        # allowance has increased
        assert allowance1 == (allowance0 + allowance)
        # allowance expiration time is in the future (but not too far)
        assert expires1 > timestamp0
        assert expires1 < (timestamp0 + duration + 30) # magicnum 30: ~ 2 blocks

        wait_n_blocks(chain, 10)

        balance2src = oo.call().balanceOf(src)
        balance2dst = oo.call().balanceOf(dst)
        allowance2 = oo.call().allowance(src, dst)
        expires2 = oo.call().get_allowance_expires(src, dst)
        timestamp2 = chain.web3.eth.getBlock('latest')['timestamp']

        # balances still haven't changed
        assert balance2src == balance1src
        assert balance2dst == balance1dst
        # allowance has expired
        assert allowance2 == 0
        # allowance expiration time hasn't changed, and is in the past
        assert expires2 == expires1
        assert expires2 < timestamp2

        return

    @pytest.mark.xfail(strict=True)
    def test_f_approve_timed_backdated(self, chain):
        '''Setting expiration earlier than right-now is not allowed.'''
        assert False
        return

    def test_f_collect(self, chain, oo, xfer):
        '''transferFrom()'''
        src = xfer['src'] # from
        dst = xfer['dst'] # to
        amt = xfer['amt'] # attempt to collect this amount

        # re-use test case to set allowance
        self.test_f_approve(chain, oo, xfer)

        balance0src = oo.call().balanceOf(src)
        balance0dst = oo.call().balanceOf(dst)
        allowance0 = oo.call().allowance(src, dst)

        assert balance0src > 0
        assert allowance0 > 0

        # should succeed only if both sufficient allowance and balance
        if allowance0 >= amt and balance0src >= amt:
            oo.transact({'from': dst}).transferFrom(src, dst, amt)
            assert oo.call().balanceOf(src) == (balance0src - amt)
            assert oo.call().balanceOf(dst) == (balance0dst + amt)
            assert oo.call().allowance(src, dst) == (allowance0 - amt)
        else:
            with pytest.raises(TransactionFailed):
                oo.transact({'from': dst}).transferFrom(src, dst, amt)

        return

    @pytest.mark.xfail(strict=True)
    def test_f_collect_unlimited(self, chain):
        '''Collecting when allowance is unlimited does not lower the allowance.'''
        assert False
        return

    @pytest.mark.xfail(strict=True)
    def test_f_collect_outdated(self, chain):
        '''Collecting an allowance after expiration fails.'''
        assert False
        return
