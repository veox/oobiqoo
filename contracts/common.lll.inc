;;;; ==========================================================================
;;;; @title NIHLIB
;;;; @author Noel Maersk <veox>

(seq
  ;;; =========================================================================
  ;;; MEMORY LAYOUT

  (def '*memloc-function-selector* 0x20)
  (def '*memloc-scratchpad*        0x40)

  ;;; =========================================================================
  ;;; STORAGE LAYOUT

  ;; token balances
  ;; 0x 00000000 00000000 00000000 ........ ........ ........ ........ ........
  (def '*storbase-balance*
       0x0000000000000000000000000000000000000000000000000000000000000000)

  ;; allowances: from this very token's owner
  ;; 0x 01000000 00000000 00000000 ........ ........ ........ ........ ........
  (def '*storbase-allowance-from-this*
       0x0100000000000000000000000000000000000000000000000000000000000000)
  ;; 0x 02000000 00000000 00000000 ........ ........ ........ ........ ........
  (def '*storbase-allowance-from-this-expires*
       0x0200000000000000000000000000000000000000000000000000000000000000)

  ;; allowances: to this very token's owner
  ;; 0x 01010000 00000000 00000000 ........ ........ ........ ........ ........
  (def '*storbase-allowance-to-this*
       0x0101000000000000000000000000000000000000000000000000000000000000)
  ;; 0x 02010000 00000000 00000000 ........ ........ ........ ........ ........
  (def '*storbase-allowance-to-this-expires*
       0x0201000000000000000000000000000000000000000000000000000000000000)

  ;; allowances: other to other (hash-packed)
  ;; 0x 0102.... ........ ........ ........ ........ ........ ........ ........
  (def '*storbase-allowance*
       0x0102000000000000000000000000000000000000000000000000000000000000)
  ;; 0x 0202.... ........ ........ ........ ........ ........ ........ ........
  (def '*storbase-allowance-expires*
       0x0202000000000000000000000000000000000000000000000000000000000000)

  ;; which library implements this function?
  ;; 0x ffffffff ffffffff ffffffff ffffffff 00000000 00000000 00000000 ........
  (def '*storbase-implementing-lib*
       0xffffffffffffffffffffffffffffffff00000000000000000000000000000000)
  ;; what is the size of data this function returns?
  ;; 0x ffffffff ffffffff ffffffff ffffffff 00000000 00000001 00000000 ........
  (def '*storbase-return-size*
       0xffffffffffffffffffffffffffffffff00000000000000010000000000000000)

  ;; ERC165 supportsInterface
  ;; 0x ffffffff ffffffff ffffffff ffffffff 00000000 00000002 00000000 ........
  (def '*storbase-supports-interface*
       0xffffffffffffffffffffffffffffffff00000000000000020000000000000000)
  ;; 0x ffffffff ffffffff ffffffff ffffffff 00000000 00000003 00000000 ........
  (def '*storbase-supports-interface-extension*
       0xffffffffffffffffffffffffffffffff00000000000000030000000000000000)

  ;; configuration fields
  ;; 0x ffffffff ffffffff ffffffff ffffffff ffffffff 00000000 00000000 ........
  (def '*storbase-config*
       0xffffffffffffffffffffffffffffffffffffffff000000000000000000000000)

  ;; variable fields
  ;; 0x ffffffff ffffffff ffffffff ffffffff ffffffff ffffffff 00000000 ........
  (def '*storbase-vars*
       0xffffffffffffffffffffffffffffffffffffffffffffffff0000000000000000)

  ;;; =========================================================================
  ;;; CONSTANTS

  ;; booleans
  (def '*false* 0)
  (def '*true*  1)

  ;;; =========================================================================
  ;;; UTILS

  ;; --------------------------------------------------------------------------
  ;; @author Ben Edgington <benjaminion>
  ;; @notice Convenience macros to load function arguments.
  ;; @dev To be used with "web3-compatible functions" only.

  (def 'cdload-arg1 (calldataload 0x04))
  (def 'cdload-arg2 (calldataload 0x24))
  (def 'cdload-arg3 (calldataload 0x44))

  ;; --------------------------------------------------------------------------
  ;; @author Ben Edgington <benjaminion>
  ;; @notice Ensure being called with the expected number of arguments.
  ;; @dev To be used with "web3-compatible functions" only.

  (def 'calldata-has-one-arg    (unless (= 0x24 (calldatasize)) (revert 0 0)))
  (def 'calldata-has-two-args   (unless (= 0x44 (calldatasize)) (revert 0 0)))
  (def 'calldata-has-three-args (unless (= 0x64 (calldatasize)) (revert 0 0)))

  ;; --------------------------------------------------------------------------
  ;; @author Noel Maersk <veox>, Ben Edgington <benjaminion>
  ;; @notice Check that address contained in 32-byte word has only 20 lower
  ;;         ones set. (20 bytes == 160 bits)

  (def 'when-is-not-address (addr code-body) (when (shr addr 160) code-body))

  ;;; =========================================================================
  ;;; WEB3 ABI

  ;; --------------------------------------------------------------------------
  ;; @author Daniel Ellison <zigguratt>
  ;; @notice Retrieves the requested function selector from the first four
  ;;         bytes of the call data.

  (def 'calldata-function-selector
       (shr (calldataload 0x00) 224))

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

  (def 'fun (function-selector code-body)
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
       (when (callvalue) (revert 0 0)))

  ;; --------------------------------------------------------------------------
  ;; @author Just about everybody.
  ;; @notice Convenience macro for emitting events with 1 indexed chunk.
  ;; @dev Currently does not support data longer than 32 bytes total.
  ;; @param id 32-byte event identifier.
  ;; @param indexed Data chunk that will also be indexed by in logs.
  ;; @param data Non-indexed data to be placed in logs.
  ;; @param datasize Number of bytes in data.

  (def 'emit1 (id indexed data datasize)
       (seq
         (mstore *memloc-scratchpad* data)
         (log2 *memloc-scratchpad* datasize id indexed)))

  ;; --------------------------------------------------------------------------
  ;; @author Just about everybody.
  ;; @notice Convenience macro for emitting events with 2 indexed chunks.
  ;; @dev Currently does not support data longer than 32 bytes total.
  ;; @param id 32-byte event identifier.
  ;; @param indexed0 Data chunk 0 that will also be indexed by in logs.
  ;; @param indexed1 Data chunk 1 that will also be indexed by in logs.
  ;; @param data Non-indexed data to be placed in logs.
  ;; @param datasize Number of bytes in data.

  (def 'emit2 (id indexed0 indexed1 data datasize)
       (seq
         (mstore *memloc-scratchpad* data)
         (log3 *memloc-scratchpad* datasize id indexed0 indexed1))))
