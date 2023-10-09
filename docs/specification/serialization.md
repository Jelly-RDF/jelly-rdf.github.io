# Jelly serialization format

TODO: intro, reference to RDF 1.1 and RDF-star, link to the proto reference, status of this spec

define consumer, producer

examples: https://protobuf.dev/reference/protobuf/textformat-spec/

UTF-8

!!! info

    The key words "MUST", "MUST NOT", "REQUIRED", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

!!! note

    The "Note" blocks in this document are not part of the specification, but rather provide additional information for implementers.

## Conformance

Implementations MAY choose to implement only a subset of the following specification. In this case, they SHOULD clearly specify which parts of the specification they implement. In the rest of this specification, the keywords "MUST", "MUST NOT", etc. refer to full (not partial) implementations.

!!! note

    Implementations may in particular choose to not implement features that are not supported on the target platform (e.g., RDF datasets, RDF-star, generalized RDF terms, etc.).

Implementations MAY also choose to extend Jelly with additional features that SHOULD NOT interfere with the serialization being readable by implementations which follow the specification.

## Versioning

The protocol follows the [Semantic Versioning 2.0](https://semver.org/) scheme. 

!!! note
    
    Releases of the protocol are published on [GitHub](https://github.com/Jelly-RDF/jelly-protobuf/releases).

### Backward compatibility

Implementations SHOULD ensure backward compatibility. To achieve backward compatibility, the implementation MUST be able to read all messages from the previous releases of the protocol with the same MAJOR version. The implementation MAY also be able to read messages from previous releases of the protocol with a different MAJOR version.

!!! note

    The protocol is designed in such a way that you don't need to worry about backward compatibility. The only thing you need to do is to implement the latest version of the protocol, and you will automatically get backward compatibility with all previous versions (of the same MAJOR).

### Forward compatibility

Forward compatibility is not guaranteed. Implementations MAY be able to read messages from future releases of the protocol with the same MAJOR version. Implementations MAY also be able to read messages from future releases of the protocol with a different MAJOR version.

## Format specification

The Jelly serialization format uses [Protocol Buffers version 3](https://protobuf.dev/programming-guides/proto3/) as the underlying serialization format. All implementations MUST use a compliant Protocol Buffers implementation. The Protocol Buffers schema for Jelly serialization is defined in `rdf.proto` ([source code](https://github.com/Jelly-RDF/jelly-protobuf/blob/main/rdf.proto), [reference](reference.md#rdfproto)).

The Jelly format is a *stream* (i.e., an ordered sequence) of *stream frames*. The frames may be sent one-by-one using a dedicated streaming protocol (e.g., [gRPC](streaming.md), MQTT, Kafka) or written in sequence to a byte stream (e.g., a file or socket). When writing to a byte stream, the frames MUST be delimeted – see the [delimited variant](#delimited-variant-of-jelly).

Jelly supports several distinct [types of streams](#stream-types), and uses a simple and configurable compression mechanism using [lookup tables](#prefix-name-and-datatype-lookups).

### Stream frames

A stream frame is a message of type `RdfStreamFrame` ([reference](reference.md#rdfstreamframe)). The message has only one field (`rows`), which is a repeated field of type `RdfStreamRow` ([reference](reference.md#rdfstreamrow)). A stream frame may contain any number of rows, however it is RECOMMENDED to keep the size of the frames below 1 MB. The semantics for the frames are not defined by the protocol. The end users are free to define their own semantics for the frames.

!!! note

    A stream frame in "simple flat file" is just a batch of RDF statements – the stream frames may carry no semantics in this case. You can make the stream frame as long as the file itself, but this is not recommended, as it would make the file harder to process.

!!! note

    Stream frames can also be used to indicate individual stream elements. For example, in the case of a stream of RDF datasets, each frame may contain one dataset. [RiverBench datasets](https://w3id.org/riverbench/datasets) use this convention in their distributions.

#### Ordering

Stream frames MUST be processed strictly in order to preserve the semantics of the stream.

Implementations MAY choose to adopt a **non-standard** solution where the order of the frames is not guaranteed and the stream can be read in more than one order. The implementation MUST clearly specify in the documentation that it uses such a non-standard solution.

!!! note

    An example where not adhering to the strict ordering may be useful is when you are dealing with a network streaming protocol that does not guarantee the order of the messages (e.g., MQTT).

!!! note

    The main thing you will need to worry about is the order of the lookup tables. If you can, emit all lookup tables at the beginning of the stream. When using stream partitions (e.g., in Kafka), you should ensure that the lookups are emitted to each partition. Alternatively, you can transmit the lookup tables separately from the stream.

### Stream rows

A stream row is a message of type `RdfStreamRow`. It has one of the following fields set:

- `options` (1) – [stream options header](#stream-options), indicating the compression options and the used RDF features in the stream.
- `triple` (2) – [RDF triple statement](#rdf-statements-and-graphs). It MUST NOT appear in streams of type other than `RDF_STREAM_TYPE_TRIPLES` or `RDF_STREAM_TYPE_GRAPHS`.
- `quad` (3) – [RDF quad statement](#rdf-statements-and-graphs). It MUST NOT appear in streams of type other than `RDF_STREAM_TYPE_QUADS`.
- `graph_start` (4) – indicates the [start of a graph](#rdf-statements-and-graphs) (named or default). It MUST NOT appear in streams of type other than `RDF_STREAM_TYPE_GRAPHS`.
- `graph_end` (5) – indicates the [end of a graph](#rdf-statements-and-graphs) (named or default). It MUST NOT appear in streams of type other than `RDF_STREAM_TYPE_GRAPHS`.
- `name` (9) – entry in the [name lookup](#prefix-name-and-datatype-lookups).
- `prefix` (10) – entry in the [prefix lookup](#prefix-name-and-datatype-lookups).
- `datatype` (11) – entry in the [datatype lookup](#prefix-name-and-datatype-lookups).

Stream rows MUST be processed strictly in order to preserve the semantics of the stream.

### Stream types

The type of the stream MUST be explicitly specified in the (stream options header)[#stream-options]. The type of the stream is defined by the `RdfStreamType` enum ([reference](reference.md#rdfstreamtype)). The following types are defined:

- `RDF_STREAM_TYPE_UNSPECIFIED` (0) – default value. This stream type MUST NOT be used. The implementations SHOULD treat this value as an error.
- `RDF_STREAM_TYPE_TRIPLES` (1) – stream of [RDF triple statements](https://www.w3.org/TR/rdf11-concepts/#section-triples). Each stream frame (or the entire stream) corresponds to an [RDF graph](https://www.w3.org/TR/rdf11-concepts/#section-rdf-graph). In this case, the stream MUST NOT contain `RdfStreamRow` messages with the `quad`, `graph_start`, or `graph_end` fields set.
- `RDF_STREAM_TYPE_QUADS` (2) – stream of RDF quad statements (same as [*simple statements* in N-Quads](https://www.w3.org/TR/n-quads/#simple-triples)). Each stream frame (or the entire stream) corresponds to an [RDF dataset](https://www.w3.org/TR/rdf11-concepts/#section-dataset). In this case, the stream MUST NOT contain `RdfStreamRow` messages with the `triple`, `graph_start`, or `graph_end` fields set.
- `RDF_STREAM_TYPE_GRAPHS` (3) – stream of RDF graphs (named or default). Each stream frame (or the entire stream) corresponds to an [RDF dataset](https://www.w3.org/TR/rdf11-concepts/#section-dataset). In this case, the stream MUST NOT contain `RdfStreamRow` messages with the `quad` fields set.

!!! note

    See also [a more human explanation](index.md#stream-types) of the available stream types.

### Stream options

The stream options is a message of type `RdfStreamOptions` ([reference](reference.md#rdfstreamoptions)). It MUST be the first row in the stream. It MAY appear more than once in the stream (also after other rows), but it MUST be identical to all previous occurrences. Implementations MAY throw an error if the stream options header is not present at the start of the stream, alternatively, they MAY use the default options. Implementations SHOULD NOT throw an error if the stream options header is present more than once in the stream.

The stream options header instructs the consumer of the stream (parser) on the size of the needed lookups to decode the stream and the features used by the stream.

The stream options header contains the following fields:

- `stream_name` (1) – name of the stream. This field is OPTIONAL and its use is not defined by the protocol. It MAY be used to identify the stream.
- `stream_type` (2) – [type of the stream](#stream-types). This field is REQUIRED.
- `generalized_statements` (3) – whether the stream contains [generalized RDF triples or graphs](https://www.w3.org/TR/rdf11-concepts/#section-generalized-rdf). This field MUST be set to true if the stream contains generalized RDF triples or graphs. It SHOULD NOT be set to true if the stream does not use this feature. This field is OPTIONAL and defaults to false.
- `use_repeat` (4) – whether the stream uses [repeated terms compression](#repeated-terms). This field MUST be set to true if the stream uses repeated terms. It SHOULD NOT be set to true if the stream does not use this feature. This field is OPTIONAL and defaults to false.
- `rdf_star` (5) – whether the stream uses [RDF-star](https://w3c.github.io/rdf-star/cg-spec/editors_draft.html) (quoted triples). This field MUST be set to true if the stream uses RDF-star. It SHOULD NOT be set to true if the stream does not use this feature. This field is OPTIONAL and defaults to false.
- `max_name_table_size` (9) – maximum size of the [name lookup](#prefix-name-and-datatype-lookups). This field is OPTIONAL and defaults to 0 (no lookup). If the field is set to 0, the name lookup MUST NOT be used in the stream. If the field is set to a positive value, the name lookup SHOULD be used in the stream and the size of the lookup MUST NOT exceed the value of this field.
- `max_prefix_table_size` (10) – maximum size of the [prefix lookup](#prefix-name-and-datatype-lookups). This field is OPTIONAL and defaults to 0 (no lookup). If the field is set to 0, the prefix lookup MUST NOT be used in the stream. If the field is set to a positive value, the prefix lookup SHOULD be used in the stream and the size of the lookup MUST NOT exceed the value of this field.
- `max_datatype_table_size` (11) – maximum size of the [datatype lookup](#prefix-name-and-datatype-lookups). This field is OPTIONAL and defaults to 0 (no lookup). If the field is set to 0, the datatype lookup MUST NOT be used in the stream (which effectively prohibits the use of [datatype literals](#literals)). If the field is set to a positive value, the datatype lookup SHOULD be used in the stream and the size of the lookup MUST NOT exceed the value of this field.

### Prefix, name, and datatype lookups

Jelly uses a common mechanism of lookup tables for IRI prefixes, IRI names (postfixes), and datatypes. The lookups are used to compress the IRIs and datatypes in the stream. All lookups function in the same way:

- The lookup is a map from a varint to a valid UTF-8 string.
- The lookup can be modified at any point in the stream. The modification consists of setting the lookup for a given varint to a given string. The modification MUST be applied to all subsequent rows in the stream.
- The first use of a given lookup element MUST be after it is defined in the lookup. If the consumer encounters a lookup element that is not defined in the lookup, it SHOULD throw an error.
- The lookups are indexed from 1. The default value of 0 MUST NOT be used as a key in the lookup.
- The maximum size of the lookup is communicated at the start of the stream (see [stream options header](#stream-options)). The producer of the stream MUST NOT exceed the maximum size of the lookup. The consumer of the stream MAY implement the lookup as a fixed-size array, or extend it dynamically.
- The lookup is updated with different messages, depending on the type of the lookup:
    - [`RdfNameEntry`](reference.md#rdfnameentry) for the name lookup,
    - [`RdfPrefixEntry`](reference.md#rdfprefixentry) for the prefix lookup,
    - [`RdfDatatypeEntry`](reference.md#rdfdatatypeentry) for the datatype lookup.
- The producer may use any strategy to update the lookup.

!!! note

    The spec does not specify what strategy should the producer use to update the lookup. You can use a the LRU strategy (as used in the Scala implementation), LFU, or something more complex. You can also have a fixed lookup in the producer and communicate it at the start of the stream. This is possible if you are using a fixed set of prefixes, names, or datatypes and want to conserve computing power (e.g., in IoT devices).

    The simplest way to implement the consumer's lookup is to just use an indexed array of fixed size. The workload on the consumer's side is much lower than on the producer's side, so your choice of the strategy depends largely on the producer.

### RDF statements and graphs

RDF statements (triples or quads) are communicated in three different ways, depending on the type of the stream:

- `RDF_STREAM_TYPE_TRIPLES` – triples are encoded using [`RdfTriple`](reference.md#rdftriple) messages.
    - `RdfTriple` has three fields: `s`, `p`, `o`, corresponding to the subject, predicate, and object of the triple. All of these fields are [RDF terms](#rdf-terms) and are REQUIRED.
- `RDF_STREAM_TYPE_QUADS` – quads are encoded using [`RdfQuad`](reference.md#rdfquad) messages.
    - `RdfQuad` has four fields: `s`, `p`, `o`, `g`, corresponding to the subject, predicate, object, and graph of the quad. The `s`, `p`, `o` are [RDF terms](#rdf-terms) and are REQUIRED. The `g` field is an [RDF graph node](#rdf-graph-nodes) and is REQUIRED.
- `RDF_STREAM_TYPE_GRAPHS` – graphs are encoded using [`RdfGraphStart`](reference.md#rdfgraphstart) and [`RdfGraphEnd`](reference.md#rdfgraphend) messages. Triples between the start and end of the graph are encoded using [`RdfTriple`](reference.md#rdftriple) messages. If a triple is between the start and end of the graph, it is considered to be in the graph.
    - In this type of stream, triples MUST NOT occur outside of a graph. If a triple is encountered outside a graph, the consumer SHOULD throw an error.
    - A graph start MUST NOT occur inside another graph. If a graph start is encountered inside another graph, the consumer SHOULD throw an error.
    - A graph end MUST NOT occur outside a graph. If a graph end is encountered outside a graph, the consumer MAY throw an error.
    - A graph MAY be empty (i.e., it may contain no triples).
    - A graph corresponding to one graph node MAY occur multiple times in a stream or a stream frame. The consumer MUST treat all occurrences of the graph as a single RDF graph.

### RDF terms

RDF terms are encoded using the [`RdfTerm`](reference.md#rdfterm) message. The message has one of the following fields set: `iri`, `bnode`, `literal`, `triple_term`, `repeat`, corresponding to RDF IRIs, blank nodes, literals, RDF-star quoted triples, and repeated terms, respectively. Exactly one of these fields MUST be set.

#### IRIs

The IRIs are encoded using the [`RdfIri`](reference.md#rdfiri) message. The message has two fields that together make up the IRI:

- `prefix_id` (1) – 1-based index of the prefix of the IRI, corresponding to an entry in the prefix lookup. This field is OPTIONAL and the default value (0) indicates an empty prefix.
- `name_id` (2) – 1-based index of the name (suffix) of the IRI, corresponding to an entry in the name lookup. This field is OPTIONAL and the default value (0) indicates an empty name.

At least one of the `prefix_id` and `name_id` fields MUST be set to a non-default, positive value. The IRI is then constructed by concatenating the prefix and the name. The IRI SHOULD be a valid IRI, as defined in [RFC 3987](https://tools.ietf.org/html/rfc3987).

??? example "Example (click to expand)"

    Assume the following lookup entries were defined in the stream (wrapping `RdfStreamRow`s were omitted for brevity):

    ```protobuf
    RdfPrefixEntry {
        id: 1
        prefix: "http://example.com/"
    }
    RdfNameEntry {
        id: 4
        name: "example"
    }
    RdfNameEntry {
        id: 1
        name: "http://test.com/test"
    }
    ```

    Then the following IRIs are encoded as follows:

    ```protobuf
    # http://example.com/example
    RdfIri {
        prefix_id: 1
        name_id: 4
    } 

    # http://example.com/
    RdfIri {
        prefix_id: 1
    }

    # http://test.com/test
    RdfIri {
        name_id: 1
    }
    ```

!!! note

    The spec does not specify how to split the IRIs into names and prefixes. You can use any strategy you want, as long as you follow the rules above. The simplest way is to split the IRI at the last occurrence of the `#` or `/` character – this is what the Scala implementation uses. The prefixes are not meant to be user-facing, but you can also use user-defined prefixes (e.g., `@prefix` in Turtle) to split the IRIs.

#### Blank nodes

RDF blank nodes are represented using simple strings. The string is the identifier of the blank node. The identifier may be any valid UTF-8 string.

Because the spec does not define the semantics of the stream frames, blank node identifiers are not guaranteed to be unique across the stream frames. The consumer MAY choose to treat the blank nodes as unique across the stream (and thus treat all occurences of the identifier as a single node), or it MAY choose to treat them as unique only within a single stream frame. The producer SHOULD specify in the documentation which strategy it uses.

!!! note

    If the stream is meant to represent a single RDF graph or dataset, then the blank node identifiers should be unique across the stream so that you can refer to them across stream frame boundaries. If the frames refer to different graphs or datasets, then the blank node identifiers should be unique only within a single frame.

!!! note

    Many RDF libraries (e.g., RDF4J, Apache Jena) use internal identifiers for blank nodes, which can be used as the identifiers in Jelly streams. You can also use a different format, for example with shorter identifiers to preserve space.

#### Literals

RDF literals are represented using the `RdfLiteral` message ([reference](reference.md#rdfliteral)). The message has the following fields:

- `lex` (1) – the lexical form of the literal in UTF-8. This field is OPTIONAL and defaults to an empty string.
- `literalKind` oneof. This field is REQUIRED and exactly one of the following fields MUST be set:
    - `simple` (2) – empty message of type `RdfLiteralSimple` indicating that the literal is a simple literal (has datatype IRI equal to `http://www.w3.org/2001/XMLSchema#string`).
    - `langtag` (3) – UTF-8 language tag, indicating that the literal is a language-tagged string (has datatype IRI equal to `http://www.w3.org/1999/02/22-rdf-syntax-ns#langString`). The language tag SHOULD be a valid [BCP 47](https://tools.ietf.org/html/bcp47) language tag.
    - `datatype` (4) – 1-based index of the datatype in the [datatype lookup](#prefix-name-and-datatype-lookups), indicating that the literal is a typed literal. The value of this field MUST be greater than 0 and it MUST correspond to a valid entry in the datatype lookup.

#### Quoted triples (RDF-star)

#### Repeated terms

### RDF graph nodes

## Delimited variant of Jelly

!!! note

    Protobuf messages [are not delimited](https://protobuf.dev/programming-guides/techniques/#streaming), so if you write multiple messages to the same file / socket / byte stream, you need to add some kind of delimiter between them. Jelly uses the convention already implemented in some protobuf libraries of prepending a varint before the message, to specify the length of the message. 

A byte stream (or file) in the delimited variant MUST consist of a series of delimited `RdfStreamFrame` messages. A delimited message is a message that has a varint prepended before it, specifying the length of the message in bytes.

Implementing the delimited variant is OPTIONAL.

### Implementations

The delimiting convention is implemented in Protobuf libraries for:

- C++: [delimited_message_util.cc](https://github.com/protocolbuffers/protobuf/blob/main/src/google/protobuf/util/delimited_message_util.cc)
- Java / Scala: [writeDelimitedTo](https://developers.google.com/protocol-buffers/docs/reference/java/com/google/protobuf/MessageLite#writeDelimitedTo-java.io.OutputStream-) and [parseDelimitedFrom](https://developers.google.com/protocol-buffers/docs/reference/java/com/google/protobuf/Parser#parseDelimitedFrom-java.io.InputStream-)

The JVM (Scala) implementation of Jelly also supports the delimited variant – [see the documentation](../jvm/reactive.md#byte-streams).
