# Jelly serialization format specification

**This document is the specification of the Jelly serialization format. It is intended for implementers of Jelly libraries and applications.** If you are looking for a user-friendly introduction to Jelly, see the [Jelly index page](index.md).

This document is accompanied by the [Jelly Protobuf reference](reference.md) and the Protobuf definition itself ([`rdf.proto`](https://github.com/Jelly-RDF/jelly-protobuf/blob/main/rdf.proto)).

The following assumptions are used in this document:

- The basis for the terms used is the RDF 1.1 specification ([W3C Recommendation 25 February 2014](https://www.w3.org/TR/rdf11-concepts/)).
- In parts referring to RDF-star, the RDF-star draft specification ([W3C Community Group Draft Report 29 June 2023](https://w3c.github.io/rdf-star/cg-spec/editors_draft.html)) is used. As the scope in which the RDF-star specification is used here is minimal, later versions of the specification are expected to be compatible with this document.
- In parts referring to the RDF Stream Taxonomy (RDF-STaX), the [RDF-STaX version 1.1.1 ontology](https://w3id.org/stax/1.1.1/ontology) and [taxonomy](https://w3id.org/stax/1.1.1/taxonomy) are used. <!-- !!! When updating the RDF-STaX version, also update it in text in the "Logical stream types" section and in the links to RDF-STaX. !!! -->
- All strings in the serialization are assumed to be UTF-8 encoded.

**Author:** [Piotr Sowiński](https://orcid.org/0000-0002-2543-9461) ([Ostrzyciel](https://github.com/Ostrzyciel))

**Version:** 1.0.0

**Document status**: Draft specification

!!! info

    The key words "MUST", "MUST NOT", "REQUIRED", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

!!! note

    The "Note" blocks in this document are not part of the specification, but rather provide additional information for implementers.

!!! note

    The "Example" blocks in this document are not part of the specification, but rather provide informal examples of the serialization format. The examples use the [Protocol Buffers Text Format Language](https://protobuf.dev/reference/protobuf/textformat-spec/).

## Conformance

Implementations MAY choose to implement only a subset of the following specification. In this case, they SHOULD clearly specify which parts of the specification they implement. In the rest of this specification, the keywords "MUST", "MUST NOT", etc. refer to full (not partial) implementations.

!!! note

    Implementations may in particular choose to not implement features that are not supported on the target platform (e.g., RDF datasets, RDF-star, generalized RDF terms, etc.).

Implementations MAY also choose to extend Jelly with additional features that SHOULD NOT interfere with the serialization being readable by implementations which follow the specification.

## Versioning

The protocol follows the [Semantic Versioning 2.0](https://semver.org/) scheme. Each MAJOR.MINOR semantic version corresponds to an integer version tag in the protocol. The version tag is encoded in the `version` field of the [`RdfStreamOptions`](reference.md#rdfstreamoptions) message. See also the [section on stream options](#stream-options) for more information on how to handle the version tags in serialized streams.

The following versions of the protocol are defined:

| Version tag | Semantic version |               |
| ----------- | ---------------- | ------------- |
| 1           | 1.0.x            | **(current)** |

!!! note
    
    Releases of the protocol are published on [GitHub](https://github.com/Jelly-RDF/jelly-protobuf/releases).

### Backward compatibility

Implementations SHOULD ensure backward compatibility. To achieve backward compatibility, the implementation MUST be able to read all messages from the previous releases of the protocol with the same MAJOR version. The implementation MAY also be able to read messages from previous releases of the protocol with a different MAJOR version.

!!! note

    The protocol is designed in such a way that you don't need to worry about backward compatibility. The only thing you need to do is to implement the latest version of the protocol, and you will automatically get backward compatibility with all previous versions (of the same MAJOR).

### Forward compatibility

Forward compatibility is not guaranteed. Implementations MAY be able to read messages from future releases of the protocol with the same MAJOR version. Implementations MAY also be able to read messages from future releases of the protocol with a different MAJOR version.

## Actors and implementations

Jelly assumes there to be two actors involved in processing the stream: the producer (serializer) and the consumer (parser). The producer is responsible for serializing the RDF data into the Jelly format, and the consumer is responsible for parsing the Jelly format into RDF data.

Implementations may include only the producer, only the consumer, or both.

## Format specification

The Jelly serialization format uses [Protocol Buffers version 3](https://protobuf.dev/programming-guides/proto3/) as the underlying serialization format. All implementations MUST use a compliant Protocol Buffers implementation. The Protocol Buffers schema for Jelly serialization is defined in `rdf.proto` ([source code](https://github.com/Jelly-RDF/jelly-protobuf/blob/main/rdf.proto), [reference](reference.md#rdfproto)).

The Jelly format is a *stream* (i.e., an ordered sequence) of *stream frames*. The frames may be sent one-by-one using a dedicated streaming protocol (e.g., [gRPC](streaming.md), MQTT, Kafka) or written in sequence to a byte stream (e.g., a file or socket). When writing to a byte stream, the frames MUST be delimeted – see the [delimited variant](#delimited-variant-of-jelly).

Jelly supports several distinct [physical types of streams](#physical-stream-types), and uses a simple and configurable compression mechanism using [lookup tables](#prefix-name-and-datatype-lookup-entries).

### Stream frames

A stream frame is a message of type `RdfStreamFrame` ([reference](reference.md#rdfstreamframe)). The message has only one field (`rows`), which is a repeated field of type `RdfStreamRow` ([reference](reference.md#rdfstreamrow)). A stream frame may contain any number of rows, however it is RECOMMENDED to keep the size of the frames below 1 MB. The semantics for the frames are not defined by the protocol. The end users are free to define their own semantics for the frames.

!!! note

    A stream frame in "simple flat file" is just a batch of RDF statements – the stream frames may carry no semantics in this case. You can make the stream frame as long as the file itself, but this is not recommended, as it would make the file harder to process.

!!! note

    Stream frames can also be used to indicate individual stream elements. For example, in the case of a stream of RDF datasets, each frame may contain one dataset. [RiverBench datasets](https://w3id.org/riverbench/datasets) use this convention in their distributions.

#### Ordering

Stream frames MUST be processed strictly in order to preserve the semantics of the stream. Each stream frame MUST be processed in its entirety before the next stream frame is processed.

Implementations MAY choose to adopt a **non-standard** solution where the order or delivery of the frames is not guaranteed and the stream can be read in more than one order or without some frames. The implementation MUST clearly specify in the documentation that it uses such a non-standard solution.

!!! note

    An example where not adhering to the strict ordering may be useful is when you are dealing with a network streaming protocol that does not guarantee the order of the messages (e.g., MQTT).

!!! note

    The main thing you will need to worry about is the order of the lookup tables. If you can, emit all lookup tables at the beginning of the stream. When using stream partitions (e.g., in Kafka), you should ensure that the lookups are emitted to each partition. Alternatively, you can transmit the lookup tables separately from the stream.

### Stream rows

A stream row is a message of type `RdfStreamRow`. It has one of the following fields set:

- `options` (1) – [stream options header](#stream-options), indicating the compression options and the used RDF features in the stream.
- `triple` (2) – [RDF triple statement](#rdf-statements-and-graphs). It MUST NOT appear in streams of type other than `PHYSICAL_STREAM_TYPE_TRIPLES` or `PHYSICAL_STREAM_TYPE_GRAPHS`.
- `quad` (3) – [RDF quad statement](#rdf-statements-and-graphs). It MUST NOT appear in streams of type other than `PHYSICAL_STREAM_TYPE_QUADS`.
- `graph_start` (4) – indicates the [start of a graph](#rdf-statements-and-graphs) (named or default). It MUST NOT appear in streams of type other than `PHYSICAL_STREAM_TYPE_GRAPHS`.
- `graph_end` (5) – indicates the [end of a graph](#rdf-statements-and-graphs) (named or default). It MUST NOT appear in streams of type other than `PHYSICAL_STREAM_TYPE_GRAPHS`.
- `name` (9) – entry in the [name lookup](#prefix-name-and-datatype-lookup-entries).
- `prefix` (10) – entry in the [prefix lookup](#prefix-name-and-datatype-lookup-entries).
- `datatype` (11) – entry in the [datatype lookup](#prefix-name-and-datatype-lookup-entries).

Stream rows MUST be processed strictly in order to preserve the semantics of the stream.

### Physical stream types

The physical type of the stream MUST be explicitly specified in the [stream options header](#stream-options). The physical type of the stream is defined by the `PhysicalStreamType` enum ([reference](reference.md#PhysicalStreamType)). The following types are defined:

- `PHYSICAL_STREAM_TYPE_UNSPECIFIED` (0) – default value. This physical stream type MUST NOT be used. The implementations SHOULD treat this value as an error.
- `PHYSICAL_STREAM_TYPE_TRIPLES` (1) – stream of [RDF triple statements](https://www.w3.org/TR/rdf11-concepts/#section-triples). In this case, the stream MUST NOT contain `RdfStreamRow` messages with the `quad`, `graph_start`, or `graph_end` fields set.
- `PHYSICAL_STREAM_TYPE_QUADS` (2) – stream of RDF quad statements (same as [*simple statements* in N-Quads](https://www.w3.org/TR/n-quads/#simple-triples)). In this case, the stream MUST NOT contain `RdfStreamRow` messages with the `triple`, `graph_start`, or `graph_end` fields set.
- `PHYSICAL_STREAM_TYPE_GRAPHS` (3) – stream of RDF graphs (named or default). In this case, the stream MUST NOT contain `RdfStreamRow` messages with the `quad` fields set.

!!! note

    See also [a more human explanation](index.md#stream-types) of the available physical stream types.

!!! note

    The physical stream type only specifies how the data is encoded, not how it should be interpreted. See the [logical stream types](#logical-stream-types) for a mechanism to specify the semantics of the stream.

### Logical stream types

Specifying the logical stream type in the [stream options header](#stream-options) is OPTIONAL. When it is specified, the implementations MAY use it to determine the semantics of the stream. The implementations also MAY ignore the specified logical stream type and interpret the stream in any other manner. The logical stream type is defined by the `LogicalStreamType` enum ([reference](reference.md#LogicalStreamType)).

This version of Jelly uses the [RDF Stream Taxonomy (RDF-STaX) 1.1.1](https://w3id.org/stax/1.1.1) and implements all stream types of RDF-STaX as logical stream types. The following logical stream types are defined:

- `LOGICAL_STREAM_TYPE_UNSPECIFIED` (0) – default value. This logical stream type is used when the serializer chooses not to specify the logical stream type.
- `LOGICAL_STREAM_TYPE_FLAT_TRIPLES` (1)
    - RDF-STaX name: Flat RDF triple stream
    - RDF-STaX IRI: `https://w3id.org/stax/ontology#flatTripleStream`
- `LOGICAL_STREAM_TYPE_FLAT_QUADS` (2)
    - RDF-STaX name: Flat RDF quad stream
    - RDF-STaX IRI: `https://w3id.org/stax/ontology#flatQuadStream`
- `LOGICAL_STREAM_TYPE_GRAPHS` (3)
    - RDF-STaX name: RDF graph stream
    - RDF-STaX IRI: `https://w3id.org/stax/ontology#graphStream`
- `LOGICAL_STREAM_TYPE_DATASETS` (4)
    - RDF-STaX name: RDF dataset stream
    - RDF-STaX IRI: `https://w3id.org/stax/ontology#datasetStream`
- `LOGICAL_STREAM_TYPE_SUBJECT_GRAPHS` (13)
    - RDF-STaX name: RDF subject graph stream
    - RDF-STaX IRI: `https://w3id.org/stax/ontology#subjectGraphStream`
    - Subtype of: `LOGICAL_STREAM_TYPE_GRAPHS` (3)
- `LOGICAL_STREAM_TYPE_NAMED_GRAPHS` (14)
    - RDF-STaX name: RDF named graph stream
    - RDF-STaX IRI: `https://w3id.org/stax/ontology#namedGraphStream`
    - Subtype of: `LOGICAL_STREAM_TYPE_DATASETS` (4)
- `LOGICAL_STREAM_TYPE_TIMESTAMPED_NAMED_GRAPHS` (114)
    - RDF-STaX name: Timestamped RDF named graph stream
    - RDF-STaX IRI: `https://w3id.org/stax/ontology#timestampedNamedGraphStream`
    - Subtype of: `LOGICAL_STREAM_TYPE_NAMED_GRAPHS` (14)

#### Version compatibility and base types

In all Jelly versions 1.x.y there MUST be the same four base logical stream types (numbered 1, 2, 3, 4). The remaining logical stream types (with numbers greater than 10) may change between releases in the 1.x.y family, following the [versioning rules](#versioning). The four base types (1–4) are thus fixed, enabling forward compatibility for implementations that only support the base types.

Each remaining logical stream type is a subtype of a base type (including recursive subtyping). To determine the base type of a logical stream type, the implementation MUST take the last digit of the logical stream type number, which is equivalent to the modulo 10 operation. Implementations MAY choose to treat a subtype of a base type in the same manner as the base type itself.

??? example "Example (click to expand)"

    The base type of `LOGICAL_STREAM_TYPE_NAMED_GRAPHS` (14) is `LOGICAL_STREAM_TYPE_DATASETS` (4).

    The base type of `LOGICAL_STREAM_TYPE_TIMESTAMPED_NAMED_GRAPHS` (114) is `LOGICAL_STREAM_TYPE_DATASETS` (4).

    The base type of `LOGICAL_STREAM_TYPE_FLAT_TRIPLES` (1) is `LOGICAL_STREAM_TYPE_FLAT_TRIPLES` (1).

!!! note

    In practice, the base logical stream types (1–4) are the most important part, determining how the data should be shaped and processed. The other logical stream types are used to provide additional information about the stream. If you are implementing a streaming serializer/deserializer, you should focus on the base types and treat their subtypes in the same way. So, do a modulo 10 on the stream type and you are good to go.

#### Consistency with physical stream types

Implementations MAY choose to use the logical stream type to determine how to interpret the stream. In that case, the implementation SHOULD ensure that the logical stream type is consistent with the physical stream type in the sense that the implementation supports this combination of stream types. If the logical stream type is inconsistent with the physical stream type, the implementation MAY throw an error.

The following table shows the RECOMMENDED support matrix for the logical stream types and physical stream types, along with the RECOMMENDED manner in which the stream should be interpreted:

| RDF-STaX (logical type) / Physical type | `TRIPLES` | `QUADS` | `GRAPHS` |
|:--|:-:|:-:|:-:|
| `LOGICAL_STREAM_TYPE_GRAPHS` | Framed | ✘ | ✘ |
| `LOGICAL_STREAM_TYPE_SUBJECT_GRAPHS` | Framed | ✘ | ✘ |
| `LOGICAL_STREAM_TYPE_DATASETS` | ✘ | Framed | Framed |
| `LOGICAL_STREAM_TYPE_NAMED_GRAPHS` | ✘ | Framed | Framed |
| `LOGICAL_STREAM_TYPE_TIMESTAMPED_NAMED_GRAPHS` | ✘ | Framed | Framed |
| `LOGICAL_STREAM_TYPE_FLAT_TRIPLES` | Continuous | ✘ | ✘ |
| `LOGICAL_STREAM_TYPE_FLAT_QUADS` | ✘ | Continuous | Continuous |

In the table above, the following interpretations are used:

- **Framed** – each stream frame SHOULD be interpreted as a stream element, as per RDF-STaX definition.
- **Continuous** – the stream SHOULD be interpreted as a continuous flat stream of elements, as per RDF-STaX definition. In this case, the stream frames carry no meaning.
- **✘** – the combination of the logical stream type and the physical stream type is not directly supported.

The implementations MAY choose to interpret the stream in a different manner than the one specified in the table.

!!! note

    See the [user's guide](../user-guide.md#stream-types) for a more intuitive explanation of what this means.

    In any case, you can choose to entirely ignore this table which should only be treated as a recommended starting point. For example, you could have an RDF graph stream with physical type `GRAPHS`, where each graph spans multiple stream frames. This and other non-standard combinations are completely fine, just make sure that all actors involved support it.

### Stream options

The stream options is a message of type `RdfStreamOptions` ([reference](reference.md#rdfstreamoptions)). It MUST be the first row in the stream. It MAY appear more than once in the stream (also after other rows), but it MUST be identical to all previous occurrences. Implementations MAY throw an error if the stream options header is not present at the start of the stream, alternatively, they MAY use the default options. Implementations SHOULD NOT throw an error if the stream options header is present more than once in the stream.

The stream options header instructs the consumer of the stream (parser) on the size of the needed lookups to decode the stream and the features used by the stream.

The stream options header contains the following fields:

- `stream_name` (1) – name of the stream. This field is OPTIONAL and the manner in which it should be used is not defined by this specification. It MAY be used to identify the stream.
- `physical_type` (2) – [physical type of the stream](#physical-stream-types). This field is REQUIRED.
- `generalized_statements` (3) – whether the stream contains [generalized RDF triples or graphs](https://www.w3.org/TR/rdf11-concepts/#section-generalized-rdf). This field MUST be set to true if the stream contains generalized RDF triples or graphs. It SHOULD NOT be set to true if the stream does not use this feature. This field is OPTIONAL and defaults to false.
- `rdf_star` (4) – whether the stream uses [RDF-star](https://w3c.github.io/rdf-star/cg-spec/editors_draft.html) (quoted triples). This field MUST be set to true if the stream uses RDF-star. It SHOULD NOT be set to true if the stream does not use this feature. This field is OPTIONAL and defaults to false.
- `max_name_table_size` (9) – maximum size of the [name lookup](#prefix-name-and-datatype-lookup-entries). This field is OPTIONAL and defaults to 0 (no lookup). If the field is set to 0, the name lookup MUST NOT be used in the stream. If the field is set to a positive value, the name lookup SHOULD be used in the stream and the size of the lookup MUST NOT exceed the value of this field.
- `max_prefix_table_size` (10) – maximum size of the [prefix lookup](#prefix-name-and-datatype-lookup-entries). This field is OPTIONAL and defaults to 0 (no lookup). If the field is set to 0, the prefix lookup MUST NOT be used in the stream. If the field is set to a positive value, the prefix lookup SHOULD be used in the stream and the size of the lookup MUST NOT exceed the value of this field.
- `max_datatype_table_size` (11) – maximum size of the [datatype lookup](#prefix-name-and-datatype-lookup-entries). This field is OPTIONAL and defaults to 0 (no lookup). If the field is set to 0, the datatype lookup MUST NOT be used in the stream (which effectively prohibits the use of [datatype literals](#literals)). If the field is set to a positive value, the datatype lookup SHOULD be used in the stream and the size of the lookup MUST NOT exceed the value of this field.
- `logical_type` (14) – [logical type of the stream](#logical-stream-types), based on RDF-STaX. This field is OPTIONAL and defaults to `LOGICAL_STREAM_TYPE_UNSPECIFIED`.
- `version` (15) – [version tag](#versioning) of the stream. This field is REQUIRED.
    - The version tag is encoded as a varint. The version tag MUST be greater than 0.
    - The producer of the stream MUST set the version tag to the version tag of the implementation.
    - The consumer SHOULD throw an error if the version tag is greater than the version tag of the implementation.
    - The consumer SHOULD throw an error if the version tag is zero.
    - The consumer SHOULD NOT throw an error if the version tag is not zero but lower than the version tag of the implementation.
    - The producer may use version tags greater than 1000 to indicate non-standard versions of the protocol.

### Prefix, name, and datatype lookup entries

Jelly uses a common mechanism of lookup tables for IRI prefixes, IRI names (postfixes), and datatypes. The lookups are used to compress the IRIs and datatypes in the stream. All lookups share the same base mechanism:

- The lookup is a map from a varint to a valid UTF-8 string.
- The lookup can be modified at any point in the stream. The modification consists of setting the lookup for a given varint to a given string. The modification MUST be applied to all subsequent rows in the stream.
- The first use of a given lookup element MUST be after it is defined in the lookup. If the consumer encounters a lookup element that is not defined in the lookup, it SHOULD throw an error.
- The lookups are indexed from `1`. The default value of `0` is a special value:
    - If the index is set to `0` in the first entry of the lookup in the stream, it MUST be interpreted as the value `1`.
    - If the index is set to `0` in any other lookup entry, it MUST be interpreted as `previous_index + 1`, that is, the index of the previous entry incremented by one.
- The maximum size of the lookup is communicated at the start of the stream (see [stream options header](#stream-options)). The producer of the stream MUST NOT exceed the maximum size of the lookup. The consumer of the stream MAY implement the lookup as a fixed-size array, or extend it dynamically.
- The lookup is updated with different messages, depending on the type of the lookup:
    - [`RdfNameEntry`](reference.md#rdfnameentry) for the name lookup,
    - [`RdfPrefixEntry`](reference.md#rdfprefixentry) for the prefix lookup,
    - [`RdfDatatypeEntry`](reference.md#rdfdatatypeentry) for the datatype lookup.
- The producer may use any strategy to update the lookup.

!!! note

    The spec does not specify what strategy should the producer use to update the lookup. You can use a the LRU strategy (as used in the Scala implementation), LFU, or something more complex. You can also have a fixed lookup in the producer and communicate it at the start of the stream. This is possible if you are using a fixed set of prefixes, names, or datatypes and want to conserve computing power (e.g., in IoT devices).

    The simplest way to implement the consumer's lookup is to just use an indexed array of fixed size. The workload on the consumer's side is much lower than on the producer's side, so your choice of the strategy depends largely on the producer.


!!! note

    The default value of `0` has a special meaning in lookup entries. You should take advantage of that and use it whenever possible. As the value of `0` is encoded with exactly zero bytes, you can save some space by using it.


### RDF statements and graphs

RDF statements (triples or quads) are communicated in three different ways, depending on the type of the stream:

- `PHYSICAL_STREAM_TYPE_TRIPLES` – triples are encoded using [`RdfTriple`](reference.md#rdftriple) messages.
    - `RdfTriple` consists of three oneofs: `subject`, `predicate`, `object`, corresponding to the three terms in an RDF triple. Each of these oneofs has four fields, out of which at most one MUST be set.
    - If no field in a given oneof is set, the term is considered to be a repeated term (see [repeated terms](#repeated-terms)).
- `PHYSICAL_STREAM_TYPE_QUADS` – quads are encoded using [`RdfQuad`](reference.md#rdfquad) messages.
    - `RdfQuad` consists of four oneofs: `subject`, `predicate`, `object`, `graph`, corresponding to the three terms and one graph node of the quad. Each of these oneofs has four fields, out of which at most one MUST be set.
    - If no field in a given oneof is set, the term is considered to be a repeated term/graph node (see [repeated terms](#repeated-terms)).
- `PHYSICAL_STREAM_TYPE_GRAPHS` – graphs are encoded using [`RdfGraphStart`](reference.md#rdfgraphstart) and [`RdfGraphEnd`](reference.md#rdfgraphend) messages. Triples between the start and end of the graph are encoded using [`RdfTriple`](reference.md#rdftriple) messages. If a triple is between the start and end of the graph, it is considered to be in the graph.
    - In this type of stream, triples MUST NOT occur outside of a graph. If a triple is encountered outside a graph, the consumer SHOULD throw an error.
    - A graph start MUST NOT occur inside another graph. If a graph start is encountered inside another graph, the consumer SHOULD throw an error.
    - A graph end MUST NOT occur outside a graph. If a graph end is encountered outside a graph, the consumer MAY throw an error.
    - A graph MAY be empty (i.e., it may contain no triples).
    - A graph corresponding to one graph node MAY occur multiple times in a stream or a stream frame. The consumer MUST treat all occurrences of the graph as a single RDF graph.
    - A graph MAY span more than one stream frame. The consumer MUST treat the graph spanning several stream frames as a single RDF graph.
    - Exactly one field in the `RdfGraphStart` message MUST be set – no repeated terms are allowed here. The consumer SHOULD throw an error if no field in the `graph` oneof is set.

!!! note

    If the stream is meant to represent a single RDF dataset, then the graphs should be able to stretch across several stream frames. If the stream is meant to represent a stream of RDF datasets, then the graphs should be contained within a single stream frame.

#### Repeated terms

Both `RdfTriple` and `RdfQuad` offer a simple compression mechanism – repeated terms. If a term in a given position (subject, predicate, object, or graph node in quads) is not set, then it is interpreted to be the same as the term in the same position in the previous triple or quad. Repeated terms are encoded simply by not setting any field in the corresponding oneof, and therefore take up zero bytes in the stream.

- Repeated terms MUST NOT occur in quoted triples.
- Repeated terms MUST NOT occur in the first statement row of the stream.
- Repeated terms MAY occur in the first statement row of a stream frame. In this case, the repeated terms MUST be interpreted as repeated from the previous stream frame.
- A repeated term in a given position MAY occur after a repeated term. The consumer MUST interpret all consecutive appearances of the repeated term as the same term.

??? example "Example (click to expand)"

    In the example the wrapping `RdfStreamRow`s were omitted for brevity:

    ```protobuf
    # First row
    RdfTriple {
        s_iri: RdfIri {
            prefix_id: 1
            name_id: 1
        }
        p_iri: RdfIri {
            prefix_id: 1
            name_id: 2
        }
        o_bnode: "b1"
    }

    # Second row – repeating the subject and predicate
    # s_iri and p_iri are reused from the previous row
    RdfTriple {
        o_bnode: "b2"
    }

    # Third row – repeating the subject and object
    # s_iri and o_bnode are reused from the first row
    RdfTriple {
        p_iri: RdfIri {
            prefix_id: 2
            name_id: 3
        }
    }
    ```

!!! note

    Repeated terms are a simple, yet incredibly effective compression mechanism and you should use them whenever possible. They are doubly effective: not only you save space by not repeating the terms, but also repeated terms are not encoded at all (zero bytes on the wire), which saves even more space.

!!! note

    Repeated terms can be simply implemented with four variables (s, p, o, g) holding the last non-repeated value of a term in that position. This O(1) solution is what the Scala implementation uses.

!!! note

    Although repeated terms can stretch across stream frame boundaries (i.e., refer to values last seen in the previous stream frame), you don't have to use this feature. If your use case requires the stream frames to be more independent of each other (see: [stream frame ordering](#ordering)), you can just reset the repeated terms at the start of each stream frame.

### RDF terms and graph nodes

RDF terms and graph nodes are encoded using oneofs in [`RdfTriple`](reference.md#rdftriple), [`RdfQuad`](reference.md#rdfquad), and [`RdfGraphStart`](reference.md#rdfgraphstart). The oneofs have each several fields, depending on the type of the term: `*_iri`, `*_bnode`, `*_literal`, `*_triple_term`, `g_default_graph`, corresponding to RDF IRIs, blank nodes, literals, RDF-star quoted triples, and the default RDF graph in an RDF dataset, respectively. At most one field in each oneof MUST be set.

#### IRIs

The IRIs are encoded using the [`RdfIri`](reference.md#rdfiri) message. The message has two fields that together make up the IRI:

- `prefix_id` (1) – 1-based index of the prefix of the IRI, corresponding to an entry in the prefix lookup.
    - The default value of `0` MUST be interpreted as the same value as in the last explictly specified (non-zero) prefix identifier.
    - If `0` appears in the first IRI of the stream (and in any subsequent IRI), this MUST be interpreted as an empty prefix (zero-length string). This is for example used when the prefix lookup table is set to size zero.
- `name_id` (2) – 1-based index of the name (suffix) of the IRI, corresponding to an entry in the name lookup. This field is OPTIONAL and the default value (0) indicates an empty name.
    - The default value of `0` MUST be interpreted as `previous_name_id + 1`, that is, the `name_id` of the previous IRI incremented by one.
    - If `0` appears in the first IRI of the stream it MUST be interpreted as `1`.
    - Multiple `0` values in a row may occur, in which case the `name_id` MUST be interpreted as incrementing by one for each `0` value.

For the default value behavior to work correctly, IRIs in the stream MUST be processed strictly in order: firstly by stream row, then by term (subject, predicate, object, graph). This also applies recursively to RDF-star quoted triples.

The IRI is then constructed by first decoding the prefix and the name using the [prefix and name lookup tables](#prefix-name-and-datatype-lookup-entries), and then concatenating the prefix and the name. The IRI SHOULD be a valid IRI, as defined in [RFC 3987](https://tools.ietf.org/html/rfc3987).

??? example "Example with the prefix table (click to expand)"

    Assume the following lookup entries were defined in the stream (wrapping `RdfStreamRow`s were omitted for brevity):

    ```protobuf
    RdfPrefixEntry {
        id: 0 # default value, interpreted as 1
        prefix: "http://example.com/"
    }
    RdfNameEntry {
        id: 0 # default value, interpreted as 1
        name: "example"
    }
    RdfNameEntry {
        id: 0 # default value, interpreted as 1 + 1 = 2
        name: ""
    }
    RdfNameEntry {
        id: 0 # default value, interpreted as 2 + 1 = 3
        name: "test"
    }
    ```

    Then the following IRIs are encoded as follows:

    ```protobuf
    # http://example.com/example
    RdfIri {
        prefix_id: 1
        name_id: 0 # default value, interpreted as 1
    } 

    # http://example.com/
    RdfIri {
        prefix_id: 0 # default value, interpreted as 1
        name_id: 0 # default value, interpreted as 1 + 1 = 2
    }

    # http://test.com/test
    RdfIri {
        prefix_id: 0 # default value, interpreted as 1
        name_id: 0 # default value, interpreted as 2 + 1 = 3
    }
    ```

    Note that the default values (zeroes) are not encoded at all in Protobuf and therefore take up zero bytes in the stream.

??? example "Example without the prefix table (click to expand)"

    In this example, the prefix lookup table is not used. The lookup entries are defined as follows:

    ```protobuf
    RdfNameEntry {
        id: 0 # default value, interpreted as 1
        name: "http://example.com/example"
    }

    RdfNameEntry {
        id: 0 # default value, interpreted as 1 + 1 = 2
        name: "http://example.com/test"
    }
    ```

    Then the following IRIs are encoded as follows:

    ```protobuf
    # http://example.com/example
    RdfIri {
        prefix_id: 0 # default value, interpreted as empty prefix
        name_id: 0 # default value, interpreted as 1
    }

    # http://example.com/test
    RdfIri {
        prefix_id: 0 # default value, interpreted as empty prefix
        name_id: 0 # default value, interpreted as 1 + 1 = 2
    }
    ```
    

!!! note

    The spec does not specify how to split the IRIs into names and prefixes. You can use any strategy you want, as long as you follow the rules above. The simplest way is to split the IRI at the last occurrence of the `#` or `/` character – this is what the Scala implementation uses. The prefixes are not meant to be user-facing, but you can also use user-defined prefixes (e.g., `@prefix` in Turtle) to split the IRIs.

!!! note

    The behavior of the default values is designed to save space in the stream. Usually in RDF many IRIs share the same prefix, so you can save space by not repeating the prefix in the stream. At the same time the name part of the IRI is often unique, so for each name you will need a new entry in the lookup table – which is often the next entry after the one you have just created.

#### Blank nodes

RDF blank nodes are represented using simple strings. The string is the identifier of the blank node. The identifier may be any valid UTF-8 string.

Because the spec does not define the semantics of the stream frames, blank node identifiers are not guaranteed to be unique across multiple stream frames. The consumer MAY choose to treat the blank nodes as unique across the stream (and thus treat all occurences of the identifier as a single node), or it MAY choose to treat them as unique only within a single stream frame. The consumer MAY use the [logical stream type](#logical-stream-types) to determine how to treat the blank nodes. The producer SHOULD specify in the documentation which strategy it uses.

!!! note

    If the stream is meant to represent a single RDF graph or dataset (flat RDF stream in RDF-STaX), then the blank node identifiers should be unique across the stream so that you can refer to them across stream frame boundaries. If the frames refer to different graphs or datasets (grouped RDF stream in RDF-STaX), then the blank node identifiers should be unique only within a single frame.

!!! note

    Many RDF libraries (e.g., RDF4J, Apache Jena) use internal identifiers for blank nodes, which can be used as the identifiers in Jelly streams. You can also use a different format, for example with shorter identifiers to preserve space.

#### Literals

RDF literals are represented using the `RdfLiteral` message ([reference](reference.md#rdfliteral)). The message has the following fields:

- `lex` (1) – the lexical form of the literal in UTF-8. This field is OPTIONAL and defaults to an empty string.
- `literalKind` oneof. At most one of the following fields MUST be set:
    - `langtag` (2) – UTF-8 language tag, indicating that the literal is a language-tagged string (has datatype IRI equal to `http://www.w3.org/1999/02/22-rdf-syntax-ns#langString`). The language tag SHOULD be a valid [BCP 47](https://tools.ietf.org/html/bcp47) language tag.
    - `datatype` (3) – 1-based index of the datatype in the [datatype lookup](#prefix-name-and-datatype-lookup-entries), indicating that the literal is a typed literal. The value of this field MUST be greater than 0 and it MUST correspond to a valid entry in the datatype lookup.

If no field in the `literalKind` oneof is set, then the literal MUST be interpreted as a simple literal (has datatype IRI equal to `http://www.w3.org/2001/XMLSchema#string`).

!!! note

    Using the default value of `0` for the `datatype` field is not allowed, in contrast to names and prefixes in RdfIri. This is because the `datatype` field itself is optional and the default value would be ambiguous.

#### Quoted triples (RDF-star)

RDF-star quoted triples are represented using the `RdfTriple` message ([reference](reference.md#rdftriple)). Quoted triples are encoded in the same manner as triple statements, with the only difference being that [repeated terms](#repeated-terms) MUST NOT be used in quoted triples. The consumer SHOULD throw an error if a repeated term is encountered in a quoted triple.

Quoted triples may be nested up to arbitrary depth. The consumer SHOULD throw an error if the depth of the nesting exceeds the capabilities of the implementation.

#### Graph nodes

Literal, IRI, and blank node values for graph nodes are encoded in the same manner as for the subject, predicate, and object terms.

The default graph node is represented using the `RdfDefaultGraph` message ([reference](reference.md#rdfdefaultgraph)). The message is empty and has no fields. The default graph node indicates that the triple is part of the default graph.

## Delimited variant of Jelly

!!! note

    Protobuf messages [are not delimited](https://protobuf.dev/programming-guides/techniques/#streaming), so if you write multiple messages to the same file / socket / byte stream, you need to add some kind of delimiter between them. Jelly uses the convention already implemented in some protobuf libraries of prepending a varint before the message, to specify the length of the message. 

A byte stream (or file) in the delimited variant MUST consist of a series of delimited `RdfStreamFrame` messages. A delimited message is a message that has a varint prepended before it, specifying the length of the message in bytes.

Implementing the delimited variant is OPTIONAL.

### Delimited variant implementations

The delimiting convention is implemented in Protobuf libraries for:

- C++: [delimited_message_util.cc](https://github.com/protocolbuffers/protobuf/blob/main/src/google/protobuf/util/delimited_message_util.cc)
- Java / Scala: [writeDelimitedTo](https://developers.google.com/protocol-buffers/docs/reference/java/com/google/protobuf/MessageLite#writeDelimitedTo-java.io.OutputStream-) and [parseDelimitedFrom](https://developers.google.com/protocol-buffers/docs/reference/java/com/google/protobuf/Parser#parseDelimitedFrom-java.io.InputStream-)

The JVM (Scala) implementation of Jelly also supports the delimited variant – [see the documentation]({{ jvm_link('user/reactive#byte-streams') }}).

## Internet media type and file extension

The RECOMMENDED media type for Jelly is `application/x-jelly-rdf`. The RECOMMENDED file extension is `.jelly`.

The files SHOULD be saved in the [delimited variant of Jelly](#delimited-variant-of-jelly).

## Implementations

*This section is not part of the specification.*

The following implementations of the Jelly serialization format specification are available:

- [Jelly-JVM (Scala) implementation]({{ jvm_link() }})
    - Specification version: 1.0.0
    - Implemented actors: producer, consumer
    - Conformance: full
    - Supported RDF libraries: [Apache Jena](https://jena.apache.org/), [RDF4J](https://rdf4j.org/)
