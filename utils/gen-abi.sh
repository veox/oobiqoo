#!/bin/sh

for f in *.solidity; do
    name="`echo $f | cut -d. -f1`.lll.abi"
    echo "Generating $name from $f..."
    solc --abi $f | grep -E "^\[" > $name
done
