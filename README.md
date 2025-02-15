[![Website](https://img.shields.io/website?url=https%3A%2F%2Fjelly-rdf.github.io%2Fdev%2F)](https://w3id.org/jelly/dev/) [![.github/workflows/pre-release.yaml](https://github.com/Jelly-RDF/jelly-rdf.github.io/actions/workflows/publish-dev.yaml/badge.svg)](https://github.com/Jelly-RDF/jelly-rdf.github.io/actions/workflows/publish-dev.yaml) ![GitHub License](https://img.shields.io/github/license/Jelly-RDF/jelly-rdf.github.io) [![Discord](https://img.shields.io/discord/1333391881404420179?label=Discord%20chat)](https://discord.gg/A8sN5XwVa5)

# Jelly website and documentation repository

See the deployed website here: **https://w3id.org/jelly**

## Contributing

Pull requests are welcome. You can also [**open an issue**](https://github.com/Jelly-RDF/jelly-rdf.github.io/issues/new/choose) to discuss documentation changes or improvements.

If you want to instead contribute to the Jelly serialization format or the Jelly-JVM implementation, see these repositories and their issue trackers:

- [Jelly serialization format and streaming protocol](https://github.com/Jelly-RDF/jelly-protobuf) ([issue tracker](https://github.com/Jelly-RDF/jelly-protobuf/issues))
- [Jelly-JVM](https://github.com/Jelly-RDF/jelly-jvm) ([issue tracker](https://github.com/Jelly-RDF/jelly-jvm/issues))

## Editing the documentation

The documentation is written in Markdown and built using [MkDocs](https://www.mkdocs.org/), using [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/). The source files are in the `docs` directory – feel free to edit them directly.

**More information on how to edit the documentation can be found in the [contribution guide](https://w3id.org/jelly/dev/contributing/) on the website.**

### Local testing of the website

Install the project's dependencies from `requirements.txt` (preferably in a virtual environment). Then, run `mkdocs serve` to compile the docs and serve them locally for testing.

### See also

- **[Full contribution guide](https://w3id.org/jelly/dev/contributing/)**
- [Material for MkDocs reference](https://squidfunk.github.io/mkdocs-material/reference/) for help with Markdown syntax and other features
- [Jelly Discord chat](https://discord.gg/A8sN5XwVa5) for questions and discussions

## License

The documentation of Jelly is licensed under the [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) license.
