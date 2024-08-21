![Jelly (superfast jellyfish)](https://jelly-rdf.github.io/dev/assets/jelly_color.png){ align=right width="150" }

# Jelly

**Jelly** is a high-performance binary serialization format and streaming protocol for [RDF](https://en.wikipedia.org/wiki/Resource_Description_Framework). It is based on [Protocol Buffers](https://protobuf.dev/) and [gRPC]((https://grpc.io/)), and has a JVM implementation that works with [Apache Jena](https://jena.apache.org/) and [RDF4J](https://rdf4j.org/).

<div class="grid cards" style="clear: right;" markdown>

-   :material-clock-fast:{ .lg .middle } __Stream any RDF data, <u>fast</u>__

    ---

    Jelly is blazing-fast by design, and can work with streams of triples, graphs, datasets, and more

    [:octicons-arrow-right-24: Getting started](user-guide.md)

-   :fontawesome-solid-mug-hot:{ .lg .middle } __Robust JVM implementation__

    ---

    Fully-integrated support for Jelly in [Apache Jena](https://jena.apache.org/) and [RDF4J](https://rdf4j.org/) with maximum performance

    [:octicons-arrow-right-24: Jelly-JVM]({{ jvm_link() }})

-   :fontawesome-solid-angles-right:{ .lg .middle } __End-to-end streaming__

    ---

    Jelly comes with a [gRPC](https://grpc.io/) protocol and can work with Kafka, MQTT, and others

    [:octicons-arrow-right-24: User guide](user-guide.md)

    [:octicons-arrow-right-24: Streaming with Jelly-JVM]({{ jvm_link( 'user/reactive' ) }})

-   :fontawesome-solid-book:{ .lg .middle } __Open specification__

    ---

    Everything is open-source and well-documented, so you can build your own Jelly implementation

    [:octicons-arrow-right-24: Protocol specification](specification/index.md)

</div>

## How fast is it?

TODO

## See also

- **[User guide](user-guide.md)**
- **[Performance benchmarks](performance.md)**
- **[Protocol specification](specification/index.md)**
- **[Contributing to Jelly](contributing.md)**
- **Code on GitHub:** [protocol definition](https://github.com/Jelly-RDF/jelly-protobuf), [JVM implementation](https://github.com/Jelly-RDF/jelly-jvm), [website](https://github.com/Jelly-RDF/jelly-rdf.github.io)
- **[Licensing and citation](licensing.md)**
