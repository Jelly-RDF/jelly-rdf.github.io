# Applications using Jelly

**If you are using Jelly in your project, we would be glad to list it here! Please [open an issue](https://github.com/Jelly-RDF/jelly-rdf.github.io/issues/new/choose) or [open a pull request](https://github.com/Jelly-RDF/jelly-rdf.github.io/edit/main/docs/use-cases.md) with the information on your use case.**

## Jelly-JVM

- [RiverBench](https://w3id.org/riverbench) benchmark suite.
    - Jelly is used as [one of the serialization formats](https://w3id.org/riverbench/v/dev/documentation/dataset-release-format) for distributing datasets in RiverBench.
    - Jelly is also used for [distributing the RDF metadata](https://w3id.org/riverbench/v/dev/documentation/metadata) of benchmark datasets, tasks, and other resources.
    - This is implemented in the [ci-worker](https://github.com/RiverBench/ci-worker) application – a Scala 3 program making heavy use of [Jelly-JVM's]({{ jvm_link() }}) streaming capabilities.
- [Jelly-JVM benchmark code](https://github.com/Jelly-RDF/jvm-benchmarks). This code was used to produce the results seen on the [performance page](performance/index.md).
- [RDF Stream Taxonomy (RDF-STaX)](https://w3id.org/stax) uses Jelly for distributing the RDF-STaX ontology and the living literature review of RDF streaming.
    - This is implemented using Apache Jena's RIOT command-line utility and [Jelly-JVM's Jena plugin]({{ jvm_link('getting-started-plugins') }}). Source code: [GitHub](https://github.com/RDF-STaX/ci-worker).
- *Not released publicly yet – stay tuned!* A Scala 2 application using Jelly over Kafka, MQTT, and gRPC (full streaming protocol).

## Example datasets in the Jelly format

Below listed are some example datasets available in the Jelly format. All of these are in the [delimited format](user-guide.md#delimited-vs-non-delimited-jelly). The licenses for these datasets are specified on the linked documentation pages.

- Large datasets (millions of triples/quads):
    - [:octicons-download-24: ASSIST-IoT weather measurements](https://w3id.org/riverbench/datasets/assist-iot-weather/1.0.3/files/jelly_full.jelly.gz) ([documentation](https://w3id.org/riverbench/datasets/assist-iot-weather/1.0.3)) – 80 million triples.
    - [:octicons-download-24: 5 million nanopublications](https://w3id.org/riverbench/datasets/nanopubs/1.0.3/files/jelly_full.jelly.gz) ([documentation](https://w3id.org/riverbench/datasets/nanopubs/1.0.3)) – 171 million quads.
    - [:octicons-download-24: RDF-star annotated facts from YAGO](https://w3id.org/riverbench/datasets/yago-annotated-facts/1.0.3/files/jelly_full.jelly.gz) ([documentation](https://w3id.org/riverbench/datasets/yago-annotated-facts/1.0.3)) – 2 million triples.

- Small datasets:
    - [:octicons-download-24: RDF-STaX ontology](https://w3id.org/stax/1.1.3/ontology.jelly) ([documentation](https://w3id.org/stax/1.1.3/ontology)).
    - [:octicons-download-24: RiverBench suite metadata](https://w3id.org/riverbench/v/dev.jelly) ([documentation](https://w3id.org/riverbench/v/dev/documentation/metadata)) – *RiverBench also includes metadata in Jelly for benchmark tasks, datasets, and more.*

You can find more interesting datasets in the Jelly format on the [RiverBench website](https://w3id.org/riverbench/dev/datasets).

## See also

- [User guide](user-guide.md)
- [Licensing and citation](licensing.md)
