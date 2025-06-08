# Jelly user guide

Jelly uses [Protocol Buffers 3](https://protobuf.dev/programming-guides/proto3/) as the basis of its serialization. You can also use an existing implementation, such as the [JVM implementation]({{ jvm_link() }}), or you can quickly [create a new Jelly implementation using code generation](#implementing-jelly). 

## What can it do?

Jelly is designed to be a protocol for *streaming* RDF knowledge graphs, but it can also be used with "classic", static RDF. The main design goals of Jelly are speed, simplicity, and wide coverage of use cases. 

- Jelly can work with **any RDF knowledge graph data**, including RDF 1.1, RDF-star, and generalized RDF.
- Jelly can be used to represent **streams of triples, quads, graphs, or datasets**.
- Jelly can also be used to represent a **single graph or dataset**.
- Jelly can be used for **streaming data over the network** (e.g., with MQTT, Kafka, gRPC), but also for **working with flat files**.
- Jelly can **compress RDF data on the fly**, without having to know the data in advance.
- Jelly is super-fast and lightweight, scaling both down to **embedded devices** and up to **high-performance servers**.

## Quick start

### [CLI tool](https://github.com/Jelly-RDF/cli)

The easiest way to do something with Jelly is with the `jelly-cli` command line tool.

1. Go to the [`jelly-cli` download page](https://github.com/Jelly-RDF/cli/releases/tag/dev) and download a binary for you platform.
    - Alternatively, you can download the `jelly-cli.jar` file and run it with `java -jar jelly-cli.jar`.
2. Run `./jelly-cli rdf to-jelly some-rdf-file.ttl > output.jelly` to convert an RDF file to Jelly.
3. Run `./jelly-cli rdf from-jelly output.jelly` to convert the Jelly file back to RDF.
4. Run `./jelly-cli --help` to see all available commands.

You can find more information about the tool in **[its README on GitHub](https://github.com/Jelly-RDF/cli)**.

!!! example "Do you have any example Jelly files to experiment with?"

    Yes! Go check out the **[Use cases page](use-cases.md#example-datasets-in-the-jelly-format)** where we list links to example datasets in the Jelly format.

### Apache Jena / RDF4J plugins

Check out the **[dedicated guide for installing plugins in Jena and RDF4J]({{ jvm_link('getting-started-plugins') }})**. You can use them to quickly add Jelly support to, for example, Apache Jena Fuseki and load Jelly files just like any other RDF file.

### Java & Scala programming

Go see the **[Jelly-JVM getting started guide for devs]({{ jvm_link('getting-started-devs') }})**. It contains a lot of examples and code snippets for using Jelly in Java and Scala, with Jena, RDF4J, and Titanium.

### Python programming

See the **[pyjelly getting started guide]({{ python_link('getting-started') }})**. It contains examples and code snippets for using Jelly with rdflib.

## How to use it – in detail

To use Jelly you firstly need an implementation of the protocol. There is currently one implementation available: **[Jelly-JVM]({{ jvm_link() }})**, which supports [Apache Jena](https://jena.apache.org/), [Eclipse RDF4J](https://rdf4j.org/), and the [Titanium RDF API](https://github.com/filip26/titanium-rdf-api). It also has support for reactive streams (via Pekko Streams) and gRPC.

The implementation will support several stream types and patterns that you can use. Which stream type you choose depends on your use case (see [stream types](#stream-types) below).

All stream types use the same concept of **stream frames** – discrete elements into which the stream is divided. Each frame contains a number of **rows**, which are the actual RDF data (RDF triples, quads, etc.). Jelly does not enforce the semantics of stream frames, although it does have a mechanism to suggest to consumers and producers how should they understand the stream. Still, you can interpret the stream however you like.

!!! question "Why doesn't Jelly enforce the semantics of stream frames?"

    There are many, many ways in which streams of RDF data can be used – there are different use cases, network protocols, QoS settings, ordering guarantees, stream semantics, etc. One stream is also often viewed from different perspectives by the different actors producing and consuming it. Picking and enforcing specific semantics for stream frames would hopelessly overcomplicate the protocol and make it less useful in some use cases.

    Jelly does have a system of **logical stream types** based on the RDF Stream Taxonomy ([RDF-STaX](https://w3id.org/stax)), which can be used to suggest how the stream should be interpreted. However, these are just suggestions – you can interpret the stream however you like.

### Stream types

Jelly has the notions of **physical stream types** and **logical stream types**. The physical type tells you how Jelly sends the data on the wire, which is a technical detail. The logical type tells you how you should interpret the stream. Specifying the logical type is optional and is only a suggestion to the consumer. You can **always** interpret the stream however you like.

There are three physical stream types in Jelly:

- **`TRIPLES`**: Data is encoded using triple statements. There is no information about the graph name in this type of stream.
- **`QUADS`**: Data is encoded using quad statements. Each quad has a graph name, which can also be the default graph.
- **`GRAPHS`**: Data is encoded using named graphs, where the graph name can also be the default graph. Each named graph can contain multiple triples.

As for logical stream types, they are taken directly from [RDF-STaX]({{ stax_link('taxonomy') }}) – see the RDF-STaX website for a complete list of them. The following table summarizes which physical stream types may be used for each logical stream type. Please note that the table covers only the cases that are directly supported by the [Jelly protocol specification](specification/index.md) and its official implementations.

| RDF-STaX (logical type) / Physical type | `TRIPLES` | `QUADS` | `GRAPHS` |
|:--|:-:|:-:|:-:|
| [Graph stream]({{ stax_link('taxonomy#rdf-graph-stream') }}) | Framed | ✘ | ✘ |
| [Subject graph stream]({{ stax_link('taxonomy#rdf-subject-graph-stream') }}) | Framed | ✘ | ✘ |
| [Dataset stream]({{ stax_link('taxonomy#rdf-dataset-stream') }}) | ✘ | Framed | Framed |
| [Named graph stream]({{ stax_link('taxonomy#rdf-named-graph-stream') }}) | ✘ | Framed | Framed |
| [Timestamped named graph stream]({{ stax_link('taxonomy#timestamped-rdf-named-graph-stream') }}) | ✘ | Framed | Framed |
| [Flat triple stream]({{ stax_link('taxonomy#flat-rdf-triple-stream') }}) | Continuous | ✘ | ✘ |
| [Flat quad stream]({{ stax_link('taxonomy#flat-rdf-quad-stream') }}) | ✘ | Continuous | Continuous |


The values in the table mean the following:

- **Framed**: Each stream frame corresponds to exactly one logical element of the stream type. For example, in a graph stream, each frame corresponds to a single RDF graph. This usage pattern is common in real-time streaming scenarios like IoT systems.
- **Continuous**: The stream is a continuous sequence of logical elements. For example, in a flat triple stream, the stream is just a sequence of triples.
- **✘**: The physical stream type is not directly supported for the logical stream type. However, you may still find a way to use it, depending on your use case.

The flat logical stream types ([flat RDF triple stream]({{ stax_link('taxonomy#flat-rdf-triple-stream') }}) and [flat RDF quad stream]({{ stax_link('taxonomy#flat-rdf-quad-stream') }}) in RDF-STaX) can also be treated as a single RDF graph or RDF dataset, respectively.

### Common patterns cookbook

Below you will find some common patterns for using Jelly. These are just examples – you can use Jelly in many other ways. All of the presented patterns are supported in the [Jelly-JVM implementation]( {{ jvm_link('user/reactive') }}) with the Reactive Streaming module.

#### Flat RDF triple stream – "just a bunch of triples"

Let's say you want to stream a lot of triples from A to B – maybe you're doing some kind of data migration, or you're sending data to a data lake. You don't care about the graph they belong to – you just want to send a bunch of triples.

This means you are using logically a [flat RDF triple stream]({{ stax_link('taxonomy#flat-rdf-triple-stream') }}). It can be physically encoded as as `TRIPLES` stream, batching the triples into frames of an arbitrary size (let's say, 1000 triples each):

??? example "Example (click to expand)"

    - Stream frame 1
        - Stream options
        - Triple 1
        - Triple 2
        - ...
        - Triple 1000
    - Stream frame 2
        - Triple 1001
        - Triple 1002
        - ...
        - Triple 2000
    - ...

You can then send these frames one-by-one over gRPC or Kafka, or write them to a file. The consumer will be able to read the triples one frame at a time, without having to know how many triples there are in total.

#### RDF graph stream

In this case we have (for example) an IoT sensor that periodically emits an RDF graph that describes what the sensor saw (something like [SOSA/SSN](https://www.w3.org/TR/vocab-ssn/)). The graphs may be of different sizes (depending on what the sensor saw) and they can be emitted at different rates (depending on how often the sensor is triggered). We want to stream these graphs to a server that will process them in real-time with no additional latency.

This means you are using logically an [RDF graph stream]({{ stax_link('taxonomy#rdf-graph-stream') }}). You can encode it as a `TRIPLES` stream, where the stream frames correspond to different unnamed (default) graphs:

??? example "Example (click to expand)"

    - Stream frame 1
        - Stream options
        - Triple 1 (of graph 1)
        - Triple 2 (of graph 1)
        - ...
        - Triple 134 (of graph 1)
    - Stream frame 2
        - Triple 1 (of graph 2)
        - Triple 2 (of graph 2)
        - ...
        - Triple 97 (of graph 2)
    - ...

The consumer will be able to read the graphs one frame at a time, without having to know how many graphs there are in total.

[RiverBench](http://w3id.org/riverbench) uses this pattern for distributing its triple streams (see [example](https://w3id.org/riverbench/datasets/lod-katrina/dev)). Note that in RiverBench the stream may be equivalently considered "just a bunch of triples" – the serialization is the same, it only depends on the interpretation on the side of the consumer.

#### Flat RDF quad stream – "just a bunch of quads"

You want to stream a lot of quads – similar to the "just a bunch of triples" case above, but you also want to include the graph node. This is logically a [flat RDF quad stream]({{ stax_link('taxonomy#flat-rdf-quad-stream') }}). It can be physically encoded as a `QUADS` stream, batching the quads into frames of an arbitrary size (let's say, 1000 quads each):

??? example "Example (click to expand)"

    - Stream frame 1
        - Stream options
        - Quad 1
        - Quad 2
        - ...
        - Quad 1000
    - Stream frame 2
        - Quad 1001
        - Quad 1002
        - ...
        - Quad 2000
    - ...

The mechanism is exactly the same as with a flat RDF triple stream.

#### Flat RDF quad stream (as `GRAPHS`)

This a slightly different take on the problem of "just a bunch of quads" – you also want to transmit what is essentially a single RDF dataset, but instead of sending individual quads, you want to send it graph-by-graph. This makes most sense if your data changes on a per-graph basis, or you are streaming a static RDF dataset.

This is logically again a flat RDF quad stream, but it can be physically encoded as a `GRAPHS` stream, batching the triples in the graphs into frames of an arbitrary size (let's say, 1000 triples each):

??? example "Example (click to expand)"

    - Stream frame 1
        - Stream options
        - Start graph (named 1)
        - Triple 1 (of graph 1)
        - Triple 2 (of graph 1)
        - ...
        - Triple 134 (of graph 1)
        - End graph
        - Start graph (named 2)
        - Triple 1 (of graph 2)
        - Triple 2 (of graph 2)
        - ...
        - Triple 97 (of graph 2)
    - Stream frame 2
        - Triple 98 (of graph 2)
        - ...
        - Triple 130 (of graph 2)
        - End graph
        - Start graph (named 3)
        - Triple 1 (of graph 3)
        - Triple 2 (of graph 3)
        - ...
        - Triple 77 (of graph 3)
        - End graph
        - Start graph (named 4)
        - Triple 1 (of graph 4)
        - Triple 2 (of graph 4)
        - ...
        - Triple 21 (of graph 4)
        - End graph
    - ...

Notice that one named graph can span multiple stream frames, and one stream frame can contain multiple graphs. The consumer will be able to read the graphs one frame at a time, without having to know how many graphs there are in total.

#### RDF dataset stream (as `QUADS`)

You want to stream RDF datasets – similar to the "a stream of graphs" case above, but your elements are entire datasets. This is logically an [RDF dataset stream]({{ stax_link('taxonomy#rdf-dataset-stream') }}), which can be physically encoded as a `QUADS` stream, where the stream frames correspond to different datasets:

??? example "Example (click to expand)"

    - Stream frame 1
        - Stream options
        - Quad 1 (of dataset 1)
        - Quad 2 (of dataset 1)
        - ...
        - Quad 454 (of dataset 1)
    - Stream frame 2
        - Quad 1 (of dataset 2)
        - Quad 2 (of dataset 2)
        - ...
        - Quad 323 (of dataset 2)
    - ...

The mechanism is exactly the same as with a triple stream of graphs.

[RiverBench](http://w3id.org/riverbench) uses this pattern for distributing its RDF dataset streams (see [example](https://w3id.org/riverbench/datasets/nanopubs/dev)). Note that in RiverBench the stream may be equivalently considered a flat RDF quad stream – the serialization is the same, it only depends on the interpretation on the side of the consumer.

#### RDF dataset stream (as `GRAPHS`)

You want to stream RDF datasets or a subclass of them – for example [timestamped named graphs]({{ stax_link('taxonomy#timestamped-rdf-named-graph-stream') }}), using the [RSP Data Model](https://streamreasoning.org/RSP-QL/Abstract%20Syntax%20and%20Semantics%20Document/), where each stream element is a named graph and a bunch of statements about this graph in the default graph. This can be physically encoded as a `GRAPHS` stream, where the stream frames correspond to different datasets:

??? example "Example (click to expand)"

    - Stream frame 1
        - Stream options
        - Start graph (default)
        - Triple 1 (of default graph, dataset 1)
        - Triple 2 (of default graph, dataset 1)
        - ...
        - Triple 134 (of default graph, dataset 1)
        - End graph
        - Start graph (named)
        - Triple 1 (of named graph, dataset 1)
        - Triple 2 (of named graph, dataset 1)
        - ...
        - Triple 97 (of named graph, dataset 1)
        - End graph
    - Stream frame 2
        - Start graph (default)
        - Triple 1 (of default graph, dataset 2)
        - Triple 2 (of default graph, dataset 2)
        - ...
        - Triple 77 (of default graph, dataset 2)
        - End graph
        - Start graph (named)
        - Triple 1 (of named graph, dataset 2)
        - Triple 2 (of named graph, dataset 2)
        - ...
        - Triple 21 (of named graph, dataset 2)
        - End graph
    - ...

Of course each stream frame could contain more than one named graph, and the graphs can be of different sizes.

## Ordering and delivery guarantees

To be able to compress RDF streams on-the-fly, Jelly requires that stream frames are kept strictly in order (see also [the spec](specification/serialization.md#ordering)). This is because the compression algorithm updates its lookup tables dynamically over the course of the stream, and a given frame depends on the lookups defined in previous frames. If the frames are out of order, the compression may fail.

There are use cases where it's hard to guarantee strict ordering of messages, such as IoT messaging (e.g., MQTT with QoS 0) or high-throughput streams with parallel partitions (e.g., Kafka). In these cases you may want to employ one of these strategies:

- **Emit shared lookup tables at the start of the stream**: If you know the vocabulary of the stream, you can emit most of the content of the lookup tables at the start of the stream, and then only update the lookup elements that vary frame-to-frame, keeping the updates local to the frame. This strategy is especially useful in IoT scenarios, where the vocabulary is usually known in advance. You don't need to modify the consumer in this case.
    - A variation of this strategy is to communicate the lookup tables over a separate channel before starting the stream. This is useful if you can't guarantee that the lookup tables will be delivered before the stream frames.
- **Use a "frame ID" to keep track of the order**: If you can't guarantee the order of the frames, you can add a "frame ID" to each frame, which will allow the consumer to reorder the frames before processing them. This strategy is useful in high-throughput scenarios, where you can't guarantee the order of the frames. You will need to modify the consumer to reorder the frames before processing them. However, handling failures in this scenario may be complicated.
- **Use partitions that are guaranteed to be in-order**: If you can't guarantee the order of the frames, you can use partitions that are guaranteed to be in-order (e.g., Kafka partitions). Then, each partition should have its own set of lookups (essentially treating each partition as a separate stream in Jelly's terms). This strategy is useful in high-throughput scenarios.

Note that Jelly by default also assumes that frames are delivered at least once. At-least-once delivery is good enough (as long as the order is kept), as lookup updates are idempotent – you may only need to de-duplicate the frames afterwards. At-most-once delivery requires you to make the frames independent of each other, such as with the IoT strategy above.

## Delimited vs. non-delimited Jelly

Protobuf messages by default [are not delimited](https://protobuf.dev/programming-guides/techniques/#streaming). This means that when you serialize a Protobuf message (e.g., a Jelly stream frame), the serialization does not include any information about where the message ends. This is fine when there is something else telling the parser where the message ends – for example, when you're sending the message over a gRPC, Kafka, or MQTT stream, the streaming protocol tells the parser how long the message is. However, if you wanted to write multiple stream frames to a file, you would need to add some kind of delimiter between the frames – otherwise the parser would not know where one frame ends and the next one begins.

So, to summarize:

| Use case | Jelly variant | Description |
|:--|:--|:--|
| Jelly gRPC streaming protocol | Non-delimited | The gRPC protocol tells the parser how long the message is. |
| Streaming with Kafka, MQTT, or similar | Non-delimited | The streaming protocol tells the parser how long the message is. |
| Writing to a file | Delimited | You need to add a delimiter between the frames. |
| Writing to a raw network socket | Delimited | You need to add a delimiter between the frames. |

The delimited variant works by adding an integer before the stream frame that specifies the length of the frame, in bytes. That's it.

You can read more about how this works in the [serialization format specification](specification/serialization.md#delimited-variant-of-jelly).

### Examples

- [Jelly-JVM]({{ jvm_link() }}) supports both variants, but uses them in different contexts. When writing to a Java byte stream (typically a file) with Apache Jena RIOT or RDF4J Rio, the delimited variant is used. However, the RIOT/Rio integrations can parse either delimited or non-delimited Jelly data. In the gRPC protocol, the non-delimited variant is used.
- [RiverBench](http://w3id.org/riverbench) publishes its RDF metadata and datasets as Jelly files. These files are always written using the delimited variant.

## Implementing Jelly

!!! note
    
    This section is intended only for those who want to write a new Jelly implementation from scratch. It's much easier to use an existing implementation, such as the [JVM implementation]({{ jvm_link() }}).

Implementing Jelly from scratch is greatly simplified by the existing Protobuf and RDF libraries. Essentially, the only thing you'll need to do is to glue them together:

- Find a Protobuf library for your language. You can find a list of official Protobuf implementations [here](https://protobuf.dev/reference/) and a list of community-maintained implementations [here](https://github.com/protocolbuffers/protobuf/blob/main/docs/third_party.md).
- Use the library to generate the code for the Jelly messages (this usually involves using `protoc`). You can find the Protobuf definitions in the [jelly-protobuf](https://github.com/Jelly-RDF/jelly-protobuf) repository.
- Find an RDF library for your language. You can find a list of RDF libraries [here](https://github.com/semantalytics/awesome-semantic-web#programming).
- Implement conversions to and/or from the RDF library's data structures. You can find an example of the conversion code in the [Jelly-JVM implementation](https://github.com/Jelly-RDF/jelly-jvm) (`core`, `jena`, and `rdf4j` modules).
- In the implementation follow the [specification](specification/index.md) to ensure compatibility.

That's it! You may also want to implement streaming facilities, such as [Reactive Streams](https://www.reactive-streams.org/) in Java/Scala. Implementing the [gRPC publish/subscribe mechanism](specification/streaming.md) follows a very similar procedure – many Protobuf libraries have built-in support for gRPC with code generation.

## See also

- [Jelly-JVM getting started guide]({{ jvm_link('getting-started-devs') }})
- [pyjelly getting started guide]({{ python_link('getting-started') }})
- [Applications using Jelly](use-cases.md)
