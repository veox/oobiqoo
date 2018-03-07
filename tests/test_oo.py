# =============================================================================
# HELPERS

def get_oo_instance(chain, owner=None):
    if owner is None:
        owner = chain.web3.eth.coinbase
    oo, _ = chain.provider.get_or_deploy_contract('oo', deploy_transaction={"from": owner})
    assert oo.address != 0
    assert oo.address != owner
    return oo

# =============================================================================
# TESTS

def test_deployment(chain):
    oo = get_oo_instance(chain, owner=chain.web3.eth.coinbase)
    return

# =============================================================================
# TESTS: non-writing

def test_f_get_owner(chain):
    oo = get_oo_instance(chain)
    assert oo.call().owner() == chain.web3.eth.coinbase
    return

def test_f_get_name(chain):
    oo = get_oo_instance(chain)
    assert oo.call().name() == "oo"
    return

def test_f_get_symbol(chain):
    oo = get_oo_instance(chain)
    assert oo.call().symbol() == "oo." + chain.web3.eth.coinbase[2:]
    return

def test_f_get_decimals(chain):
    oo = get_oo_instance(chain)
    assert oo.call().decimals() == 0
    return

def test_f_get_total_supply(chain):
    oo = get_oo_instance(chain)
    assert oo.call().totalSupply() == 0
    return

def test_f_get_default_approval_duration(chain):
    oo = get_oo_instance(chain)
    assert oo.call().get_default_approval_duration() == 60*60*24*7
    return
