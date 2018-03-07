# =============================================================================
# HELPERS

def get_oobiqoo_instance(chain, owner=None):
    if owner is None:
        owner = chain.web3.eth.coinbase
    oobiqoo, _ = chain.provider.get_or_deploy_contract('oobiqoo', deploy_transaction={"from": owner})
    assert oobiqoo.address != 0
    assert oobiqoo.address != owner
    return oobiqoo

# =============================================================================
# TESTS

def test_deployment(chain):
    oobiqoo = get_oobiqoo_instance(chain, owner=chain.web3.eth.coinbase)
    return
