# Jelly user guide

To use Jelly, pick an implementation that matches your tech stack:

- **[Jelly-JVM]({{ jvm_link() }})** – written in Java, integrated with Apache Jena, RDF4J, Titanium, and Neo4j.
- **[pyjelly]({{ python_link() }})** – written in Python, integrated with RDFLib. Can also be used without RDFLib.
- **[jelly_rs](https://github.com/Jelly-RDF/jelly_rs)** *(experimental)* – written in Rust, integrated with Sophia.
- **[jelly-cli](https://github.com/Jelly-RDF/cli)** – command-line tool, works on Windows, macOS, and Linux.

You can also [create your own implementation](#implementing-jelly). Because Jelly is built on top of [Protocol Buffers](https://protobuf.dev/), you can generate most of the code automatically in any popular programming language.

## What can it do?

Jelly is designed to be a protocol for *streaming* RDF knowledge graphs, but it can also be used with static RDF datasets. Jelly was designed to be fast, well-compressed, and versatile.

- Jelly can work with **any RDF knowledge graph data**, including RDF 1.1, RDF-star, and generalized RDF.
- Jelly can be used to represent **streams of triples, quads, graphs, or datasets**.
- Jelly can also be used to represent a **single graph or dataset**.
- Jelly-Patch can be used to [**record changes** to RDF datasets](specification/patch.md), including add/delete operations and transactions.
- Jelly can be used for **streaming data over the network** (e.g., with MQTT, Kafka, gRPC), but also for **working with flat files**.
- Jelly can **compress RDF data on the fly**, without having to know the data in advance.
- Jelly is super-fast and lightweight, scaling down to **IoT** and up to **high-performance servers**.

## Quick start

### [CLI tool](https://github.com/Jelly-RDF/cli)

The easiest way to do something with Jelly is with the [`jelly-cli`](https://github.com/Jelly-RDF/cli) command line tool.

For Linux, macOS, and WSL on Windows, install it with the following command:

```shell
. <(curl -sSfL https://w3id.org/jelly/setup-cli.sh)
jelly-cli
```

You can also install `jelly-cli` manually by downloading the [latest release](https://github.com/Jelly-RDF/cli/releases/latest), including a version for Windows without WSL and a platform-independent JAR file.


- Run `jelly-cli rdf to-jelly some-rdf-file.ttl > output.jelly` to convert an RDF file to Jelly.
- Run `jelly-cli rdf from-jelly output.jelly` to convert the Jelly file back to RDF.
- Run `jelly-cli --help` to see all available commands.

You can find more information about `jelly-cli` in **[its README on GitHub](https://github.com/Jelly-RDF/cli)**.

!!! example "Example Jelly files"

    Go check out the **[Use cases page](use-cases.md#example-datasets-in-the-jelly-format)** where we list links to example datasets in the Jelly format.

### Apache Jena / RDF4J plugins

Check out the **[dedicated guide for installing plugins in Jena and RDF4J]({{ jvm_link('getting-started-plugins') }})**. You can use them to quickly add Jelly support to, for example, Apache Jena Fuseki and load Jelly files just like any other RDF file.

### Neo4j plugin

We also have a plugin for Neo4j, extending the official neosemantics plugin. **[Check out installation instructions and usage guide.]({{ jvm_link('getting-started-neo4j') }})**

### Java & Scala programming

Go see the **[Jelly-JVM getting started guide for devs]({{ jvm_link('getting-started-devs') }})**. It contains a lot of examples and code snippets for using Jelly in Java and Scala, with Jena, RDF4J, and Titanium.

### Python programming

See the **[pyjelly getting started guide]({{ python_link('getting-started') }})**. It contains examples and code snippets for using Jelly with or without RDFLib, as well as other libraries like NetworkX.

## How does it work – encoding

RDF data consists of triples (subject, predicate, object) or quads (subject, predicate, object, graph name). We will use these three triples in the N-Triples format as a running example:

```turtle
<https://example.org/jelly> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> _:b1 .
<https://example.org/jelly> <https://example.org/label> "Jelly" .
_:b1 <https://example.org/label> "Serialization format"@en .
```

You can read that as "Jelly is an instance of a serialization format".

Jelly encodes a sequence of triples or quads as a binary stream, using efficient encoding. The first thing it does is splitting IRIs into prefixes and postfixes (we call postfixes "names"):

- Prefixes:
    - `[1]: https://example.org/`
    - `[2]: http://www.w3.org/1999/02/22-rdf-syntax-ns#`
- Names:
    - `[1]: jelly`
    - `[2]: type`
    - `[3]: label`

They are communicated in the stream as part of a dynamically changing lookup table. If we run out of IDs, we remove old entries in the lookup to free up space. Each prefix and name is assigned a numerical ID starting with 1. We can now efficiently construct IRIs as a pair of IDs (1st ID is the prefix, the 2nd ID is the name):

- `https://example.org/jelly` -> `RdfIri(1, 1)`
- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` -> `RdfIri(2, 2)`
- `https://example.org/label` -> `RdfIri(1, 3)`

This allows us to reuse repeating prefixes and names while saving on the serialized size. We also apply the same principle to datatype IRIs (they are not split in half, though). When we apply this across our 3 triples, we will get (in simplified form):

| Subject | Predicate | Object |
| ------- | --------- | ------ |
| `RdfIri(1, 1)` | `RdfIri(2, 2)` | `"b1"` |
| `RdfIri(1, 1)` | `RdfIri(1, 3)` | `RdfLiteral("Jelly")` |
| `"b1"` | `RdfIri(1, 3)` | `RdfLiteral("Serialization format", "en")` |

Notice that we have repeated IRIs in the first and second column. Jelly can compress that, by applying a method similar to Turtle's colons and semicolons, but a bit more general. If we have two consecutive triples/quads with the exact same subject, predicate, object, or graph name, we simply... don't write the repeated term:

| Subject | Predicate | Object |
| ------- | --------- | ------ |
| `RdfIri(1, 1)` | `RdfIri(2, 2)` | `"b1"` |
| *(empty)* | `RdfIri(1, 3)` | `RdfLiteral("Jelly")` |
| `"b1"` | *(empty)* | `RdfLiteral("Serialization format", "en")` |

Jelly parsers detect these missing values and automatically fill them in with values from previous rows. These empty terms take up exactly 0 bytes on the wire, which makes this method very efficient.

Jelly also applies a delta compression scheme to prefix and name IDs. [You can find the details in the spec](specification/serialization.md), but the short version is that we use `0` to indicate `previous + 1` ID in the case of names, and `previous` ID in the case of prefixes. For our triples, this allows us to replace all name IDs with zeroes:

| Subject | Predicate | Object |
| ------- | --------- | ------ |
| `RdfIri(1, 0)` | `RdfIri(2, 0)` | `"b1"` |
| *(empty)* | `RdfIri(1, 0)` | `RdfLiteral("Jelly")` |
| `"b1"` | *(empty)* | `RdfLiteral("Serialization format", "en")` |

The value of `0` takes up exactly zero bytes – that's the same trick as with repeated terms, allowing us to save even more space.

Jelly's encoding scheme was designed to work in a fully streaming manner. We can compress RDF data by only looking at one triple at a time, and we use a strictly limited amount of memory for that. **This allows Jelly to work with datasets of any size** – billions, trillions, and beyond.

That's the basics – [see the spec for details](specification/serialization.md).

??? example "Full translation of the example to Jelly"

    The running example was translated to a text-based readable version of Jelly with [jelly-cli](https://github.com/Jelly-RDF/cli):

    ```shell
    jelly-cli rdf to-jelly --opt.physical-type=triples | \
        jelly-cli rdf from-jelly --out-format jelly-text
    ```

    Output:

    ```json
    # Frame 0
    rows {
      options {
        physical_type: PHYSICAL_STREAM_TYPE_TRIPLES
        rdf_star: true
        max_name_table_size: 4000
        max_prefix_table_size: 150
        max_datatype_table_size: 32
        version: 1
      }
    }
    rows {
      prefix {
        value: "https://example.org/"
      }
    }
    rows {
      name {
        value: "jelly"
      }
    }
    rows {
      prefix {
        value: "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
      }
    }
    rows {
      name {
        value: "type"
      }
    }
    rows {
      quad {
        s_iri {
          prefix_id: 1
        }
        p_iri {
          prefix_id: 2
        }
        o_bnode: "b1"
        g_default_graph {
        }
      }
    }
    rows {
      name {
        value: "label"
      }
    }
    rows {
      quad {
        p_iri {
          prefix_id: 1
        }
        o_literal {
          lex: "Jelly"
        }
      }
    }
    rows {
      quad {
        s_bnode: "b1"
        o_literal {
          lex: "Serialization format"
          langtag: "en"
        }
      }
    }
    ```

### What Jelly does and does not compress

Jelly is pretty good at compressing IRI-heavy RDF data, but it doesn't compress the text in the IRIs themselves. Same applies to blank node identifiers, language tags, and literal contents. If you care about small file size, **you should compress your Jelly file with your compressor of choice**, like gzip, bzip, or zstd. We found zstd to work particularly well in practice. While Jelly by itself can make datasets ~6x smaller (this largely depends on the dataset), with zstd compression, you can sometimes get it up to 100x.

## How does it work – streams

A stream is just a sequence of items. We want to only look at one element of the stream at a time – this limits memory usage and allows us to process infinitely long streams.

The most basic kind of RDF stream is what you would see in an N-Triples or N-Quads file – after all, it's just a sequence of triples:

```turtle
<https://example.org/jelly> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> _:b1 .
<https://example.org/jelly> <https://example.org/label> "Jelly" .
_:b1 <https://example.org/label> "Serialization format"@en .
```

We call this a *flat RDF stream*. Jelly supports this kind of streams – you will find them useful in transferring large RDF files, query responses, database dumps, and so on.

But, what if our stream contains a sequence of RDF graphs or datasets? For example, if we want to transfer the measurements of a temperature sensor, we would have:

Graph 1:

```turtle
ex:sensor ex:measuredProperty ex:temperature ;
    ex:unit ex:Kelvin ;
    ex:value "280.4"^^xsd:decimal .
```

Graph 2:

```turtle
ex:sensor ex:measuredProperty ex:temperature ;
    ex:unit ex:Kelvin ;
    ex:value "280.6"^^xsd:decimal .
```

...and so on. In traditional RDF systems, you had two options. You could modify the data, wrap it in containers, or apply some other processing to make it fit into one graph. Or you could simply put each graph/dataset in a separate file. Jelly offers a simpler way, where multiple graphs or datasets can live within one file. We use *frames* as boundary markers:

```turtle
# Frame 1
ex:sensor ex:measuredProperty ex:temperature ;
    ex:unit ex:Kelvin ;
    ex:value "280.4"^^xsd:decimal .

# Frame 2
ex:sensor ex:measuredProperty ex:temperature ;
    ex:unit ex:Kelvin ;
    ex:value "280.6"^^xsd:decimal .
```

We call this a *grouped RDF stream*. A Jelly parser can unpack this and process the frames one by one. The best part is that the compression (explained [above](#how-does-it-work--encoding)) is applied **across the entire stream**. So, if an IRI appears in frame 1, and then again in frame 2, we will only have to write it only once. This is very effective for data with repeating patterns, like IoT measurements, nanopublications, encyclopedic entries, or maps (geography).

**As a summary:**

- **Flat RDF stream** – just a sequence of triples or quads. Great for processing a single file.
- **Grouped RDF stream** – a sequence of graphs or datasets. Great if you have many small files.

Jelly can record in its files whether the stream is flat or grouped, but this annotation is entirely optional, and parsers can ignore it. In fact, in both cases the physical layout of the stream is the same, only the interpretation of it changes.

The following sections contain more details about stream types in Jelly.

## Streams and stream types in detail

### Stream frames

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

!!! warning

    The `GRAPHS` type is a left-over from a previous version of the format and right now its usefulness is limited – you can do the exact same thing with `QUADS`, which is simpler. In new projects, we recommend using `QUADS` instead.

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
