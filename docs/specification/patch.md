# Jelly RDF Patch format specification

!!! warning

    Jelly-Patch is an experimental serialization format. It is expected to stabilize in June 2025. Until then, the format may change in incompatible ways.

**This document is the specification of the Jelly RDF Patch format, also known as Jelly-Patch. It is intended for implementers of Jelly libraries and applications.** If you are looking for a user-friendly introduction to Jelly, see the [Jelly index page](index.md).

!!! info

    It is highly recommended to first read the [RDF Patch specification](https://afs.github.io/rdf-delta/rdf-patch.html). Jelly-Patch is an implementation of RDF Patch built on top of [Jelly-RDF](serialization.md).

This document is accompanied by the [Jelly Protobuf reference](reference.md) and the Protobuf definition itself ([`patch.proto`]({{ git_proto_link('patch.proto') }})).

The following assumptions are used in this document:

- The Jelly-Patch format is based on [Jelly RDF serialization format](serialization.md), version `{{ proto_version() }}`. All concepts, definitions, and Protobuf messages defined there apply also here, unless explicitly stated otherwise.
- The basis for the terms used is the RDF 1.1 specification ([W3C Recommendation 25 February 2014](https://www.w3.org/TR/2014/REC-rdf11-concepts-20140225/)).
- Additionally, the RDF 1.1 Turtle specification ([W3C Recommendation 25 February 2014](https://www.w3.org/TR/2014/REC-turtle-20140225/)) is used in parts as a basis for selected definitions.
- The RDF Patch specification document ([RDF Delta, Andy Seaborne](https://afs.github.io/rdf-delta/rdf-patch.html)) is used as the basis for RDF Patch concepts and definitions.
- In parts referring to RDF-star, the RDF-star draft specification ([W3C Community Group Draft Report 29 June 2023](https://w3c.github.io/rdf-star/cg-spec/editors_draft.html)) is used. As the scope in which the RDF-star specification is used here is minimal, later versions of the specification are expected to be compatible with this document.
- All strings in the serialization are assumed to be UTF-8 encoded.

| Document information | |
| --- | --- |
| **Author:** | [Piotr Sowiński](https://ostrzyciel.eu) ([Ostrzyciel](https://github.com/Ostrzyciel)) |
| **Version:** | experimental (dev) |
| **Date:** | {{ git_revision_date_localized }} |
| **Permanent URL:** | [`https://w3id.org/jelly/{{ proto_version() }}/specification/patch`](https://w3id.org/jelly/{{ proto_version() }}/specification/patch) |
| **Document status**: | Experimental draft specification |
| **License:** | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

{% include "./includes/start_info.md" %}

## Conformance

{% include "./includes/conformance.md" %}

## Versioning

The protocol follows the [Semantic Versioning 2.0](https://semver.org/) scheme. Each MAJOR.MINOR semantic version corresponds to an integer version tag in the protocol. The version tag is encoded in the `version` field of the [`RdfPatchOptions`](reference.md#rdfpatchoptions) message. See also the [section on patch stream options](#patch-stream-options) for more information on how to handle the version tags in serialized streams.

The following versions of the protocol are defined:

| Version tag | Semantic version    | Last release date                 | Changes                         |
| ----------- | ------------------- | --------------------------------- | ------------------------------- |
| 1           | 1.0.0               | Not finalized yet (experimental)  | (initial version)               |

!!! note
    
    Releases of the protocol are published on [GitHub](https://github.com/Jelly-RDF/jelly-protobuf/releases).

### Backward compatibility

{% include "./includes/back_compat.md" %}

### Forward compatibility

{% include "./includes/forward_compat.md" %}

!!! note

    See also the notes about the practical implications of this in the [Jelly-RDF specification](serialization.md#forward-compatibility).

## Actors and implementations

Jelly-Patch assumes there to be two actors involved in processing the stream: the producer (serializer) and the consumer (parser). The producer is responsible for serializing the RDF Patch data into the Jelly-Patch format, and the consumer is responsible for parsing the Jelly-Patch format into RDF Patch data.

Implementations may include only the producer, only the consumer, or both.

## Format specification

Jelly-Patch uses [Protocol Buffers version 3](https://protobuf.dev/programming-guides/proto3/) as the underlying serialization format. All implementations MUST use a compliant Protocol Buffers implementation. The Protocol Buffers schema for Jelly-Patch is defined in `patch.proto` ([source code]({{ git_proto_link('patch.proto') }}), [reference](reference.md#patchproto)).

The Jelly-Patch format describes a *stream* (i.e., and ordered sequence) of *patch frames*. The frames may be sent one-by-one using a dedicated streaming protocol (e.g., [gRPC](streaming.md), MQTT, Kafka) or written in sequence to a byte stream (e.g., a file or socket). When writing multiple to a byte stream, the frames MUST be delimited – see the [delimited variant](#delimited-variant).

The semantics of the patch frames (i.e., how should the frames be interpreted) are decided by the *[patch stream type](#patch-stream-types)*. The statements in the stream may be either RDF triples or quads, depending on the *[statement stream type](#statement-types)*. Jelly-Patch uses the same compression mechanisms as [Jelly-RDF](serialization.md) to compress the statements.

### Patch frames

A patch frame is a message of type `RdfPatchFrame` ([reference](reference.md#rdfpatchframe)). The message has a field `rows`, which is a repeated field of type `RdfPatchRow` ([reference](reference.md#rdfpatchrow)). A patch frame may contain any number of rows, however it is RECOMMENDED to keep the size of the frames below 1 MB. Unlike Jelly-RDF, Jelly-Patch defines specific semantics for the patch frames using [patch stream types](#patch-stream-types).

#### Ordering

Patch frames MUST be processed strictly in order to preserve the semantics of the stream. Each patch frame MUST be processed in its entirety before the next patch frame is processed.

Implementations MAY choose to adopt a **non-standard** solution where the order or delivery of the frames is not guaranteed and the stream can be read in more than one order or without some frames. The implementation MUST clearly specify in the documentation that it uses such a non-standard solution.

!!! note

    See also the notes about the practical implications of this in the [Jelly-RDF specification](serialization.md#ordering).

### Patch rows

A patch row is a message of type `RdfPatchRow` ([reference](reference.md#rdfpatchrow)). It MUST have exactly one of the following fields set:

- `options` (1) – [patch options header](#patch-stream-options), indicating the patch stream type, statement type, compression options, and used RDF features.
- `statement_add` (2) – adding an [RDF statement](#rdf-statements) operation. Row type in RDF Patch: `A`.
- `statement_delete` (3) – deleting an [RDF statement](#rdf-statements) operation. Row type in RDF Patch: `D`.
- `namespace_add` (4) – addding a [namespace](#namespaces) operation. Row type in RDF Patch: `PA`.
- `namespace_delete` (5) – deleting a [namespace](#namespaces) operation. Row type in RDF Patch: `PD`.
- `transaction_start` (6) – starting a [transaction](#transactions). Row type in RDF Patch: `TX`.
- `transaction_commit` (7) – committing an ongoing [transaction](#transactions). Row type in RDF Patch: `TC`.
- `transaction_abort` (8) – aborting an ongoing [transaction](#transactions). Row type in RDF Patch: `TA`.
- `name` (11) – entry in the [name lookup](#prefix-name-and-datatype-lookup-entries).
- `prefix` (12) – entry in the [prefix lookup](#prefix-name-and-datatype-lookup-entries).
- `datatype` (13) – entry in the [datatype lookup](#prefix-name-and-datatype-lookup-entries).
- `header` (14) – RDF Patch [header row](#headers). Row type in RDF Patch: `H`.
- `punctuation` (15) – punctuation mark. It MUST NOT appear in streams of type other than `PUNCTUATED`.

Fields 9 and 10 are reserved for future use.

Fields 11, 12, 13 (lookup entries) do not correspond to any row type in RDF Patch. They are used by Jelly-Patch for compressing the IRIs and datatypes. Field 15 also does not correspond to any row type in RDF Patch. It is used for punctuation in the `PUNCTUATED` [patch stream type](#patch-stream-types), introduced by Jelly-Patch. Finally, field 1 is used for the [patch options header](#patch-stream-options), which is also specific to Jelly-Patch.

The remaining fields (2, 3, 4, 5, 6, 7, 8, 14) correspond directly to the listed row types in RDF Patch and MUST be interpreted as such.

### Patch stream types

The patch stream type MUST be explicitly specified in the [patch stream options](#patch-stream-options). The patch stream type is defined by the `PatchStreamType` enum ([reference](reference.md#patchstreamtype)). The following types are defined:

- `PATCH_STREAM_TYPE_UNSPECIFIED` (0) – default value. This patch stream type MUST NOT be used. Consumers SHOULD throw an error if this value is used.
- `PATCH_STREAM_TYPE_FRAME` (1) – every `RdfPatchFrame` message is a single, complete RDF Patch. In this stream type, transactions MUST NOT span multiple frames (see [Transactions](#transactions) for details). The stream MUST NOT contain any `RdfPatchRow` messages with the `punctuation` field set.
- `PATCH_STREAM_TYPE_FLAT` (2) – the entire stream is a single, complete RDF Patch. In this stream type, a transaction spanning multiple frames MUST be interpreted as a single transaction. The stream MUST NOT contain any `RdfPatchRow` messages with the `punctuation` field set.
- `PATCH_STREAM_TYPE_PUNCTUATED` (3) – the stream is a sequence of RDF Patches, marked by punctuation marks (`RdfPatchPunctuation` message). The punctuation mark MUST occur at the end of a patch frame. The punctuation mark MUST NOT be used in any other context.

!!! note "Stream types"

    The `FRAME` type is simple to use, but it requires you to fit the entire Patch inside a single frame. Because the contents of the frame are stored in memory as a whole, and because Protobuf implementations typically have strict limits on message sizes (~4 MB), this may not be possible for large patches. Therefore, we recommend using this stream type only if you are sure that the patches will always be small.

    The `FLAT` type is only appropriate if you want to store a single RDF patch in a byte stream.

    `PUNCTUATED` is the most flexible type, decoupling frames from logical patches. It allows you to send multiple patches in a single stream, and it allows you to send patches that are larger than the maximum frame size.

!!! note "Punctuated streams"

    Effectively, the punctuation mark must only be used to mark the end of an RDF Patch. So, if you start the stream with a punctuation mark, this would be interpreted as an empty RDF Patch.

### Statement types

The statement type MUST be explicitly specified in the [patch stream options](#patch-stream-options). The statement type is defined by the `PatchStatementType` enum ([reference](reference.md#patchstatementtype)). The following types are defined:

- `STATEMENT_TYPE_UNSPECIFIED` (0) – default value. This statement type MUST NOT be used. Consumers SHOULD throw an error if this value is used.
- `STATEMENT_TYPE_TRIPLES` (1) – in this case, the statements in the stream MUST be interpreted as RDF triples (graph is unspecified). The stream MUST NOT contain any `RdfQuad` or `RdfPatchNamespace` messages with the `graph` oneof set to any value.
- `STATEMENT_TYPE_QUADS` (2) – in this case, the statements in the stream MUST be interpreted as RDF quads. If the `graph` oneof in the `RdfQuad` or `RdfPatchNamespace` message is not set, it MUST be interpreted as a repeated graph term, in line with the [Jelly-RDF format specification](serialization.md#repeated-terms).

!!! note

    Statement types in Jelly-Patch work differently to [Jelly-RDF's physical stream types](serialization.md#physical-stream-types). Instead of restricting which types of messages are valid in the stream, we always use `RdfQuad`, and the statement type option simply tells us how to interpret the messages.

    Note that in the RDF 1.1 spec there is a clear difference between a "triple" and a "triple in the default graph" which would be a quad. A "triple" does not specify which graph it belongs to – it may be the default graph, or it may be a named graph. In practice, only some RDF implementations make the distinction between a triple and a triple in the default graph (e.g., Apache Jena). Others, like Eclipse RDF4J always assume that the triple is in the default graph.

### Patch stream options

The patch stream options is a message of type `RdfPatchOptions` ([reference](reference.md#rdfpatchoptions)). It MUST be the first row in the stream. It MAY appear more than once in the stream (also after other rows), but it MUST be identical to all previous occurrences. Consumers MAY throw an error if the patch stream options are not present at the start of the stream. Alternatively, they MAY use their own, implementation-specified default options. Consumers SHOULD NOT throw an error if the patch options are present more than once in the stream.

The patch stream options instruct the consumer of the stream (parser) on the used patch stream type, statement type, compression options, and RDF features.

The patch stream options message contains the following fields:

- `statement_type` (1) – the [statement type](#statement-types). This field is REQUIRED and it MUST be set to a value defined in the protocol other than `STATEMENT_TYPE_UNSPECIFIED`.
- `stream_type` (2) – the [patch stream type](#patch-stream-types). This field is REQUIRED and it MUST be set to a value defined in the protocol other than `PATCH_STREAM_TYPE_UNSPECIFIED`.
- `generalized_statements` (3) – whether the stream contains [generalized RDF triples or graphs](https://www.w3.org/TR/rdf11-concepts/#section-generalized-rdf). This field MUST be set to true if the stream contains generalized RDF triples or graphs. It SHOULD NOT be set to true if the stream does not use this feature. This field is OPTIONAL and defaults to false.
- `rdf_star` (4) – whether the stream uses [RDF-star](https://w3c.github.io/rdf-star/cg-spec/editors_draft.html) (quoted triples). This field MUST be set to true if the stream uses RDF-star. It SHOULD NOT be set to true if the stream does not use this feature. This field is OPTIONAL and defaults to false.
- `max_name_table_size` (9) – maximum size of the [name lookup](#prefix-name-and-datatype-lookup-entries). This field is REQUIRED and MUST be set to a value greater than or equal to 8. The size of the lookup MUST NOT exceed the value of this field.
- `max_prefix_table_size` (10) – maximum size of the [prefix lookup](#prefix-name-and-datatype-lookup-entries). This field is OPTIONAL and defaults to 0 (no lookup). If the field is set to 0, the prefix lookup MUST NOT be used in the stream. If the field is set to a positive value, the prefix lookup SHOULD be used in the stream and the size of the lookup MUST NOT exceed the value of this field.
- `max_datatype_table_size` (11) – maximum size of the [datatype lookup](#prefix-name-and-datatype-lookup-entries). This field is OPTIONAL and defaults to 0 (no lookup). If the field is set to 0, the datatype lookup MUST NOT be used in the stream (which effectively prohibits the use of datatype literals). If the field is set to a positive value, the datatype lookup SHOULD be used in the stream and the size of the lookup MUST NOT exceed the value of this field.
- `version` (15) – [version tag](#versioning) of the stream. This field is REQUIRED.
    - The version tag is encoded as a varint. The version tag MUST be greater than 0.
    - The producer of the stream MUST set the version tag to the version tag of the protocol that was used to serialize the stream.
    - It is RECOMMENDED that the producer uses the lowest possible version tag that is compatible with the features used in the stream.
    - The consumer SHOULD throw an error if the version tag is greater than the version tag of the implementation.
    - The consumer SHOULD throw an error if the version tag is zero.
    - The consumer SHOULD NOT throw an error if the version tag is not zero but lower than the version tag of the implementation.
    - The producer may use version tags greater than 10000 to indicate non-standard versions of the protocol.

### Prefix, name, and datatype lookup entries

Jelly-Patch uses the same IRI and datatype compression mechanism as [Jelly-RDF](serialization.md#prefix-name-and-datatype-lookup-entries). All rules specified for Jelly-RDF also apply here.

### RDF statements

Add and delete operations on RDF statements (`A` and `D` in RDF Patch) are always encoded as `RdfQuad` messages ([reference](reference.md#rdfquad)). The interpretation of `RdfQuad` messages depends on the [statement type](#statement-types) specified in the [patch stream options](#patch-stream-options):

- `STATEMENT_TYPE_TRIPLES` – the `graph` oneof MUST NOT be set. If it is set, the consumer SHOULD ignore the graph term and MAY throw an error. The `RdfQuad` message MUST be interpreted as an RDF triple. The `subject`, `predicate`, and `object` oneofs MUST be set, unless a repeated term is used (see: [Repeated terms](#repeated-terms)).
- `STATEMENT_TYPE_QUADS` – the `RdfQuad` message MUST be interpreted as an RDF quad. The `subject`, `predicate`, `object`, and `graph` oneofs MUST be set, unless a repeated term is used (see: [Repeated terms](#repeated-terms)).

#### Repeated terms

Jelly-Patch uses the same repeated term encoding as [Jelly-RDF](serialization.md#repeated-terms) for `RdfQuad` messages. The only difference is in handling the `graph` oneof in streams with type `STATEMENT_TYPE_TRIPLES`, where the `graph` oneof MUST NOT be set and is not used for repeated term encoding.

In Jelly-Patch, the type of the operation (add or delete) does not affect the repeated term encoding. An empty term in a `RdfQuad` message MUST be interpreted as a repeated term from the last `RdfQuad` or `RdfNamespaceDeclaration` (in case of `graph`) message in the stream, regardless of whether both operations are of the same type (add and add, or delete and delete) or not (add and delete, or delete and add).

### Namespaces

Add and delete operations of namespace declarations (`PA` and `PD` in RDF Patch) are encoded as `RdfPatchNamespace` messages ([reference](reference.md#rdfpatchnamespace)). The `RdfPatchNamespace` message contains the following fields:

- `name` (1) – the short name of the namespace, encoded in UTF-8. It SHOULD conform to the [`PN_PREFIX` production in RDF 1.1 Turtle](https://www.w3.org/TR/2014/REC-turtle-20140225/#grammar-production-PN_PREFIX). Note that the `:` character (colon) is not part of the name. An empty string (the default value) is allowed.
- `value` (2) – the IRI of the namespace as an `RdfIri` message. This field is REQUIRED for the namespace add operation (`PA`) and OPTIONAL for the namespace delete operation (`PD`).
- `graph` oneof (3–6, fields `g_iri`, `g_bnode`, `g_default_graph`, `g_literal`) – the graph term of the namespace declaration.

The `graph` oneof follows the [Jelly-RDF graph node encoding](serialization.md#rdf-terms-and-graph-nodes). The `graph` oneof MUST NOT be set to any value in streams with type `STATEMENT_TYPE_TRIPLES`. In streams with type `STATEMENT_TYPE_QUADS`, the `graph` oneof MUST be set to one of the possible values, unless a repeated term is used (see: [Repeated terms](#repeated-terms)).

In repeated term encoding, the `graph` oneof of `RdfPatchNamespace` MUST be interpreted in the same manner as if it appeared in a `RdfQuad` message. When `STREAM_TYPE_QUADS` is used and the `graph` oneof is not set to any value, it MUST be interpreted as a repeated graph term from the last `RdfQuad` or `RdfNamespaceDeclaration` message in the stream, regardless of whether both operations are of the same type (add and add, or delete and delete) or not (add and delete, or delete and add).

!!! note "Graph names in namespace declarations"

    The original [RDF Patch spec](https://afs.github.io/rdf-delta/rdf-patch.html) does not mention graph names in namespace declarations, but this feature is implemented in Apache Jena. This is useful for exact 1:1 RDF dataset replication in systems that store namespace mappings per graph, not per dataset.

    If your system does not support this, in `TRIPLES` streams you should simply ignore the graph name, and in `QUADS` streams, set it to `g_default_graph`.

!!! note "Repeated terms and namespace declarations"

    In Jelly-Patch the type of the operation (add or delete) does not influence the repeated term encoding – in implementations you should use the same "last term" data structure for both. The same applies to the `graph` oneof in `RdfPatchNamespace` messages – its last value should be shared with quads.

### Transactions

Transaction operations (`TX`, `TC`, `TA` rows in RDF Patch) are encoded as `RdfPatchTransactionStart` ([reference](reference.md#rdfpatchtransactionstart)), `RdfPatchTransactionCommit` ([reference](reference.md#rdfpatchtransactioncommit)), and `RdfPatchTransactionAbort` ([reference](reference.md#rdfpatchtransactionabort)) messages, respectively. Each of these messages defines no fields.

Using transactions in the stream is OPTIONAL and the semantics of transactions are not defined by Jelly-Patch. Users are therefore free to use headers and operations on namespaces and statements within or outside of transactions, depending on their use case.

Jelly-Patch restricts the syntax of transactions to the following:

- We define "the previous transaction operation" as the last encountered row in the stream until a given point with row type `transaction_start`, `transaction_commit` or `transaction_abort`. If there were no transaction operations in the stream until this point, the previous transaction operation is undefined.
- A row with a `transaction_commit` or `transaction_abort` operation MUST have a previous transaction operation equal to `transaction_start`. If there is no previous transaction operation, the consumer MAY throw an error. If there is a previous transaction operation that is a `transaction_commit` or `transaction_abort`, the consumer MAY throw an error.
- A row with a `transaction_start` operation MUST have a previous transaction operation that is either undefined or equal to `transaction_commit` or `transaction_abort`. If there is a previous transaction operation that is a `transaction_start`, the consumer MAY throw an error.
- In stream type `PATCH_STREAM_TYPE_FRAME`, transactions MUST NOT span multiple patch frames. The transaction start and commit/abort messages MUST be in the same frame.
- A patch frame may contain multiple transactions, regardless of the used stream type.

!!! note "Transaction syntax and semantics"

    Jelly-Patch only restricts the semantics of transactions, so that the only valid sequences of transaction operations are `TX ... TC` and `TX ... TA` – no nesting, no double-aborting, and no double-committing.

    The semantics of these operations are not defined by Jelly-Patch. [RDF Patch](https://afs.github.io/rdf-delta/rdf-patch.html) contains more restrictions on transactions (e.g., headers must be at the beginning of the patch and outside the transaction), but these are not enforced by Jelly-Patch. The semantics are still not defined there, so you are free to use transactions in any way you like.

### Headers

Headers (`H` row in RDF Patch) are encoded as `RdfPatchHeader` messages ([reference](reference.md#rdfpatchheader)). The `RdfPatchHeader` message contains the following fields:

- `key` (1) – the key of the header, encoded in UTF-8. An empty string (the default value) is allowed.
- `value` oneof (2–5, fields `h_iri`, `h_bnode`, `h_literal`, `h_triple_term`) – the value of the header. The value is encoded as [an RDF term](#rdf-terms-and-graph-nodes). The `value` oneof MUST be set to one of the possible values.

Repeated term encoding MUST NOT be used for the `value` oneof in the `RdfPatchHeader` message ([reference](reference.md#rdfpatchheader)). The `value` oneof MUST always be set to a single value.

### RDF terms and graph nodes

Jelly-Patch uses the same RDF term and graph node encoding as [Jelly-RDF](serialization.md#rdf-terms-and-graph-nodes).

RDF term encoding is also used for the `h_iri`, `h_bnode`, `h_literal`, and `h_triple_term` fields in the `value` oneof of the `RdfPatchHeader` message ([reference](reference.md#rdfpatchheader)).

RDF graph node encoding is also used for the `g_iri`, `g_bnode`, `g_default_graph`, and `g_literal` fields in the `graph` oneof of the `RdfPatchNamespace` message ([reference](reference.md#rdfpatchnamespace)). Additionally, RDF IRI encoding [defined in Jelly-RDF](serialization.md#iris) is used for the `value` field in the `RdfPatchNamespace` message.

The same rules about the order of processing RDF IRIs, RDF terms, RDF graph nodes, and their lookup references also apply here. The terms and graph nodes present in `RdfPatchHeader` and `RdfPatchNamespace` messages MUST be processed as if they were present in the `RdfQuad` messages, in the order in which their rows appear in the stream. In `RdfPatchNamespace`, the IRI in the `value` field MUST be processed before the RDF term in the `graph` oneof.

??? example "Example of RDF term encoding in Jelly-Patch (click to expand)"

    This basically means that you should treat terms in headers and namespaces in the same way as those in quad statements. The only difference is that for the `value` oneof in `RdfPatchHeader` there is no repeated term encoding, so it always must be set to some value.

    In this example the comments indicate equivalent RDF Patch rows in the stream, assuming the statement type is set to `STATEMENT_TYPE_QUADS`.

    ```protobuf
    # H id <http://example.org/iri>
    rows {
        prefix {
            id: 0 # default value, interpreted as 1
            prefix: "http://example.org/"
        }
    }
    rows {
        name {
            id: 0 # default value, interpreted as 1
            name: "iri"
        }
    }
    rows {
        header {
            h_iri {
                prefix_id: 1
                name_id: 0 # default value, interpreted as 1
            }
        }
    }

    # PA "ex" <http://example.org/> <http://example.org/graph> .
    rows {
        name {
            id: 0 # default value, interpreted as 1
            name: "" # empty string
        }
    }
    rows {
        name {
            id: 0 # default value, interpreted as 1
            name: "graph"
        }
    }
    rows {
        namespace_add {
            name: "ex"
            value {
                prefix_id: 0 # default value, interpreted as 1
                name_id: 0 # default value, interpreted as 1+1=2
                # because last name_id in h_iri was 0 interpreted as 1
            }
            g_iri {
                prefix_id: 0 # default value, interpreted as 1
                name_id: 0 # default value, interpreted as 2+1=3
            }
        }
    }

    # A _:b1 <http://example.org/iri> _:b2 <http://example.org/graph> .
    rows {
        statement_add {
            s_bnode: "b1"
            p_iri {
                prefix_id: 0 # default value, interpreted as 1
                name_id: 1 # interpreted as 1
            }
            o_bnode: "b2"
            # ((graph oneof not set))
            # This is interpreted as repeating the graph term
            # from the PA row above.
        }
    }
    ```

<!-- end of serialization format spec section -->

## Delimited variant

A byte stream (or file) in the delimited variant MUST consist of a series of delimited `RdfPatchFrame` messages. A delimited message is a message that has a Protobuf varint prepended before it, specifying the length of the message in bytes.

!!! note

    See also notes about the delimited variant in the [Jelly-RDF specification](serialization.md#delimited-variant-of-jelly).

## Internet media type and file extension

The RECOMMENDED media type for Jelly is `application/x-jelly-rdf-patch`. The RECOMMENDED file extension is `.jellyp`.

The files SHOULD be saved in the [delimited variant of Jelly-Patch](#delimited-variant).

## Security considerations

*This section is not part of the specification.*

The same security considerations apply to Jelly-Patch as to Jelly-RDF. Please refer to the [Jelly-RDF specification](serialization.md#security-considerations) for more information.

## Implementations

*This section is not part of the specification.*

The following implementations of the Jelly-Patch specification are available:

- [Jelly-JVM implementation]({{ jvm_link() }})
    - Specification version: {{ proto_version() }}
    - Implemented actors: producer, consumer
    - Conformance: full
    - Supported RDF libraries: [Apache Jena](https://jena.apache.org/), [RDF4J](https://rdf4j.org/)
