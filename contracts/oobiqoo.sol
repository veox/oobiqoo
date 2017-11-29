pragma solidity ~0.4.18;
// needs `z3`, not installed on my system (yet), so disabled
//pragma experimental SMTChecker;
// required for .transfer() no-overload: https://github.com/ethereum/solidity/issues/2683
pragma experimental "v0.5.0";

/*
 * Live and die - a second every second.
 *
 * A single oobiqoo ERC20 token. To be deployed on-request by oobiqooRegistry.
 *
 * Author:  Noel Maersk (veox)
 * License: GPLv3
 * Sources: https://gitlab.com/veox/oobiqoo
 * Compile: TODO
 */

import "./majoolr/TokenLib.sol";

/// @dev minimal, with the only signature that will be used
interface ERC20Interface {
    function transfer(address /* _to */, uint256 /* _amount */) external returns (bool);
}

contract oobiqoo {
    using TokenLib for TokenLib.TokenStorage;

    ///
    TokenLib.TokenStorage token;
    ///
    uint256 public prevMintTime;

    // TODO: drop? already checked by TokenLib where necessary?
    modifier only_owner { require(msg.sender == token.owner); _; }

    /// @dev constructor
    function oobiqoo(address __owner) {
        token.init({
                    _owner: __owner,
                    _name: "oobiqoo",   // TODO: custom deterministic name/symbol:
                    _symbol: "oobiqoo", //       perhaps 'oobiqoo.' + str(msg.sender)
                    _decimals: 0,
                    _initial_supply: 0,
                    _allowMinting: true });
    }

    // UGLY: wrap-around TokenLib struct for ERC20 function signatures
    function owner() external view returns (address) { return token.owner; }
    function name() external view returns (string) { return token.name; }
    function symbol() external view returns (string) { return token.symbol; }
    function decimals() external view returns (uint8) { return token.decimals; }
    function totalSupply() external view returns (uint256) { return token.totalSupply; }
    function balanceOf(address who) external view returns (uint256) {
        return token.balanceOf(who);
    }
    function allowance(address owner, address spender) external view returns (uint256) {
        return token.allowance(owner, spender);
    }
    function transfer(address to, uint value) external returns (bool ok) {
        return token.transfer(to, value);
    }
    function transferFrom(address from, address to, uint value) external returns (bool ok) {
        return token.transferFrom(from, to, value);
    }
    function approve(address spender, uint value) external returns (bool ok) {
        return token.approve(spender, value);
    }

    /// @dev how many seconds have passed since previous minting
    function mintAllowance()
        public
        view
        returns (uint256)
    {
        // TODO: use BasicMathLib?
        require(now >= prevMintTime);
        return (now - prevMintTime);
    }

    ///
    function reserveFullMintAllowance()
        private
        returns (uint256)
    {
        uint256 max = mintAllowance();
        prevMintTime = now;
        return max;
    }

    /// @dev mint full allowance to owner
    function mint()
        public
        only_owner
        returns (bool)
    {
        uint256 max = reserveFullMintAllowance();

        // transfer full allowance to owner...
        assert(token.mintToken(max));

        // ...and everything belonging to _this_ contract, if any
        uint256 stuck = token.balanceOf(address(this));
        if (stuck > 0) {
            require(this.transfer(token.owner, stuck));
        }

        return true;
    }

    /// @dev convenience: mint and transfer in same call
    function mint(address _to, uint256 _amount)
        external
        only_owner
        returns (bool)
    {
        // transfer full allowance to owner...
        require(mint());

        // ...then specified amount from caller (owner) to whomever
        require(token.transfer(_to, _amount));

        return true;
    }

    /// @dev forward "transfer" call of a different token owned by _this_ contract
    /// @notice most likely to happen when someone meant to transfer to token.owner
    function transferOtherToken(address _otherTokenAddress, address _to, uint256 _amount)
        external
        only_owner
        returns (bool)
    {
        // to transfer _this_ contract's tokens belonging to itself, use `mint()`
        require(_otherTokenAddress != address(this));

        //
        ERC20Interface otherToken = ERC20Interface(_otherTokenAddress);

        // may throw, return true or false: up to "other" token
        // TODO: is gas specification even needed here? remove if not
        return otherToken.transfer.gas(msg.gas)(_to, _amount);
    }

    /// @dev fallback - don't accept ether transfers (for now)
    function ()
        external
    {
        // TODO?: if/else, check `allowedFunctionSignatures`, do delegatecall
        require(msg.data.length == 0);
        mint();
    }
}
