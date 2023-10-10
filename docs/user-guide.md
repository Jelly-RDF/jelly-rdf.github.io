# Jelly user guide

**Jelly is a high-performance protocol for streaming and non-streaming RDF data. It is designed to be simple, fast, and easy to implement. This guide will help you get started with Jelly.**

Jelly uses [Protocol Buffers 3](https://protobuf.dev/programming-guides/proto3/) as the basis of its serialization. This means that you can quickly [create a new Jelly implementation using code generation](#implementing-jelly). You can also use an existing implementation, such as the [JVM (Scala) implementation](jvm/index.md).

## What can it do?

Jelly is designed to be a protocol for *streaming* RDF data, but it can also be used with "classic", static RDF data. The main design goals of Jelly are speed, simplicity, and wide coverage of use cases. 

- Jelly can work with **any RDF data**, including RDF-star, RDF 1.1, and generalized RDF.
- Jelly can be used to represent **streams of triples, quads, graphs, or datasets**.
- Jelly can also be used to represent a **single graph or dataset**.
- Jelly can be used for **streaming data over the network** (e.g., with MQTT, Kafka, gRPC), but also for **working with flat files**.
- Jelly can **compress RDF data on the fly**, without having to know the data in advance.
- Jelly is super-fast and lightweight, scaling both down to **embedded devices** and up to **high-performance servers**.

## How to use it?

To use Jelly you firstly need an implementation of the protocol. There is currently one implementation available: **[Jelly JVM (Scala)](jvm/index.md)**, which supports both [Apache Jena](https://jena.apache.org/) and [Eclipse RDF4J](https://rdf4j.org/). It also has support for reactive streams and gRPC.

The implementation will support several stream types and patterns that you can use. Which stream type you choose depends on your use case (see [stream types](#stream-types) below).

All stream types use the same concept of **stream frames** – discrete elements into which the stream is divided. Each frame contains a number of **rows**, which are the actual RDF data (RDF triples, quads, etc.). Jelly does not define the semantics of stream frames – it's up to you to decide what they mean (see examples below).

!!! question "Why doesn't Jelly define the semantics of stream frames?"

    There are many, many ways in which streams of RDF data can be used – there are different use cases, network protocols, QoS settings, ordering guarantees, stream semantics, etc. Picking specific semantics for stream frames would hopelessly overcomplicate the protocol and make it less useful in some use cases.

    Jelly tries to make as few assumptions as possible about the streams to ensure it is widely applicable. It is the responsibility of the end users to define the semantics of stream frames for their use case. To help with that, this user guide contains some common patterns and examples.

### Stream types

- **Triple stream**: A stream of triple statements. You can use it to represent:
    - A single unnamed RDF graph – stream frames are just batches of triples.
    - A stream of triple statements – stream frames are just batches of triples.
    - A stream of default (unnamed) RDF graphs – each stream frame corresponds to a different RDF graph.
- **Quad stream**: A stream of quad (triple with graph node) statements. You can use it to represent:
    - A single RDF dataset – stream frames are just batches of quads.
    - A stream of quad statements – stream frames are just batches of quads.
    - A stream of RDF datasets – each stream frame corresponds to a different RDF dataset.
- **Graph stream**: A stream of triples grouped into graphs (named or unnamed). You can use it to represent:
    - A single RDF dataset – stream frames are just batches of graphs (possibly partial graphs).
    - A stream of named RDF graphs – each stream frame corresponds to a different named graph.
    - A stream of RDF datasets – each stream frame corresponds to a different RDF dataset.

### Common patterns cookbook

Below you will find some common patterns for using Jelly. These are just examples – you can use Jelly in many other ways. All of the presented patterns are supported in the [Jelly JVM (Scala) implementation](jvm/reactive.md) with the Reactive Streaming module.

#### Triple stream – "just a bunch of triples"

Let's say you want to stream a lot of triples from A to B – maybe you're doing some kind of data migration, or you're sending data to a data lake. You don't care about the graph they belong to – you just want to send a bunch of triples.

You can use a triple stream, batching the triples into frames of an arbitrary size (let's say, 1000 triples each):

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

#### Triple stream – "a stream of graphs"

In this case we have an IoT sensor that periodically emits an RDF graph that describes what the sensor saw (something like [SOSA/SSN](https://www.w3.org/TR/vocab-ssn/)). The graphs may be of different sizes (depending on what the sensor saw) and they can be emitted at different rates (depending on how often the sensor is triggered). We want to stream these graphs to a server that will process them in real-time with no additional latency.

You can use a triple stream, where the stream frames correspond to different unnamed (default) graphs:

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

#### Quad stream – "just a bunch of quads"

You want to stream a lot of quads – similar to the "just a bunch of triples" case above, but you also want to include the graph node. You can use a quad stream, batching the quads into frames of an arbitrary size (let's say, 1000 quads each):

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

The mechanism is exactly the same as with a triple stream.

#### Quad stream – "a stream of datasets"

You want to stream RDF datasets – similar to the "a stream of graphs" case above, but your elements are entire datasets. You can use a quad stream, where the stream frames correspond to different datasets:

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

[RiverBench](http://w3id.org/riverbench) uses this pattern for distributing its quad and graph streams (see [example](https://w3id.org/riverbench/datasets/nanopubs/dev)). Note that in RiverBench the stream may be equivalently considered "just a bunch of quads" – the serialization is the same, it only depends on the interpretation on the side of the consumer.

#### Graph stream – "just a bunch of named graphs"

This a slightly different take on the problem of "just a bunch of quads" – you also want to transmit what is essentially an RDF dataset, but instead of sending individual quads, you want to send it graph-by-graph. This makes most sense if your data changes on a per-graph basis, or you are streaming a static RDF dataset.

You can use a graph stream, batching the triples in the graphs into frames of an arbitrary size (let's say, 1000 triples each):

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

Notice that one graph can span multiple stream frames, and one stream frame can contain multiple graphs. The consumer will be able to read the graphs one frame at a time, without having to know how many graphs there are in total.

#### Graph stream – "a stream of datasets"

You want to stream RDF datasets – for example using the [RSP Data Model](https://streamreasoning.org/RSP-QL/Abstract%20Syntax%20and%20Semantics%20Document/), where each element is a named graph and a bunch of statements about this graph in the default graph. You can use a graph stream, where the stream frames correspond to different datasets:

??? example "Example (click to expand)"

    - Stream frame 1
        - Stream options
        - Start graph (default)    
        - Triple 1 (of default graph)
        - Triple 2 (of default graph)
        - ...
        - Triple 134 (of default graph)
        - End graph
        - Start graph (named)
        - Triple 1 (of named graph)
        - Triple 2 (of named graph)
        - ...
        - Triple 97 (of named graph)
        - End graph
    - Stream frame 2
        - Start graph (default)
        - Triple 1 (of default graph)
        - Triple 2 (of default graph)
        - ...
        - Triple 77 (of default graph)
        - End graph
        - Start graph (named)
        - Triple 1 (of named graph)
        - Triple 2 (of named graph)
        - ...
        - Triple 21 (of named graph)
        - End graph
    - ...

Of course each stream frame can contain more than one named graph, and the graphs can be of different sizes.

## Ordering and delivery guarantees

To be able to compress RDF streams on-the-fly, Jelly requires that stream frames are kept strictly in order (see also [the spec](specification/serialization.md#ordering)). This is because the compression algorithm updates its lookup tables dynamically over the course of the stream, and a given frame depends on the lookups defined in previous frames. If the frames are out of order, the compression may fail.

There are use cases where it's hard to guarantee strict ordering of messages, such as IoT messaging (e.g., MQTT with QoS 0) or high-throughput streams with parallel partitions (e.g., Kafka). In these cases you may want to employ one of these strategies:

- **Emit shared lookup tables at the start of the stream**: If you know the vocabulary of the stream, you can emit most of the content of the lookup tables at the start of the stream, and then only update the lookup elements that vary frame-to-frame, keeping the updates local to the frame. This strategy is especially useful in IoT scenarios, where the vocabulary is usually known in advance. You don't need to modify the consumer in this case.
    - A variation of this strategy is to communicate the lookup tables over a separate channel before starting the stream. This is useful if you can't guarantee that the lookup tables will be delivered before the stream frames.
- **Use a "frame ID" to keep track of the order**: If you can't guarantee the order of the frames, you can add a "frame ID" to each frame, which will allow the consumer to reorder the frames before processing them. This strategy is useful in high-throughput scenarios, where you can't guarantee the order of the frames. You will need to modify the consumer to reorder the frames before processing them. However, handling failures in this scenario may be complicated.
- **Use partitions that are guaranteed to be in-order**: If you can't guarantee the order of the frames, you can use partitions that are guaranteed to be in-order (e.g., Kafka partitions). Then, each partition should have its own set of lookups (essentially treating each partition as a separate stream in Jelly's terms). This strategy is useful in high-throughput scenarios.

Note that Jelly by default also assumes that frames are delivered at least once. At-least-once delivery is good enough (as long as the order is kept), as lookup updates are idempotent – you may only need to de-duplicate the frames afterwards. At-most-once delivery requires you to make the frames independent of each other, such as with the IoT strategy above.

## Implementing Jelly

!!! note
    
    This section is intended only for those who want to write a new Jelly implementation from scratch. It's much easier to use an existing implementation, such as the [JVM (Scala) implementation](jvm/index.md).

Implementing Jelly from scratch is greatly simplified by the existing Protobuf and RDF libraries. Essentially, the only thing you'll need to do is to glue them together:

- Find a Protobuf library for your language. You can find a list of official Protobuf implementations [here](https://protobuf.dev/reference/) and a list of community-maintained implementations [here](https://github.com/protocolbuffers/protobuf/blob/main/docs/third_party.md).
- Use the library to generate the code for the Jelly messages (this usually involves using `protoc`). You can find the Protobuf definitions in the [jelly-protobuf](https://github.com/Jelly-RDF/jelly-protobuf) repository.
- Find an RDF library for your language. You can find a list of RDF libraries [here](https://github.com/semantalytics/awesome-semantic-web#programming).
- Implement conversions to and/or from the RDF library's data structures. You can find an example of the conversion code in the [Jelly JVM (Scala) implementation](https://github.com/Jelly-RDF/jelly-jvm) (`core`, `jena`, and `rdf4j` modules).
- In the implementation follow the [specification](specification/index.md) to ensure compatibility.

That's it! You may also want to implement streaming facilities, such as [Reactive Streams](https://www.reactive-streams.org/) in Java/Scala. Implementing the [gRPC publish/subscribe mechanism](specification/streaming.md) follows a very similar procedure – many Protobuf libraries have built-in support for gRPC with code generation.
