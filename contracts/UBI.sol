pragma solidity ~0.4.16;
pragma experimental SMTChecker;

/*
 * Live and die - a second every second.
 * TODO: general desc
 *
 * Author:  Noel Maersk (veox)
 * License: GPLv3
 * Sources: https://gitlab.com/veox/oobiqoo (TODO: Not yet available - stay tuned!..)
 * Compile: TODO
 */

contract UBI {
    ///
    uint256 public lastMintInvocationTime;

    ///
    function mintAllowance() public view returns(uint) {
        return now - lastMintInvocationTime;
    }

    ///
    function () payable {
        // TODO: check allowedFunctionSignatures, do delegatecall
        throw;
    }
}
