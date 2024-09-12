# Applications using Jelly

**If you are using Jelly in your project, we would be glad to list it here! Please [open an issue](https://github.com/Jelly-RDF/jelly-rdf.github.io/issues/new/choose) or [open a pull request](https://github.com/Jelly-RDF/jelly-rdf.github.io/edit/main/docs/use-cases.md) with the information on your use case.**

## Jelly-JVM

- [RiverBench](https://w3id.org/riverbench) benchmark suite.
    - Jelly is used as [one of the serialization formats](https://w3id.org/riverbench/v/dev/documentation/dataset-release-format) for distributing datasets in RiverBench.
    - Jelly is also used for [distributing the RDF metadata](https://w3id.org/riverbench/v/dev/documentation/metadata) of benchmark datasets, tasks, and other resources.
    - This is implemented in the [ci-worker](https://github.com/RiverBench/ci-worker) application – a Scala 3 program making heavy use of [Jelly-JVM's]({{ jvm_link() }}) streaming capabilities.
- [Jelly-JVM benchmark code](https://github.com/Jelly-RDF/jvm-benchmarks). This code was used to produce the results seen on the [performance page](performance.md).
- *Not released publicly yet – stay tuned!* A Scala 2 application using Jelly over Kafka, MQTT, and gRPC (full streaming protocol). 

## See also

- [User guide](user-guide.md)
- [Licensing and citation](licensing.md)
