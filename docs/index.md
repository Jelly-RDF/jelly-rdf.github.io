![Jelly (superfast jellyfish)](assets/jelly_color.png){ align=right width="150" }

# Jelly

**Jelly** is a high-performance binary serialization format and streaming protocol for [RDF](https://en.wikipedia.org/wiki/Resource_Description_Framework). It is based on [Protocol Buffers](https://protobuf.dev/) and [gRPC](https://grpc.io/), and has a JVM implementation that works with [Apache Jena](https://jena.apache.org/) and [RDF4J](https://rdf4j.org/).

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

    Everything is open-source and well-documented to help you get started

    [:octicons-arrow-right-24: Protocol specification](specification/index.md)

</div>

## How fast is it?

*Fast.* Jelly was specifically designed to serialize and deserialize streams of RDF data faster than N-Triples or other binary formats, while being [more compact than Turtle](performance/index.md#grouped-streaming-serialized-size).

The benchmarks below were performed on streams of RDF graphs or datasets, but Jelly is also good at handling streams of triples or quads ("classic" serialization). The benchmark was performed with Jelly-JVM 2.2.2 with Apache Jena 5.2.0. See: **[more benchmark results and details about the benchmark setup](performance/index.md)**.

<figure markdown="span">
  ![Serialization speed bar plot](assets/benchmarks/grouped_ser.png){ width="100%" }
  <figcaption markdown style="max-width: 100%;">Serialization speed of a stream of RDF graphs or RDF datasets, averaged over 13 datasets (RiverBench 2.1.0 profile [`stream-mixed-rdfstar`](https://w3id.org/riverbench/v/2.1.0/profiles/stream-mixed-rdfstar), task [`stream-serialization-throughput`](https://w3id.org/riverbench/v/2.1.0/tasks/stream-serialization-throughput)).<br>* Partial results for RDF/XML and JSON-LD (some datasets not supported).<br>[More details about the benchmark](performance/index.md).</figcaption>
</figure>

<figure markdown="span">
  ![Deserialization speed bar plot](assets/benchmarks/grouped_des.png){ width="100%" }
  <figcaption markdown style="max-width: 100%;">Deserialization (parsing) speed of a stream of RDF graphs or RDF datasets, averaged over 13 datasets (RiverBench 2.1.0 profile [`stream-mixed-rdfstar`](https://w3id.org/riverbench/v/2.1.0/profiles/stream-mixed-rdfstar), task [`stream-deserialization-throughput`](https://w3id.org/riverbench/v/2.1.0/tasks/stream-deserialization-throughput)).<br>* Partial results for RDF/XML and JSON-LD (some datasets not supported).<br>[More details about the benchmark](performance/index.md).</figcaption>
</figure>

## See also

- **[User guide](user-guide.md)**
- **[Performance benchmarks](performance/index.md)**
- **[Protocol specification](specification/index.md)**
- **[Contributing to Jelly](contributing.md)**
- **Code on GitHub:** [protocol definition](https://github.com/Jelly-RDF/jelly-protobuf), [JVM implementation](https://github.com/Jelly-RDF/jelly-jvm), [website](https://github.com/Jelly-RDF/jelly-rdf.github.io)
- **[Licensing and citation](licensing.md)**
