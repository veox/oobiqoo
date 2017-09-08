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

// FIXME: OpenZeppelin uses contract inheritance instead of libraries
// which hinders upgradability and call delegation.
// Also, I don't like how they don't prefix events with `log`, don't
// stylistically separate modifiers, function names, and variable names.

// FIXME: use ethpm for these zeppelins
import 'BurnableToken.sol';
import 'MintableToken.sol';

/// @dev minimal, with the only signature that will be used
interface ERC20FakeInterface {
    function transfer(address /* _to */, uint256 /* _amount */) returns (bool);
}

contract UBI is MintableToken, BurnableToken {
    ///
    uint256 public lastMintInvocationTime;

    ///
    function mintAllowance() public view returns(uint256) {
        int256 diff = now - lastMintInvocationTime;
        assert(diff >= 0);
        return uint256(diff);
    }

    /// @dev overridden: MintableToken.mint(address, uint256)
    function mint(address _to, uint256 _amount) public onlyOwner canMint returns (bool) {
        // check
        require(mintAllowance() >= _amount);

        // mark
        lastMintInvocationTime = now;

        // transfer all to self...
        assert(super.mint(owner, canMintThisMuch));

        // ...then specified amount to whomever
        assert(super.transfer(_to, _amount));

        return true;
    }

    /// @dev convenience: fall through with owner/full allowance
    function mint() external onlyOwner canMint returns (bool) {
        return mint(owner, mintAllowance());
    }

    /// @dev forward "transfer" of a different token
    function otherTransfer(address _otherTokenAddress, address _to, uint256 _amount) external onlyOwner returns (bool) {
        // to transfer _this_ token, use regular `transfer()`
        require(_otherTokenAddress != this.address);

        //
        ERC20FakeInterface otherToken = ERC20FakeInterface(_otherTokenAddress);

        // may throw, return true or false: up to "other" token
        return otherToken.transfer.gas(msg.gas)(_to, _amount);
    }

    ///
    function () payable {
        // TODO: check `allowedFunctionSignatures`, do delegatecall
        throw;
    }
}
