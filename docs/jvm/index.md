# Jelly JVM (Scala) implementation

**Jelly JVM** is an implementation of the Jelly serialization format and the gRPC streaming protocol for the Java Virtual Machine (JVM), written in Scala 3. The supported RDF libraries are [Apache Jena](https://jena.apache.org/) and [Eclipse RDF4J](https://rdf4j.org/).

This collection of libraries aims to provide the full stack of utilities for fast and scalable RDF streaming with the [Jelly protocol](../specification/index.md).

!!! tip "Getting started"

    See the **[Getting started guide](getting-started.md)** for a quick introduction to the Jelly JVM implementation.

## Library modules

The implementation is split into a few modules that can be used separately:

- `jelly-core` – implementation of the [Jelly serialization format](../specification/serialization.md) (using the [scalapb](https://scalapb.github.io/) library), along with generic utilities for converting the deserialized RDF data to/from the representations of RDF libraries (like Apache Jena or RDF4J). 
    - [![jelly-core Scala version support](https://index.scala-lang.org/jelly-rdf/jelly-jvm/jelly-core/latest.svg)](https://index.scala-lang.org/jelly-rdf/jelly-jvm/jelly-core) [![javadoc](https://javadoc.io/badge2/eu.ostrzyciel.jelly/jelly-core_3/javadoc.svg)](https://javadoc.io/doc/eu.ostrzyciel.jelly/jelly-core_3) 

- `jelly-jena` – conversions and interop code for the [Apache Jena](https://jena.apache.org/) library.
    - [![jelly-jena Scala version support](https://index.scala-lang.org/jelly-rdf/jelly-jvm/jelly-jena/latest.svg)](https://index.scala-lang.org/jelly-rdf/jelly-jvm/jelly-jena) [![javadoc](https://javadoc.io/badge2/eu.ostrzyciel.jelly/jelly-jena_3/javadoc.svg)](https://javadoc.io/doc/eu.ostrzyciel.jelly/jelly-jena_3)

- `jelly-rdf4j` – conversions and interop code for the [RDF4J](https://rdf4j.org/) library.
    - [![jelly-rdf4j Scala version support](https://index.scala-lang.org/jelly-rdf/jelly-jvm/jelly-rdf4j/latest.svg)](https://index.scala-lang.org/jelly-rdf/jelly-jvm/jelly-rdf4j) [![javadoc](https://javadoc.io/badge2/eu.ostrzyciel.jelly/jelly-rdf4j_3/javadoc.svg)](https://javadoc.io/doc/eu.ostrzyciel.jelly/jelly-rdf4j_3)

- `jelly-stream` – utilities for building [Reactive Streams](https://www.reactive-streams.org/) of RDF data (based on Pekko Streams). Useful for integrating with gRPC or other streaming protocols (e.g., Kafka, MQTT).
    - [![jelly-stream Scala version support](https://index.scala-lang.org/jelly-rdf/jelly-jvm/jelly-stream/latest.svg)](https://index.scala-lang.org/jelly-rdf/jelly-jvm/jelly-stream) [![javadoc](https://javadoc.io/badge2/eu.ostrzyciel.jelly/jelly-stream_3/javadoc.svg)](https://javadoc.io/doc/eu.ostrzyciel.jelly/jelly-stream_3)

- `jelly-grpc` – implementation of a gRPC client and server for the [Jelly gRPC streaming protocol](../specification/streaming.md).
    - [![jelly-grpc Scala version support](https://index.scala-lang.org/jelly-rdf/jelly-jvm/jelly-grpc/latest.svg)](https://index.scala-lang.org/jelly-rdf/jelly-jvm/jelly-grpc) [![javadoc](https://javadoc.io/badge2/eu.ostrzyciel.jelly/jelly-grpc_3/javadoc.svg)](https://javadoc.io/doc/eu.ostrzyciel.jelly/jelly-grpc_3)

## Compatibility

The Jelly JVM implementation is compatible with Java 11 and newer. Java 11, 17, and 21 are tested in CI and are guaranteed to work.

The following table shows the compatibility of the Jelly JVM implementation with other libraries:

| Jelly | Scala | Java | RDF4J | Apache Jena | Apache Pekko |
| ----- | ----- | ---- | ----- | ----------- | ------------ |
| 1.0.x | 3.3.1 | 11–21| 4.x   | 4.x         | 1.x          |

## Documentation

Below is a list of all documentation pages about Jelly JVM. You can also browse the Javadoc using the badges in the module list above. The documentation uses examples written in Scala, but the libraries can be used from Java as well.

- [Getting started](getting-started.md)
- User guide
    - [Apache Jena integration](jena.md)
    - [RDF4J integration](rdf4j.md)
    - [Reactive streaming](reactive.md)
    - [gRPC](grpc.md)
- Developer guide
    - [Releases](releases.md)
    - [Implementing Jelly for other libraries](implementing.md)
