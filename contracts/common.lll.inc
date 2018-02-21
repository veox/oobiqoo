;;;; ==========================================================================
;;;; @title NIHLIB
;;;; @author Noel Maersk <veox>

(seq
  ;;; =========================================================================
  ;;; MEMORY LAYOUT

  (def '*memloc-function-selector* 0x20)

  ;;; =========================================================================
  ;;; STORAGE LAYOUT

  ;; FIXME: put these somewhere :/
  (def '*storloc-owner*               0x00)
  (def '*storloc-name*                0x00)
  (def '*storloc-symbol*              0x00)
  (def '*storloc-decimals*            0x00)
  (def '*storloc-total-supply*        0x00)
  (def '*storloc-def-approval-dur*    604800) ; one week

  ;; token balances
  ;; 0x 00000000 00000000 00000000 ........ ........ ........ ........ ........
  (def '*storbase-balance*
       0x0000000000000000000000000000000000000000000000000000000000000000)

  ;; allowances: other to other (hash-packed)
  ;; 0x 0100.... ........ ........ ........ ........ ........ ........ ........
  (def '*storbase-allowance*
       0x0100000000000000000000000000000000000000000000000000000000000000)
  ;; 0x 0200.... ........ ........ ........ ........ ........ ........ ........
  (def '*storbase-allowance-expires*
       0x0200000000000000000000000000000000000000000000000000000000000000)
  ;; allowances: from this very token's owner
  ;; 0x 01010000 00000000 00000000 ........ ........ ........ ........ ........
  (def '*storbase-allowance-from-this*
       0x0101000000000000000000000000000000000000000000000000000000000000)
  ;; 0x 02010000 00000000 00000000 ........ ........ ........ ........ ........
  (def '*storbase-allowance-from-this-expires*
       0x0201000000000000000000000000000000000000000000000000000000000000)
  ;; allowances: to this very token's owner
  ;; 0x 01020000 00000000 00000000 ........ ........ ........ ........ ........
  (def '*storbase-allowance-to-this*
       0x0102000000000000000000000000000000000000000000000000000000000000)
  ;; 0x 02020000 00000000 00000000 ........ ........ ........ ........ ........
  (def '*storbase-allowance-to-this-expires*
       0x0202000000000000000000000000000000000000000000000000000000000000)

  ;; which library implements this function?
  ;; 0x ffffffff ffffffff ffffffff ffffffff ffffffff ffffffff 00000000 ........
  (def '*storbase-implementing-lib*
       0xffffffffffffffffffffffffffffffffffffffffffffffff0000000000000000)
  ;; what is the size of data this function returns?
  ;; 0x ffffffff ffffffff ffffffff ffffffff ffffffff ffffffff 10000000 ........
  (def '*storbase-return-size*
       0xffffffffffffffffffffffffffffffffffffffffffffffff1000000000000000)

  ;;; =========================================================================
  ;;; CONSTANTS

  ;; booleans
  (def '*false* 0)
  (def '*true*  1)

  ;;; =========================================================================
  ;;; UTILS

  ;; --------------------------------------------------------------------------
  ;; @author Daniel Ellison <zigguratt>, Noel Maersk <veox>
  ;; @notice Shifts the leftmost bits of a 32-byte number right.
  ;; @dev E.g. (shift-right *data* 224) will shift *data* by 224/8 == 28 bytes,
  ;;      leaving the leftmost 32-28 == 4 bytes.
  ;;      0x14ab90388092664827928d90384c73d82c5bf21abb61dd7d4971fc65f4851dfb
  ;;      0x0000000000000000000000000000000000000000000000000000000014ab9038
  ;; @param input A 32-byte number.

  ;; TODO: same as lllc-provided `shr`?..
  (def 'shift-right (input nbits)
       (div input (exp 2 nbits)))

  ;; TODO: same as lllc-provided `shl`?..
  (def 'shift-left (input nbits)
       (mul input (exp 2 nbits)))

  ;;; =========================================================================
  ;;; WEB3 ABI

  ;; --------------------------------------------------------------------------
  ;; @author Daniel Ellison <zigguratt>
  ;; @notice Retrieves the requested function selector from the first four
  ;;         bytes of the call data.

  (def 'calldata-function-selector
       (shift-right (calldataload 0x00) 224))

  ;; --------------------------------------------------------------------------
  ;; @author Ben Edgington <benjaminion>
  ;; @notice Gets the function selector and stores it in memory for reference.
  ;; @dev The function selector is stored at a pre-defined memory location and
  ;;      can be read from there every time instead of accessing the call data.
  ;; TODO: consider lll-docs -> lll_abi.html#passing-data-to-a-function

  (def 'mstore-function-selector
       (mstore *memloc-function-selector*
               calldata-function-selector))

  ;; --------------------------------------------------------------------------
  ;; @author Daniel Ellison <zigguratt>
  ;; @notice Determines whether the supplied function selector matches a known
  ;;         one and executes <code-body> if so.
  ;; @dev The selector is in the leftmost four bytes of the call data:
  ;;      https://github.com/ethereum/wiki/wiki/Ethereum-Contract-ABI
  ;; @param function-selector The four-byte hash of a known function signature.
  ;; @param code-body The code to run in the case of a match.

  (def 'function (function-selector code-body)
       (when (= (mload *memloc-function-selector*) function-selector)
         code-body))

  ;; --------------------------------------------------------------------------
  ;; @author Noel Maersk <veox>, Daniel Ellison <zigguratt>
  ;; @notice Retrieves data return size for a given (in-mem) function selector.

  (def 'return-size (function-selector)
       (sload (+ *storloc-base-return-size* function-selector)))

  ;; --------------------------------------------------------------------------
  ;; @author Daniel Ellison <zigguratt>
  ;; @notice Forbid ether transfers.

  (def 'unpayable
       (when (callvalue) (revert 0 0))))
