# oobiqoo

An implementation of UBI on Ethereum, as a system of ERC20 tokens
referenced from a registry.

The tokens are "mintable", allowing the creation of one indivisible
unit every second.

In early design stage.

License: GPLv3.


## See also

* [Circles overview][circles], an eerily similar proposal.
* A [dispatcher contract][dispatcher] and the [contract delegated to][dispatch-to]
  by said dispatcher, from [this wonderful series of articles][resurrection] by
  Daniel Ellison.
* An implementation of an [ERC20 token in LLL][erc20-lll], by Ben Edgington.

[circles]: https://github.com/CirclesUBI/docs/blob/master/Circles.md
[dispatch-to]: https://github.com/zigguratt/lll-dispatcher/blob/master/src/arithmetic.lll
[dispatcher]: https://github.com/zigguratt/lll-dispatcher/blob/master/src/dispatcher.lll
[resurrection]: http://blog.syrinx.net/the-resurrection-of-lll-part-1/
[erc20-lll]: https://github.com/benjaminion/LLL_erc20
