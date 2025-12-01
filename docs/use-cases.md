# Applications using Jelly

**If you are using Jelly in your project, we would be glad to list it here! Please [open an issue](https://github.com/Jelly-RDF/jelly-rdf.github.io/issues/new/choose) or [open a pull request](https://github.com/Jelly-RDF/jelly-rdf.github.io/edit/main/docs/use-cases.md) with the information on your use case.**

## [Jelly-JVM]({{ jvm_link() }})

### Tools and libraries

- **[jelly-cli](https://github.com/Jelly-RDF/cli)** – simple but performant command-line utility for working with Jelly files.
    - The app can be used to convert to/from Jelly, validate and debug Jelly files.
    - You can find the code and released binaries on [GitHub](https://github.com/Jelly-RDF/cli). The repository also has up-to-date installation instructions and command usage examples.
    - You can also use the [Jelly-RDF/setup-cli](https://github.com/marketplace/actions/setup-jelly-cli) GitHub Action to quickly set up jelly-cli in your CI/CD workflows.
- **[RMLMapper](https://github.com/RMLio/rmlmapper-java)** – library and CLI tool for generating knowledge graphs from semi-structured data, using RML rules.
    - RMLMapper supports Jelly as one of the output formats. You can use it to convert CSV, JSON, Excel, SQL, and other data sources into Jelly.
- **[nanopub-java](https://github.com/Nanopublication/nanopub-java)** – Java library for working with [nanopublications](https://nanopub.net).
    - The library supports Jelly as one of the serialization formats, including processing streams of multiple nanopublications.

### Projects

- **[Nanopub Registry](https://github.com/knowledgepixels/nanopub-registry)** and **[Nanopub Query](https://github.com/knowledgepixels/nanopub-query)** – next-gen services for distributed storage, management, and querying of [nanopublications](https://nanopub.net).
    - Jelly is used for communication between the services in the nanopub network. Jelly endpoints (ending with `.jelly`) are also exposed for downstream applications to consume nanopubs.
    - The Registry stores nanopublications in the Jelly format and uses a Jelly transcoder to merge nanopubs on the fly into a single stream.
- **[RiverBench](https://w3id.org/riverbench)** benchmark suite.
    - Jelly is used as [one of the serialization formats](https://w3id.org/riverbench/v/dev/documentation/dataset-release-format) for distributing datasets in RiverBench.
    - Jelly is also used for [distributing the RDF metadata](https://w3id.org/riverbench/v/dev/documentation/metadata) of benchmark datasets, tasks, and other resources.
    - This is implemented in the [ci-worker](https://github.com/RiverBench/ci-worker) application – a Scala 3 program making heavy use of [Jelly-JVM's]({{ jvm_link() }}) streaming capabilities.
- **[Jelly-JVM benchmark code](https://github.com/Jelly-RDF/jvm-benchmarks)**. This code was used to produce the results seen on the [performance page](performance/index.md).
- **[RDF Stream Taxonomy (RDF-STaX)](https://w3id.org/stax)** uses Jelly for distributing the RDF-STaX ontology and the living literature review of RDF streaming.
    - This is implemented using [jelly-cli](https://github.com/Jelly-RDF/cli). Source code: [GitHub](https://github.com/RDF-STaX/ci-worker).

## Morph-KGC (Python)

**[Morph-KGC](https://github.com/morph-kgc/morph-kgc)** is a Python engine for generating RDF knowledge graphs from heterogeneous data sources using **RML** and **R2RML** mappings.  
Morph-KGC includes **optional Jelly output support** through RDFLib and the `pyjelly` package.

### How Morph-KGC uses Jelly

- Adds **`output_format = JELLY`** as a dedicated serialization option.
- Jelly works in both:
    - **CLI mode:** `python -m morph_kgc`
    - **Python API:** `graph.serialize(destination=..., format="jelly")`
- Produces a single compact **.jelly** binary file suitable for large datasets and downstream streaming pipelines.
- Jelly support is available via:
  ```bash
  pip install "morph-kgc[jelly]"
  ```

### Notes

- Current implementation uses Morph-KGC’s existing text-based pipeline, so Jelly output may be **slower than N-Quads** for very large graphs.
- RDF-star is **not supported** in Jelly output due to reliance on embedded triples.
- The integration is fully accepted upstream; architectural improvements may enable direct binary graph construction in the future.

### Example configuration

```ini
[CONFIGURATION]
output_file = kg.jelly
output_format = JELLY

[DataSource1]
mappings = mapping.ttl
```

## Example datasets in the Jelly format

Below listed are some example datasets available in the Jelly format. All of these are in the [delimited format](user-guide.md#delimited-vs-non-delimited-jelly). The licenses for these datasets are specified on the linked documentation pages.

- Large datasets (millions of triples/quads):
    - [:octicons-download-24: ASSIST-IoT weather measurements](https://w3id.org/riverbench/datasets/assist-iot-weather/1.0.3/files/jelly_full.jelly.gz) ([documentation](https://w3id.org/riverbench/datasets/assist-iot-weather/1.0.3)) – 80 million triples.
    - [:octicons-download-24: 5 million nanopublications](https://w3id.org/riverbench/datasets/nanopubs/1.0.3/files/jelly_full.jelly.gz) ([documentation](https://w3id.org/riverbench/datasets/nanopubs/1.0.3)) – 171 million quads.
    - [:octicons-download-24: RDF-star annotated facts from YAGO](https://w3id.org/riverbench/datasets/yago-annotated-facts/1.0.3/files/jelly_full.jelly.gz) ([documentation](https://w3id.org/riverbench/datasets/yago-annotated-facts/1.0.3)) – 2 million triples.

- Small datasets:
    - [:octicons-download-24: RDF-STaX ontology](https://w3id.org/stax/1.1.4/ontology.jelly) ([documentation](https://w3id.org/stax/1.1.4/ontology)).
    - [:octicons-download-24: RiverBench suite metadata](https://w3id.org/riverbench/v/dev.jelly) ([documentation](https://w3id.org/riverbench/v/dev/documentation/metadata)) – *RiverBench also includes metadata in Jelly for benchmark tasks, datasets, and more.*

You can find some more interesting datasets in the Jelly format on the [RiverBench website](https://w3id.org/riverbench/dev/datasets).

## Commercial support

**[NeverBlink](https://neverblink.eu)** provides commercial support services for Jelly, including implementing custom features, system integrations, implementations for new languages, benchmarking, and more.

## See also

- [User guide](user-guide.md)
- [Licensing and citation](licensing/index.md)
