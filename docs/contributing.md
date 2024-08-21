# Contributing

Jelly is an open project – **you are welcome to submit issues, pull requests, or just ask questions**.

## Contributing to the Jelly specification

The Jelly Protocol Buffers and gRPC definitions are in the [jelly-protobuf repository](https://github.com/Jelly-RDF/jelly-protobuf). If you want to contribute to the specification, it is strongly recommended that you first **[open an issue there](https://github.com/Jelly-RDF/jelly-protobuf/issues/new/choose)** to discuss your idea.

The [specification documents](specification/index.md) are edited in the same way as other documentation pages. See the next section for details.

## Editing documentation

The documentation is written in Markdown and built using [MkDocs](https://www.mkdocs.org/), using [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

To edit a documentation page, simply click the :material-file-edit-outline: button in the top-right of the page:

![Edit this page](assets/edit_button.png)

It will take you to GitHub, where you can edit the Markdown file and submit a pull request. You can also clone [the repository](https://github.com/Jelly-RDF/jelly-rdf.github.io) and edit the files locally. The source files are in the `docs` directory.

Note: the `reference.md` file is automatically generated from the Jelly Protocol Buffers definitions. Do not edit it directly.

### Macros

The documentation makes use of several macros for generating links, displaying the software version, etc. The macros are used in the Markdown files like this:

```markdown
**Version**: {{ '{{ proto_version() }}' }}
```

Which yields: 

> **Version**: {{ proto_version() }}

The list of available macros can be found in the [`main.py` file]({{ git_docs_link('main.py') }}) in the root of the repository.

### Local testing of the website

Install the project's dependencies from `requirements.txt` (preferably in a virtual environment). Then, run `mkdocs serve` to compile the docs and serve them locally for testing.

```bash
# Create a virtual environment – use your preferred tool here
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the local server
mkdocs serve
```

### Making a Jelly protocol release

Jelly protocol releases are handled from the `jelly-protobuf` repository. To make a new tagged release, follow these steps:

1. Clone the [`jelly-protobuf` repository](https://github.com/Jelly-RDF/jelly-protobuf).
2. Make sure you are on the `main` branch and that it is up-to-date: `git checkout main && git pull`
3. Create a new tag for the release. For example, for version 1.2.3: `git tag v1.2.3`
4. Push the tag to GitHub: `git push origin v1.2.3`

The CI/CD pipeline will automatically pick up the new tag and make a tagged release of the documentation, including the protocol specification. The [spec pages](specification/index.md) use [macros](#macros) to display the current version, so they will be updated automatically.

After a new protocol release, you should also update the implementations to use it.

### Further reading

- [Material for MkDocs reference](https://squidfunk.github.io/mkdocs-material/reference/)
- [MkDocs documentation](https://www.mkdocs.org/user-guide/writing-your-docs/)
- [Macro plugin documentation](https://mkdocs-macros-plugin.readthedocs.io/en/latest/)

### Editing Jelly-JVM documentation

Use the exact same process as for the website documentation. The Jelly-JVM documentation sources are in the [`jelly-jvm` repository](https://github.com/Jelly-RDF/jelly-jvm), `docs/docs` directory.

## Contributing to Jelly implementations

### Jelly-JVM

- **[Jelly-JVM documentation]({{ jvm_link()}})** includes the developer guide, explaining the technical aspects of contributing to it.
- **[GitHub repository](https://github.com/Jelly-RDF/jelly-jvm)**
- **[Issue tracker](https://github.com/Jelly-RDF/jelly-jvm/issues)**
