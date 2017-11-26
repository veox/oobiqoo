pragma solidity ~0.4.18;
//pragma experimental SMTChecker;
pragma experimental "v0.5.0";

/*
 * Who's who in oobiqoo?
 *
 * ENS registry and entry-point for participation.
 *
 * Author:  Noel Maersk (veox)
 * License: GPLv3
 * Sources: https://gitlab.com/veox/oobiqoo
 * Compile: TODO
 */

import "./oobiqoo.sol";

// FIXME: stub!
contract oobiqooRegistry {
    mapping (address => address) public registry;

    /// @dev register an address as participating, create token
    function register() public returns(address) {
        require(registry[msg.sender] == 0);

        oobiqoo o = new oobiqoo(msg.sender); // FIXME: address precomputable?
        registry[msg.sender] = address(o);

        // TODO: actually register on ENS

        return address(o);
    }

    /// @dev fallback
    function () external {
        require(msg.data.length == 0);
        register();
    }
}
