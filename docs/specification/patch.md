# Jelly RDF Patch format specification

!!! warning

    Jelly-Patch is an experimental serialization format. It is expected to stabilize in June 2025. Until then, the format may change in incompatible ways.

**This document is the specification of the Jelly RDF Patch format, also known as Jelly-Patch. It is intended for implementers of Jelly libraries and applications.** If you are looking for a user-friendly introduction to Jelly, see the [Jelly index page](index.md).

This document is accompanied by the [Jelly Protobuf reference](reference.md) and the Protobuf definition itself ([`patch.proto`]({{ git_proto_link('patch.proto') }})).

The following assumptions are used in this document:

- The Jelly-Patch format is based on [Jelly-RDF](serialization.md), version `{{ proto_version() }}`. All concepts, definitions, and Protobuf messages defined there apply also here, unless explicitly stated otherwise.
- The basis for the terms used is the RDF 1.1 specification ([W3C Recommendation 25 February 2014](https://www.w3.org/TR/2014/REC-rdf11-concepts-20140225/)).
- Additionally, the RDF 1.1 Turtle specification ([W3C Recommendation 25 February 2014](https://www.w3.org/TR/2014/REC-turtle-20140225/)) is used in parts as a basis for selected definitions.
- The RDF Patch specification document ([RDF Delta, Andy Seaborne](https://afs.github.io/rdf-delta/rdf-patch.html)) is used as the basis for RDF Patch concepts and definitions.
- In parts referring to RDF-star, the RDF-star draft specification ([W3C Community Group Draft Report 29 June 2023](https://w3c.github.io/rdf-star/cg-spec/editors_draft.html)) is used. As the scope in which the RDF-star specification is used here is minimal, later versions of the specification are expected to be compatible with this document.
- In parts referring to the RDF Stream Taxonomy (RDF-STaX), the [RDF-STaX version {{ stax_version() }} ontology]({{ stax_link('ontology') }}) and [taxonomy]({{ stax_link('taxonomy') }}) are used.
- All strings in the serialization are assumed to be UTF-8 encoded.

| Document information | |
| --- | --- |
| **Author:** | [Piotr Sowiński](https://ostrzyciel.eu) ([Ostrzyciel](https://github.com/Ostrzyciel)) |
| **Version:** | experimental (dev) |
| **Date:** | {{ git_revision_date_localized }} |
| **Permanent URL:** | [`https://w3id.org/jelly/{{ proto_version() }}/specification/serialization`](https://w3id.org/jelly/{{ proto_version() }}/specification/serialization) |
| **Document status**: | Experimental draft specification |
| **License:** | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

{% include "./snippets/start_info.md" %}

## Conformance

{% include "./snippets/conformance.md" %}

## Versioning

The protocol follows the [Semantic Versioning 2.0](https://semver.org/) scheme. Each MAJOR.MINOR semantic version corresponds to an integer version tag in the protocol. The version tag is encoded in the `version` field of the [`RdfPatchOptions`](reference.md#rdfpatchoptions) message. See also the [section on stream options](#stream-options) for more information on how to handle the version tags in serialized streams.

The following versions of the protocol are defined:

| Version tag | Semantic version    | Last release date                 | Changes                         |
| ----------- | ------------------- | --------------------------------- | ------------------------------- |
| 1           | 1.0.0               | Not released yet (experimental)   | (initial version)               |

!!! note
    
    Releases of the protocol are published on [GitHub](https://github.com/Jelly-RDF/jelly-protobuf/releases).

### Backward compatibility

{% include "./snippets/back_compat.md" %}

### Forward compatibility

{% include "./snippets/forward_compat.md" %}

!!! note

    See also the notes about the practical implications of this in the [Jelly-RDF specification](serialization.md#forward-compatibility).

## Actors and implementations

Jelly-Patch assumes there to be two actors involved in processing the stream: the producer (serializer) and the consumer (parser). The producer is responsible for serializing the RDF Patch data into the Jelly-Patch format, and the consumer is responsible for parsing the Jelly-Patch format into RDF Patch data.

Implementations may include only the producer, only the consumer, or both.

## Format specification

Jelly-Patch uses [Protocol Buffers version 3](https://protobuf.dev/programming-guides/proto3/) as the underlying serialization format. All implementations MUST use a compliant Protocol Buffers implementation. The Protocol Buffers schema for Jelly-Patch is defined in `patch.proto` ([source code]({{ git_proto_link('patch.proto') }}), [reference](reference.md#patchproto)).

The Jelly-Patch format describes a *stream* (i.e., and ordered sequence) of *patch frames*. The frames may be sent one-by-one using a dedicated streaming protocol (e.g., [gRPC](streaming.md), MQTT, Kafka) or written in sequence to a byte stream (e.g., a file or socket). When writing multiple to a byte stream, the frames MUST be delimited – see the [delimited variant](#delimited-variant).

The semantics of the patch frames (i.e., how should the frames be interpreted) are decided by the *[patch stream type](#patch-stream-types)*. The statements in the stream may be either RDF triples or quads, depending on the *[statement stream type](#statement-stream-types)*. Jelly-Patch uses the same compression mechanisms as [Jelly-RDF](serialization.md) to compress the statements.

### Patch frames

A patch frame is a message of type `RdfPatchFrame` ([reference](reference.md#rdfpatchframe)). The message has a field `rows`, which is a repeated field of type `RdfPatchRow` ([reference](reference.md#rdfpatchrow)). A patch frame may contain any number of rows, however it is RECOMMENDED to keep the size of the frames below 1 MB. Unlike Jelly-RDF, Jelly-Patch defines specific semantics for the patch frames using [patch stream types](#patch-stream-types).

#### Ordering

Patch frames MUST be processed strictly in order to preserve the semantics of the stream. Each patch frame MUST be processed in its entirety before the next patch frame is processed.

Implementations MAY choose to adopt a **non-standard** solution where the order or delivery of the frames is not guaranteed and the stream can be read in more than one order or without some frames. The implementation MUST clearly specify in the documentation that it uses such a non-standard solution.

!!! info

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

TODO

### Statement types

TODO

### Patch stream options

TODO

### Prefix, name, and datatype lookup entries

TODO

### RDF statements

TODO

#### Repeated terms

TODO

### RDF terms and graph nodes

TODO

TODO: refer to Jelly-RDF term encoding here

### Namespaces

TODO

### Transactions

TODO

### Headers

TODO

<!-- end of serialization format spec section -->

## Delimited variant

TODO

## Internet media type and file extension

TODO

## Security considerations

*This section is not part of the specification.*

TODO

## Implementations

*This section is not part of the specification.*

TODO
