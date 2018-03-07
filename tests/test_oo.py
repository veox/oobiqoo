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

# =============================================================================
# TESTS

def test_deployment(chain):
    oo = deploy(chain, owner=chain.web3.eth.coinbase)
    return

# =============================================================================
# TESTS: non-writing

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

    # roll the chain
    waitnblocks = 10
    waituntil = chain.web3.eth.getBlock('latest')['number'] + waitnblocks
    chain.wait.for_block(block_number=waituntil)

    # mintable on block2
    mintable2 = oo.call().get_mintable()

    assert mintable2 > mintable1
    assert mintable2 <= 15 * waitnblocks

    return
