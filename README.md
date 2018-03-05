# oobiqoo

A Universal Basic Income scheme built on Ethereum, as a system of ERC20
tokens referenced from a registry.

The tokens are "mintable", allowing the creation of one indivisible
unit every second.

In early implementation stage.


## Development

[Populus](https://github.com/ethereum/populus/) is used for development.
Although `requirements.txt` specifies `populus==2.1.0`, the actual version
required is the one in [my `populus/lll-to-merge`
branch](https://github.com/veox/populus/tree/lll-to-merge), at least until
[`ethereum/populus` PR 408](https://github.com/ethereum/populus/pull/408)
is merged.


## License

If not stated otherwise, everything in this repository is licensed under the
GNU Affero General Public License - specifically, AGPLv3.

See [`LICENSE.txt`](LICENSE.txt).


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
