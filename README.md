# oobiqoo

A Universal Basic Income scheme built on Ethereum, as a system of ERC20
tokens referenced from a registry.

The tokens are "mintable", allowing the creation of one indivisible
unit every second.

In early implementation stage.


## Development

[Populus](https://github.com/ethereum/populus/) and Python 3 are used for
development.

`requirements.txt` specifies `populllus==2.1.0`, which is as-of-yet
unreleased. The actual package needed is the one in [this
`populus/lll-to-merge` branch][populllus], at least until
[`ethereum/populus` PR 408][populus-pr408] is merged.

That is not likely to happen in the near future, since Populus currently
lacks a maintainer. I might fork it eventually as Populllus, just so this
very project can be built more easily - both by people and CI tools.

[populllus]: https://github.com/veox/populus/tree/lll-to-merge
[populus-pr408]: https://github.com/ethereum/populus/pull/408


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
* [LLL creation patterns][lll-creation], detailing approaches to the Factory
  programming pattern, when considered in a smart contract context.

[circles]: https://github.com/CirclesUBI/docs/blob/master/Circles.md
[dispatch-to]: https://github.com/zigguratt/lll-dispatcher/blob/master/src/arithmetic.lll
[dispatcher]: https://github.com/zigguratt/lll-dispatcher/blob/master/src/dispatcher.lll
[resurrection]: http://blog.syrinx.net/the-resurrection-of-lll-part-1/
[erc20-lll]: https://github.com/benjaminion/LLL_erc20
[lll-creation]: https://gitlab.com/veox/lll-creation-patterns/blob/master/contracts/README.md
