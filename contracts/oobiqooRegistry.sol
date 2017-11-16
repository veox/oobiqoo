pragma solidity ~0.4.18;
//pragma experimental SMTChecker;
pragma experimental "v0.5.0";

/*
 * Who's who in oobiqoo?
 * TODO: general desc
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

    ///
    function register() external returns(address) {
        require(registry[msg.sender] == 0); // TODO: type cast?

        oobiqoo o = new oobiqoo(msg.sender); // FIXME: address precomputable?
        address a = address(o); // TODO: type cast not needed, use directly?
        registry[msg.sender] = a;

        // TODO: actually register on ENS

        return a;
    }

    ///
    function () external {
        revert();
    }
}
