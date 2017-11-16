pragma solidity ~0.4.18;
// needs `z3`, not installed on my system (yet), so disabled
//pragma experimental SMTChecker;
// required for .transfer() no-overload: https://github.com/ethereum/solidity/issues/2683
pragma experimental "v0.5.0";

/*
 * Live and die - a second every second.
 *
 * A single oobiqoo token. Allows minting one unit every second.
 *
 * Author:  Noel Maersk (veox)
 * License: GPLv3
 * Sources: https://gitlab.com/veox/oobiqoo
 * Compile: TODO
 */

import "./majoolr/TokenLib.sol";

/// @dev minimal, with the only signature that will be used.
interface ERC20Interface {
    function transfer(address /* _to */, uint256 /* _amount */) external returns (bool);
}

contract oobiqoo {
    using TokenLib for TokenLib.TokenStorage;

    ///
    TokenLib.TokenStorage token;
    ///
    uint256 public lastMintInvocationTime;

    uint8 constant DECIMALS = 0;
    uint256 constant INITIAL_SUPPLY = 1; // TODO: 0 when Majoolr fixes issue #41

    /// @dev constructor
    function oobiqoo(address _owner) {
        // TODO: custom deterministic name/symbol: perhaps 'oobiqoo.' + str(msg.sender)
        token.init(_owner, "oobiqoo", "oobiqoo", DECIMALS, INITIAL_SUPPLY, true);
    }

    // UGLY: wrap-around TokenLib struct for ERC20 function signatures
    function owner() constant returns (address) { return token.owner; }
    function name() constant returns (string) { return token.name; }
    function symbol() constant returns (string) { return token.symbol; }
    function decimals() constant returns (uint8) { return token.decimals; }
    function totalSupply() constant returns (uint256) { return token.totalSupply; }
    function balanceOf(address who) constant returns (uint256) {
        return token.balanceOf(who);
    }
    function allowance(address owner, address spender) constant returns (uint256) {
        return token.allowance(owner, spender);
    }
    function transfer(address to, uint value) returns (bool ok) {
        return token.transfer(to, value);
    }
    function transferFrom(address from, address to, uint value) returns (bool ok) {
        return token.transferFrom(from, to, value);
    }
    function approve(address spender, uint value) returns (bool ok) {
        return token.approve(spender, value);
    }

    // TODO: drop? already checked by TokenLib where necessary?
    modifier only_owner { require(msg.sender == token.owner); _; }

    ///
    function mintAllowance() public view returns (uint256) {
        // FIXME: use BasicMathLib
        require(now >= lastMintInvocationTime);
        return (now - lastMintInvocationTime);
    }

    /// @dev mint full allowance to owner
    function mint() public only_owner returns (bool) {
        // mark
        lastMintInvocationTime = now;

        // transfer all to self
        assert(token.mintToken(mintAllowance()));

        return true;
    }

    /// @dev convenience: mint and transfer in same call
    function mint(address _to, uint256 _amount)
        public
        only_owner
        returns (bool)
    {
        // transfer all to self...
        require(mint());

        // ...then specified amount to whomever
        require(token.transfer(_to, _amount));

        return true;
    }

    /// @dev forward "transfer" call of a different token
    function otherTransfer(address _otherTokenAddress, address _to, uint256 _amount)
        external
        only_owner
        returns (bool)
    {
        // to transfer _this_ token, use regular `transfer()` instead
        require(_otherTokenAddress != address(this));

        //
        ERC20Interface otherToken = ERC20Interface(_otherTokenAddress);

        // may throw, return true or false: up to "other" token
        return otherToken.transfer.gas(msg.gas)(_to, _amount);
    }

    ///
    function () external {
        // TODO?: check `allowedFunctionSignatures`, do delegatecall
        revert();
    }
}
