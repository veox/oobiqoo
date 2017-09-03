pragma solidity ~0.4.16;

contract oobiqoo {
    address public registry;

    function hereiam() external returns(bool) {
        return new UBI(msg.sender);
    }
}
