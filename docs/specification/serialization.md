# Jelly serialization format

TODO: intro, reference to RDF 1.1 and RDF-star, link to the proto reference, status of this spec

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
- `max_name_table_size` (9) – maximum size of the [name lookup](#prefix-name-and-datatype-lookups). This field is OPTIONAL and defaults to 0 (no lookup). If the field is set to 0, the name lookup MUST NOT be used in the stream. If the field is set to a positive value, the name lookup SHOULD be used and the size of the lookup MUST NOT exceed the value of this field.
- `max_prefix_table_size` (10) – maximum size of the [prefix lookup](#prefix-name-and-datatype-lookups). This field is OPTIONAL and defaults to 0 (no lookup). If the field is set to 0, the prefix lookup MUST NOT be used in the stream. If the field is set to a positive value, the prefix lookup SHOULD be used and the size of the lookup MUST NOT exceed the value of this field.
- `max_datatype_table_size` (11) – maximum size of the [datatype lookup](#prefix-name-and-datatype-lookups). This field is OPTIONAL and defaults to 0 (no lookup). If the field is set to 0, the datatype lookup MUST NOT be used in the stream (which effectively prohibits the use of [datatype literals](#literals)). If the field is set to a positive value, the datatype lookup SHOULD be used and the size of the lookup MUST NOT exceed the value of this field.

### Prefix, name, and datatype lookups

TODO

### RDF statements and graphs

### RDF terms

#### IRIs

#### Blank nodes

#### Literals

#### Quoted triples (RDF-star)

#### Repeated terms

### RDF graph nodes

## Delimited variant of Jelly

!!! note

    Protobuf messages [are not delimited](https://protobuf.dev/programming-guides/techniques/#streaming), so if you write multiple messages to the same file / socket / byte stream, you need to add some kind of delimiter between them. Jelly uses the convention already implemented in some protobuf libraries of prepending a varint before the message, to specify the length of the message. 

A byte stream (or file) in the delimited variant MUST consist of a series of delimited `RdfStreamFrame` messages. A delimited message is a message that has a varint prepended before it, specifying the length of the message.

Implementing the delimited variant is OPTIONAL.

### Implementations

The delimiting convention is implemented in:

- C++: [delimited_message_util.cc](https://github.com/protocolbuffers/protobuf/blob/main/src/google/protobuf/util/delimited_message_util.cc)
- Java / Scala: [writeDelimitedTo](https://developers.google.com/protocol-buffers/docs/reference/java/com/google/protobuf/MessageLite#writeDelimitedTo-java.io.OutputStream-) and [parseDelimitedFrom](https://developers.google.com/protocol-buffers/docs/reference/java/com/google/protobuf/Parser#parseDelimitedFrom-java.io.InputStream-)

The JVM (Scala) implementation of Jelly also supports the delimited variant – [see the documentation](../jvm/reactive.md#byte-streams).
