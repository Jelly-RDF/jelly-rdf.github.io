# Jelly RDF serialization format specification

**This document is the specification of the Jelly RDF serialization format, also known as Jelly-RDF, version 1.2. It is intended for implementers of Jelly libraries and applications.** If you are looking for a user-friendly introduction to Jelly, see the [Jelly index page](index.md).

This document is accompanied by the [Jelly Protobuf reference](reference.md) and the Protobuf definition itself ([`rdf.proto`]({{ git_proto_link('rdf.proto') }})).

!!! info "Jelly-RDF 1.0 and 1.1"

    This document describes only Jelly-RDF 1.2. Jelly-RDF 1.0.x and 1.1.x store the stream frames differently (in the *row layout*), as described in the **[Jelly-RDF 1.1 specification]({{ rdf_1_1_link() }})**. See the [Earlier versions](#earlier-versions) section for more details.

The following assumptions are used in this document:

- The basis for the terms used is the RDF 1.2 Concepts and Abstract Data Model specification ([W3C Candidate Recommendation Snapshot 07 April 2026](https://www.w3.org/TR/rdf12-concepts/)). The format also supports RDF 1.1 – see [RDF version](#rdf-version).
- Additionally, the RDF 1.2 Turtle specification ([W3C Working Draft 07 October 2026](https://www.w3.org/TR/rdf12-turtle/)) is used in parts as a basis for selected definitions.
- In parts referring to RDF Messages, the [latest version of the RDF Messages specification](https://w3c-cg.github.io/rsp/spec/messages) is used.
- All strings in the serialization are assumed to be UTF-8 encoded.

| Document information | |
| --- | --- |
| **Authors:** | [Piotr Sowiński](https://ostrzyciel.eu) ([Ostrzyciel](https://github.com/Ostrzyciel)), Anastasiya Danilenka ([adanilenka](https://github.com/adanilenka)) |
| **Version:** | {{ proto_version() }} |
| **Date:** | {{ git_revision_date_localized }} |
| **Permanent URL:** | [`https://w3id.org/jelly/{{ proto_version() }}/specification/serialization`](https://w3id.org/jelly/{{ proto_version() }}/specification/serialization) |
| **Document status**: | {{ specification_status() }} |
| **License:** | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

{% include "./includes/start_info.md" %}

## Conformance

{% include "./includes/conformance.md" %}

To claim conformance with this specification, an implementation MUST pass all applicable tests from the [Jelly-RDF conformance test suite](../conformance/rdf-test-cases.md) (and, for reading Jelly-RDF 1.0 and 1.1 streams, from the [Jelly-RDF 1.1 test suite](../conformance/rdf-1-1-test-cases.md)), and MUST provide a conformance report as described on the [reporting conformance](../conformance/reporting-conformance.md) page. Implementations SHOULD pass the conformance tests marked with the `SHOULD` conformance level (`jellyt:featureShouldLevel`).

!!! note

    Conformance tests are a way to verify that implementations correctly follow the specification. However, passing all tests does not guarantee that the implementation perfectly implements the specification, is free of bugs, or that it will work in all scenarios.

    Implementations typically also employ extensive unit tests, integration tests, and other quality assurance measures to ensure correctness and reliability.


## Versioning

The protocol follows the [Semantic Versioning 2.0](https://semver.org/) scheme. Each MAJOR.MINOR semantic version corresponds to an integer version tag in the protocol. The version tag is encoded in the `version` field of the [`RdfStreamOptions`](reference.md#rdfstreamoptions) message. See also the [section on the version tag](#version-tag) for more information on how to handle the version tags in serialized streams.

The following versions of the protocol are defined:

| Version tag | Semantic version    | Release date                      | Changes                         |
| ----------- | ------------------- | --------------------------------- | ------------------------------- |
| 1           | 1.0.x               | August 24, 2024                   | (initial version)               |
| 2           | 1.1.0 | December 21, 2024 | Added `RdfNamespaceDeclaration` |
| 2           | 1.1.1 | March 10, 2025 | Added `RdfStreamFrame.metadata` |
| 2           | 1.1.2 | June 12, 2025 | Bugfixes: [#35](https://github.com/Jelly-RDF/jelly-rdf.github.io/pull/35), [#43](https://github.com/Jelly-RDF/jelly-rdf.github.io/pull/43), [#44](https://github.com/Jelly-RDF/jelly-rdf.github.io/pull/44) |
| 2           | 1.1.3 | September 30, 2025 | Added the conformance test suite |
| 3           | 1.2.0 **(current)** | October 23, 2026 | New column layout of stream frames, RDF 1.2, RDF Messages, concatenable streams. See [changes from Jelly-RDF 1.1](#changes-from-jelly-rdf-11). |

!!! note
    
    Releases of the protocol are published on [GitHub](https://github.com/Jelly-RDF/jelly-protobuf/releases).

### Earlier versions

Streams with version tag 1 or 2 (Jelly-RDF 1.0.x and 1.1.x) use the *row layout*, in which a stream frame is a list of rows, containing statements and lookup entries. Streams with version tag 3 (Jelly-RDF 1.2.x) use the *column layout* described in this document. Both layouts use the same Protobuf messages for stream frames and stream options, so a consumer can determine which layout is in use by examining the `version` field of the [stream options](#stream-options).

- If the stream options of a stream have version tag 1 or 2, the consumer MUST read the stream as described in the [Jelly-RDF 1.1 specification]({{ rdf_1_1_link() }}). This document does not apply to such a stream.
- A producer MAY write a stream with version tag 1 or 2, for example so that consumers that support only Jelly-RDF 1.0 or 1.1 can read it. It MUST then follow the [Jelly-RDF 1.1 specification]({{ rdf_1_1_link() }}), and this document does not apply to that stream.
- In a stream with version tag 1 or 2, the fields added in Jelly-RDF 1.2 MUST NOT be set: `RdfStreamFrame.columns`, `RdfStreamOptions.stream_type`, `RdfStreamOptions.rdf_version`, and `RdfLiteral.direction`. The consumer MAY ignore these fields if they are set.

Following the [backward compatibility](#backward-compatibility) rules, a consumer that fully implements this specification MUST be able to read streams with version tags 1 and 2.

### Backward compatibility

{% include "./includes/back_compat.md" %}

### Forward compatibility

{% include "./includes/forward_compat.md" %}

!!! note

    In practical terms, new MINOR versions of the protocol introduce features that previous implementations do not know how to handle. Implementations will generally refuse to read a stream that is marked as using a higher protocol version than they support (see: [version tag](#version-tag)).

!!! note "Forward-compatible features"
    
    Protobuf allows for adding new fields to messages without breaking compatibility with older implementations – they will simply ignore the new field. An example of this is the `metadata` field in the `RdfStreamFrame` message, which was added in version 1.1.1. Implementations of version 1.1.0 ignore it.

## Actors and implementations

Jelly-RDF assumes there to be two actors involved in processing the stream: the producer (serializer) and the consumer (parser). The producer is responsible for serializing the RDF data into the Jelly format, and the consumer is responsible for parsing the Jelly format into RDF data.

Implementations may include only the producer, only the consumer, or both.

## Format specification

The Jelly RDF serialization format uses [Protocol Buffers version 3](https://protobuf.dev/programming-guides/proto3/) as the underlying serialization format. All implementations MUST use a compliant Protocol Buffers implementation. The Protocol Buffers schema for Jelly serialization is defined in `rdf.proto` ([source code]({{ git_proto_link('rdf.proto') }}), [reference](reference.md#rdfproto)).

The Jelly-RDF format describes a *stream* (i.e., an ordered sequence) of *stream frames*. The frames may be sent one-by-one using a dedicated streaming protocol (e.g., [gRPC](streaming.md), MQTT, Kafka) or written in sequence to a byte stream (e.g., a file or socket). When writing multiple frames to a byte stream, the frames MUST be delimited – see the [delimited variant](#delimited-variant-of-jelly).

A stream contains RDF statements: triples or quads, depending on the [physical stream type](#physical-stream-types). The whole stream is either one RDF graph or dataset, or a sequence of RDF Messages, depending on the [stream type](#stream-types).

Within a frame, the RDF terms of statements are stored in columns: all subjects of the frame in one column, then all predicates, all objects, and all graph names. Within a column, the values of each type of RDF term are stored in their own flat lists. IRIs and datatypes are compressed using [lookup tables](#prefix-name-and-datatype-lookup-entries).

!!! note "Why columns?"

    In a row-oriented layout, every term needs its own length-delimited sub-message with a `oneof` selecting the term type, which costs additional bytes on the wire and memory on the consumer's side. Grouping the values of one position in a column lets us amortize this cost. If all values in a column are of the same type, there is no additional cost, and 2 bits per value otherwise (see [term types](#term-types)). Values that repeat in consecutive statements (e.g., the same subject or graph) can be compressed efficiently (see [sequence layout](#sequence-layout)), and a consumer can keep the values of a column in primitive arrays.

!!! note "Messages used only by Jelly-RDF 1.0 and 1.1"

    `rdf.proto` also contains messages used only by the row layout of Jelly-RDF 1.0.x and 1.1.x (and by [Jelly-Patch](patch.md)): `RdfTriple`, `RdfQuad`, `RdfGraphStart`, `RdfGraphEnd`, `RdfDefaultGraph`, `RdfNameEntry`, `RdfPrefixEntry`, `RdfDatatypeEntry`, `LogicalStreamType`, and all fields of `RdfStreamRow` except `options`. They are not used in Jelly-RDF 1.2 streams and are not described in this document.

### Stream types

The stream type indicates whether the stream is one RDF graph or dataset, or a sequence of RDF Messages. It is set in the `stream_type` field (5) of the [stream options](#stream-options), as an [`RdfStreamType`](reference.md#rdfstreamtype) value:

- `RDF_STREAM_TYPE_FLAT` (0) – default value. The entire stream is one RDF graph (physical type `TRIPLES`) or one RDF dataset (physical type `QUADS`). [Blank node labels](#blank-nodes) are scoped to the whole stream. [Message boundaries](#message-boundaries) MUST NOT be used. The consumer SHOULD throw an error otherwise.
- `RDF_STREAM_TYPE_MESSAGES` (1) – the stream is an [RDF Message Stream or RDF Message Log](https://w3c-cg.github.io/rsp/spec/messages). Each message is an RDF graph (physical type `TRIPLES`) or an RDF dataset (physical type `QUADS`). The messages are delimited by [message boundaries](#message-boundaries). [Blank node labels](#blank-nodes) are scoped to one message. The lookup tables and the [namespace declarations](#namespace-declarations) are kept from one message to the next.

An RDF Message is a unit of RDF data, as defined by the [RDF Messages specification](https://w3c-cg.github.io/rsp/spec/messages). One RDF Message may span many [stream frames](#stream-frames), and one frame may contain many RDF Messages.

Support for the `RDF_STREAM_TYPE_MESSAGES` stream type is OPTIONAL. A consumer that does not support it SHOULD throw an error when it reads stream options with this stream type.

Consumers MUST throw an error if the stream type has a value that is not listed above.

### Stream frames

A stream frame is a message of type `RdfStreamFrame` ([reference](reference.md#rdfstreamframe)). It has the following fields:

- `rows` (1) – either empty, or exactly one [`RdfStreamRow`](reference.md#rdfstreamrow) message with the `options` field set, containing the [stream options](#stream-options). The consumer SHOULD throw an error if `rows` contains more than one row, or a row with a field other than `options` set.
- `columns` (2) – the contents of the frame, as an [`RdfColumnBatch`](reference.md#rdfcolumnbatch) message – see [column batches](#column-batches). This field is OPTIONAL. A frame without it contains no statements.
- `metadata` (15) – [stream frame metadata](#stream-frame-metadata).

If the frame has the stream options, they MUST be processed before the column batch of the same frame.

A frame that has no rows and no column batch is an *empty frame*. Empty frames are valid, and have no effect on the RDF data.

A stream frame may contain any number of statements, however it is RECOMMENDED to keep the serialized size of the frames below 1 MB.

The frames have no meaning of their own – they are purely a batching mechanism. In particular, in a stream of RDF Messages, the frame boundaries are not message boundaries: the messages are delimited explicitly (see [message boundaries](#message-boundaries)).

!!! note

    Because a frame is just a batch of statements, the producer is free to choose the batch size. The producer may also have to end a frame early, when the [lookup tables fill up](#the-working-set-of-a-batch).

#### Ordering

Stream frames MUST be processed strictly in order to preserve the semantics of the stream. Each stream frame MUST be processed in its entirety before the next stream frame is processed.

Implementations MAY choose to adopt a **non-standard** solution where the order or delivery of the frames is not guaranteed and the stream can be read in more than one order or without some frames. The implementation MUST clearly specify in the documentation that it uses such a non-standard solution.

!!! note

    An example where not adhering to the strict ordering may be useful is when you are dealing with a network streaming protocol that does not guarantee the order of the messages (e.g., MQTT).

!!! note "Making frames independently decodable"

    The main thing you will need to worry about is the state of the lookup tables. If you can, emit all lookup entries at the beginning of the stream. When using stream partitions (e.g., in Kafka), you should ensure that the lookup entries are emitted to each partition. Alternatively, you can transmit the lookup entries separately from the stream.

    Because the [IRI inference state resets per column, per batch](#iris), a frame can be decoded using only the stream options and the state of the lookup tables. A producer that re-emits all the lookup entries it needs in **every** frame makes each frame decodable on its own, given the stream options. This costs space, allows for building a stream whose frames can be dropped or processed out of order.

#### Stream frame metadata

`RdfStreamFrame` messages have a `metadata` field (15) of type `map<string, bytes>`. This field is OPTIONAL and does not influence the processing of RDF data in any manner. The keys and values in the map are arbitrary and implementation-defined.

Consumers SHOULD ignore unknown keys in the metadata map. Consumers also SHOULD validate the values in the metadata map to ensure that they follow the expected format. Consumers MUST NOT assume that values are character strings or that they are valid UTF-8.

!!! note

    The metadata field is intended for use cases where additional information about the stream frame must be attached directly to the stream, but not as part of the RDF stream itself. For example, you could use it to store the timestamp of the frame, its unique identifier, hash code, or anything else relevant to your use case.

    You can use the metadata to store UTF-8 strings, numbers, or even nested protobuf messages. Because of this, you should never assume that the value is a valid string. Always validate the value before using it.

### Stream options

The stream options is a message of type `RdfStreamOptions` ([reference](reference.md#rdfstreamoptions)), stored in the `rows` field of a stream frame. It communicates to the consumer the type of the stream, RDF features used in it, sizes of the lookup tables needed to decode it, and the version of the protocol.

The producer MUST put the stream options in the first non-empty frame of the stream, that is, the first frame that has rows or a column batch. A later frame MAY [restate the stream options](#restating-the-stream-options).

The consumer MAY throw an error if a column batch is encountered before any stream options. Alternatively, it MAY use its own, implementation-specified default options.

The stream options message contains the following fields:

- `stream_name` (1) – name of the stream. This field is OPTIONAL and the manner in which it should be used is not defined by this specification. It MAY be used to identify the stream.
- `physical_type` (2) – [physical type of the stream](#physical-stream-types). This field is REQUIRED.
- `generalized_statements` (3), `rdf_star` (4), and `logical_type` (14) – these fields are used only in Jelly-RDF 1.0.x and 1.1.x. They MUST NOT be set (i.e., they must have their default values). The consumer SHOULD throw an error if any of them is set.
- `stream_type` (5) – the [stream type](#stream-types). This field is OPTIONAL and defaults to `RDF_STREAM_TYPE_FLAT`.
- `rdf_version` (6) – the [version of RDF](#rdf-version) whose terms may occur in the stream. This field is OPTIONAL and defaults to `RDF_VERSION_UNSPECIFIED`.
- `max_name_table_size` (9) – maximum size of the [name lookup](#prefix-name-and-datatype-lookup-entries). This field is REQUIRED and MUST be set to a value greater than or equal to 128. The consumer SHOULD throw an error otherwise. The size of the name lookup MUST NOT exceed the value of this field.
- `max_prefix_table_size` (10) – maximum size of the [prefix lookup](#prefix-name-and-datatype-lookup-entries). This field is OPTIONAL and defaults to 0 (no lookup). If the field is set to 0, the prefix lookup MUST NOT be used in the stream, and the consumer SHOULD throw an error if it is. If the field is set to a positive value, the prefix lookup SHOULD be used in the stream and the size of the prefix lookup MUST NOT exceed the value of this field.
- `max_datatype_table_size` (11) – maximum size of the [datatype lookup](#prefix-name-and-datatype-lookup-entries). This field is OPTIONAL and defaults to 0 (no lookup). If the field is set to 0, the datatype lookup MUST NOT be used in the stream, which effectively prohibits the use of datatype literals. The consumer SHOULD throw an error if it is used. If the field is set to a positive value, the datatype lookup SHOULD be used in the stream and the size of the lookup MUST NOT exceed the value of this field.
- `version` (15) – [version tag](#version-tag) of the stream. This field is REQUIRED. For streams that follow this specification, it MUST be set to 3.

This specification sets no upper bound on the lookup table sizes. Instead, each consumer SHOULD define the largest tables it is willing to allocate and reject a stream that asks for more – see [security considerations](#overly-large-lookup-tables). The RECOMMENDED defaults are **16384** names, **4096** prefixes, and **256** datatypes, and consumers SHOULD let the user raise or lower them.

#### Version tag

The following rules apply to the `version` field of the stream options:

- The version tag is encoded as a varint. The version tag MUST be greater than 0.
- The producer of the stream MUST set the version tag to the version tag of the protocol that was used to serialize the stream.
- The consumer SHOULD throw an error if the version tag is greater than the version tag of the implementation.
- The consumer SHOULD throw an error if the version tag is zero.
- The consumer SHOULD NOT throw an error if the version tag is not zero but lower than the version tag of the implementation.
- The producer may use version tags greater than 10000 to indicate non-standard versions of the protocol.

Streams with version tags 1 and 2 are read as described in [earlier versions](#earlier-versions).

#### Restating the stream options (stream concatenation) { #restating-the-stream-options }

A frame after the first non-empty frame MAY contain the stream options again. This is called *restating* the stream options. It makes Jelly-RDF 1.2 and newer streams concatenable: a Jelly-RDF file can be appended to another one with the same physical type and stream type without changes, and the result is a valid stream. The other options of the two files, such as the lookup table sizes or the RDF version, may differ. Jelly-RDF 1.0 and 1.1 files cannot be concatenated with Jelly-RDF 1.2 files.

Restating the stream options has the following effects, which take place before the column batch of the same frame is processed:

- The name, prefix, and datatype lookups are emptied, and their identifier numbering restarts from 1, as at the start of the stream.
- In a [stream of RDF Messages](#stream-types), the current message ends, as it would at the end of the stream (see [message boundaries](#message-boundaries)).

[Namespace declarations](#namespace-declarations) are **not** reset – they stay in effect. In a `FLAT` stream, [blank node labels](#blank-nodes) are **not** reset either – a label refers to the same blank node before and after the restated options, as when concatenating N-Triples files.

The `physical_type` and `stream_type` fields MUST have the same values in all stream options of a stream. The consumer SHOULD throw an error otherwise. The other fields may differ from the previous stream options, and apply to the frames that follow, until the stream options are restated again. The restated stream options MUST be valid on their own. The consumer MAY throw an error if it does not support the new options (e.g., because they ask for too large lookup tables).

!!! note

    Restating the stream options is **not** a way for a consumer to join a stream that is already in progress. If you want frames that can be decoded independently, see the [note on independently decodable frames](#ordering) instead.

### Physical stream types

The physical type of the stream MUST be explicitly specified in the [stream options](#stream-options). The following types are defined in the `PhysicalStreamType` enum ([reference](reference.md#physicalstreamtype)):

- `PHYSICAL_STREAM_TYPE_UNSPECIFIED` (0) – default value. This physical stream type MUST NOT be used. Consumers MUST throw an error if this value is used.
- `PHYSICAL_STREAM_TYPE_TRIPLES` (1) – stream of [RDF triples](https://www.w3.org/TR/rdf12-concepts/#section-triples). In this case, the column batches MUST NOT have the `graphs` column set. The consumer SHOULD throw an error otherwise.
- `PHYSICAL_STREAM_TYPE_QUADS` (2) – stream of RDF quads: triples, each in the default graph or in a named graph. See [column batches](#column-batches) for how the graphs are encoded.
- `PHYSICAL_STREAM_TYPE_GRAPHS` (3) – used only in Jelly-RDF 1.0.x and 1.1.x. This physical stream type MUST NOT be used. Consumers MUST throw an error if this value is used.

Consumers MUST throw an error if the physical stream type has a value that is not listed above.

!!! note

    In Jelly-RDF 1.1, the `GRAPHS` type was used to send triples grouped by graph. In Jelly-RDF 1.2, use `QUADS` instead.

### RDF version

The `rdf_version` field (6) of the [stream options](#stream-options) announces which RDF terms may occur in the stream. Its values follow the [version labels of RDF 1.2](https://www.w3.org/TR/rdf12-concepts/#defined-version-labels):

| `RdfVersion` value            | Version label | Base directions | Triple terms |
| ----------------------------- | ------------- | --------------- | ------------ |
| `RDF_VERSION_UNSPECIFIED` (0) | none          | ✅              | ✅           |
| `RDF_VERSION_1_1` (1)         | `1.1`         | ❌              | ❌           |
| `RDF_VERSION_1_2_BASIC` (2)   | `1.2-basic`   | ✅              | ❌           |
| `RDF_VERSION_1_2` (3)         | `1.2`         | ✅              | ✅           |

The following rules apply, following the behavior of other RDF 1.2 serialization formats:

- If `rdf_version` is `RDF_VERSION_UNSPECIFIED`, no version is announced, and the consumer can assume RDF 1.2: the stream MAY contain any term of RDF 1.2.
- The consumer SHOULD throw an error if `rdf_version` has a value that is not listed above.
- Producers SHOULD declare a version when they know in advance which terms the stream may contain. It is RECOMMENDED to declare the lowest version that allows all of these terms. A producer that cannot know this in advance MAY declare a higher version than needed, or MAY leave `rdf_version` unspecified.
- If a version is declared, the stream MUST NOT contain a term that the version does not allow. If it does, the consumer MAY throw an error, or it MAY ignore the declared version and read the term.
- A consumer that does not support the declared version SHOULD throw an error when it reads the stream options.
- When the stream options are [restated](#restating-the-stream-options), the new `rdf_version` applies from that frame on.

### Prefix, name, and datatype lookup entries

Jelly uses a common mechanism of lookup tables for IRI prefixes, IRI names (postfixes), and datatypes. The lookups are used to compress the IRIs and datatypes in the stream. All lookups share the same base mechanism:

- The lookup is a map from a positive integer (the identifier) to a valid UTF-8 string.
- The lookups are indexed from `1`.
- The lookup can be modified at any point in the stream, using lookup entries. A lookup entry sets the value for a given identifier. The modification MUST be applied to everything that follows it in the stream (see also [the working set of a batch](#the-working-set-of-a-batch)).
- The first use of a given identifier MUST be after a value is set for it. If the consumer encounters an identifier that has no value in the lookup, it SHOULD throw an error.
- The maximum size of the lookup is communicated in the [stream options](#stream-options). The producer of the stream MUST NOT exceed the maximum size of the lookup. The consumer SHOULD throw an error if a lookup entry has an identifier greater than the maximum size of the lookup. The consumer MAY implement the lookup as a fixed-size array, or extend it dynamically.
- The lookups are kept from one frame to the next. They are emptied only when the stream options are [restated](#restating-the-stream-options).
- The producer may use any strategy to update the lookup.

!!! note

    You are free to use any strategy for updating the lookup in the producer. You can use the LRU strategy, LFU, or something more complex. The quality of the strategy will influence the compression ratio and the performance of the system. In general, evicting entries in sequential blocks produces smaller file sizes, because then the producer can use [packed lookup entries](#packed-lookup-entries) and [compression in IRI sequences](#iris).
    
    You can also have a fixed lookup in the producer and communicate it at the start of the stream. This is possible if you are using a fixed set of prefixes, names, or datatypes and want to conserve computing power (e.g., in IoT devices).

    The simplest way to implement the consumer's lookup is to just use an indexed array of fixed size.

#### Packed lookup entries

Lookup entries are stored in three fields of [`RdfColumnBatch`](#column-batches), one for each lookup. Each field contains a repeated [`RdfLookupEntryPacked`](reference.md#rdflookupentrypacked) message:

- `names` (2) – entries of the name lookup.
- `prefixes` (3) – entries of the prefix lookup.
- `datatypes` (4) – entries of the datatype lookup.

Lookup entries are often assigned consecutive identifiers. A packed entry states the identifier once and then lists the values of a whole run of consecutive entries, which saves space.

The `RdfLookupEntryPacked` message contains the following fields:

- `id` (1) – 1-based identifier of the **first** value in this entry. The default value of 0 MUST be interpreted as `previous_id + 1`, where `previous_id` is the identifier of the last value of the previous entry of *the same lookup table* in the stream. If 0 appears in the first entry of a given lookup table in the stream, or in the first entry after the stream options were [restated](#restating-the-stream-options), it MUST be interpreted as 1.
- `values` (2) – the values of the entries, in UTF-8. The first value is assigned the identifier `id`, and every following value is assigned the identifier of the previous one plus 1.

A packed entry with zero values MUST NOT be written. Consumers MAY throw an error if they encounter one.

!!! note

    The default value of `0` has a special meaning in lookup entries. You should take advantage of that and use it whenever possible. As the value of `0` is encoded with exactly zero bytes, you can save some space by using it.

#### The working set of a batch

All lookup entries of a [column batch](#column-batches) are applied, in order, **before anything else in the batch is decoded**. This allows the columns of a batch to be decoded independently of each other.

As a consequence, every lookup identifier referenced by a batch MUST still contain the intended value after all of the batch's entries have been applied. In other words: **the working set of a single batch must fit in the lookup tables.** A producer MUST NOT overwrite, within one batch, an identifier that the same batch still refers to.

If a producer cannot satisfy this, it MUST end the frame and start a new one. If a single statement cannot be encoded even in an otherwise empty batch, the producer MUST throw an error – the configured lookup table sizes are too small for this data.

!!! warning

    A consumer cannot detect a violation of this rule. It will silently decode the affected terms to the wrong values. This is a producer-side obligation.

!!! note

    A simple way to implement this on the producer's side is to track which identifiers the current batch has touched (assigned or referenced), and to end the frame before a statement could touch an identifier that is already in that set. If the lookup uses an LRU eviction policy, everything the batch has touched resides at the recent end, so the batch stays safe exactly as long as it has not touched every identifier of the table.

### Column batches

The contents of a stream frame are stored in its `columns` field, as an [`RdfColumnBatch`](reference.md#rdfcolumnbatch) message. A column batch contains the following fields:

| Field                    | Contents                                   | Described in                     |
| ------------------------ | ------------------------------------------ | -------------------------------- |
| `row_count` (1)          | number of statements in the batch          | this section                     |
| `names` (2)              | entries of the name lookup                 | [Packed lookup entries](#packed-lookup-entries) |
| `prefixes` (3)           | entries of the prefix lookup               | [Packed lookup entries](#packed-lookup-entries) |
| `datatypes` (4)          | entries of the datatype lookup             | [Packed lookup entries](#packed-lookup-entries) |
| `namespaces` (5)         | namespace declarations                     | [Namespace declarations](#namespace-declarations) |
| `subjects` (6)           | column of subjects                         | this section, [Columns](#columns) |
| `predicates` (7)         | column of predicates                       | this section, [Columns](#columns) |
| `objects` (8)            | column of objects                          | this section, [Columns](#columns) |
| `graphs` (9)             | column of graph names                      | this section, [Columns](#columns) |
| `message_lengths` (15)   | message boundaries                         | [Message boundaries](#message-boundaries) |

The elements of a batch MUST be processed in the following order:

1. Lookup entries – see [the working set of a batch](#the-working-set-of-a-batch).
2. Namespace declarations, in order.
3. Statements, in order.

The `row_count` field (1) is the number of statements (rows) in the batch. It MUST NOT be greater than 2<sup>27</sup> − 1, which is the largest number of cells the [sequence layout](#sequence-layout) of a column can address. The consumer MUST throw an error otherwise.

Each column stores the RDF terms of one position of the statements (subject, predicate, object, or graph name), with one cell per statement, in the order of the statements. To read a statement, take the cells at the same position in each column: the first statement of the batch is made up of the first cell of the `subjects` column, the first cell of the `predicates` column, and the first cell of the `objects` column (and the first cell of the `graphs` column, in a `QUADS` stream). The second statement is made up of the second cells, and so on. A column field that is not set is treated in the same way as an empty [column](#columns), in which all cells are unbound. The following rules apply to the columns:

- `subjects` (6) – MUST contain only IRIs and blank nodes.
- `predicates` (7) – MUST contain only IRIs.
- `objects` (8) – may contain IRIs, blank nodes, literals, and triple terms.
- `graphs` (9) – MUST NOT be set in a stream with physical type `TRIPLES`. In a stream with physical type `QUADS`, it MUST contain only IRIs and blank nodes. An unbound cell means that the statement is in the default graph. If the field is not set, all statements of the batch are in the default graph.
- The `subjects`, `predicates`, and `objects` columns MUST NOT have unbound cells. The consumer MUST throw an error if any of them has an unbound cell in the first `row_count` cells.
- The consumer SHOULD throw an error if a column contains a type of RDF term that is not allowed in it.

!!! note

    These rules mean that Jelly-RDF 1.2 cannot represent generalized RDF (e.g., literals as subjects).

!!! note

    Most columns are cheap to encode. A batch of statements about one subject has a `subjects` column with one value and one [repeat run](#sequence-layout). A batch of quads in one named graph has a `graphs` column with one value and one repeat run. A batch of quads in the default graph does not need the `graphs` column at all.

??? example "Example (click to expand)"

    Consider a stream with physical type `QUADS` and a batch with these three statements, in N-Quads notation with the prefix `ex:` used for brevity:

    ```
    ex:alice ex:knows ex:bob .
    ex:alice ex:name "Alice" ex:g1 .
    ex:bob ex:name "Bob" ex:g1 .
    ```

    The batch has `row_count: 3`, and its columns contain the following cells (`_` marks an unbound cell):

    | Statement | `subjects` | `predicates` | `objects` | `graphs` |
    | --------- | ---------- | ------------ | --------- | -------- |
    | 1         | `ex:alice` | `ex:knows`   | `ex:bob`  | `_` (default graph) |
    | 2         | `ex:alice` | `ex:name`    | `"Alice"` | `ex:g1`  |
    | 3         | `ex:bob`   | `ex:name`    | `"Bob"`   | `ex:g1`  |

    Each of the four columns is then encoded as an `RdfColumn`, as described in [columns](#columns). The `subjects` column has the run values `ex:alice` and `ex:bob`, with `ex:alice` taking up two cells. The `objects` column mixes IRIs and literals, so it needs the [`kinds`](#term-types) field. See the [full example](#example) for a complete encoding of a similar batch.

#### Message boundaries

In a stream of [RDF Messages](#stream-types) (stream type `RDF_STREAM_TYPE_MESSAGES`), the statements of the stream are split into messages. The frame boundaries do not mark where a message ends. Instead, the ends of the messages are written explicitly, in the `message_lengths` field (15) of the column batches. In a stream with stream type `RDF_STREAM_TYPE_FLAT`, this field MUST be empty.

At any point of the stream, the *current message* is made up of the statements that were not yet assigned to any message. It may include statements from earlier frames. Each value of `message_lengths`, in order, adds that many more statements of the batch to the current message, and then ends the current message. In particular:

- A value of 0 ends the current message without adding statements to it. If the current message has no statements, this is an empty message.
- The sum of the values MUST NOT be greater than `row_count`. The consumer MUST throw an error otherwise.
- The statements of the batch after the last boundary start the next message, which continues in the following frames.

At the end of the stream, if the current message has any statements, it ends there. If it has none, no message is added. The same applies when the stream options are [restated](#restating-the-stream-options).

??? example "Example (click to expand)"

    Assume that the previous frame ended with one statement, *s0*, that was not assigned to any message. The current batch has `row_count: 5`, with statements *s1* to *s5*, and:

    ```protobuf
    message_lengths: [2, 0, 1]
    ```

    - `2` – the current message (*s0*) gets *s1* and *s2*, and ends. The message is *s0*, *s1*, *s2*.
    - `0` – the next message ends immediately. It is an empty message.
    - `1` – the next message gets *s3*, and ends. The message is *s3*.

    *s4* and *s5* start the next message, which continues in the following frames.

!!! note

    A producer that writes one message per frame simply sets `message_lengths: [row_count]` in every frame. A producer with small messages can put many of them in one frame.

### Columns

Columns are a general mechanism for storing sequences of RDF terms. They are used by Jelly-RDF and by [Jelly-SPARQL](sparql.md#columns).

A column stores the cells of one statement position (in Jelly-RDF) or one variable (in Jelly-SPARQL) across all `row_count` rows of a batch, in row order. A cell is either a **bound** RDF term or **unbound**. Each format defines what an unbound cell means, and where it is allowed – for Jelly-RDF, see [column batches](#column-batches).

A column is stored as an [`RdfColumn`](reference.md#rdfcolumn) message. Every column contains:

- The **run values** of the column – RDF terms, with each run of consecutive equal values stored exactly once. Unbound cells are not stored. The run values are split by the type of RDF term into separate lists: IRIs, literals, blank nodes, and triple terms. The `kinds` field indicates which list stores each run value, see [term types](#term-types).
- The `layouts` list – a description of where the sequence of cells deviates from "each run value occupies exactly one cell", see [sequence layout](#sequence-layout).

The `RdfColumn` message has the following fields:

| Field                    | Contents                                   | Described in                     |
| ------------------------ | ------------------------------------------ | -------------------------------- |
| `kinds` (1)              | the term type of each run value            | [Term types](#term-types)        |
| `layouts` (2)            | the sequence layout                        | [Sequence layout](#sequence-layout) |
| `name_ids` (3)           | name identifiers of the IRIs               | [IRIs in columns](#iris-in-columns) |
| `prefix_ids` (4)         | prefix identifiers of the IRIs             | [IRIs in columns](#iris-in-columns) |
| `lex_values` (5)         | lexical forms of the literals              | [Literals in columns](#literals-in-columns) |
| `literal_kinds` (6)      | literal kinds of the literals              | [Literals in columns](#literals-in-columns) |
| `langtags` (7)           | language tags of the literals              | [Literals in columns](#literals-in-columns) |
| `langtag_directions` (8) | base directions of the language tags       | [Literals in columns](#literals-in-columns) |
| `bnodes` (9)             | blank node labels                          | [Blank nodes in columns](#blank-nodes-in-columns) |
| `triple_terms` (10)      | triple terms                               | [Triple terms in columns](#triple-terms-in-columns) |

Each list contains the values of its type in row order, and is empty if the column has no values of that type.

A column whose cells are all unbound is encoded as an empty message. A column MUST NOT decode to more than `row_count` cells. If it decodes to fewer, the remaining cells at the end of the column are unbound.

#### Term types

The `kinds` field packs one term type per run value into 2 bits, four run values per byte, starting from the least significant bits of the first byte:

| Term type | Meaning |
| --------- | ------- |
| 0         | The next IRI (`name_ids` and `prefix_ids`). |
| 1         | The next literal (`lex_values` and `literal_kinds`). |
| 2         | The next blank node (`bnodes`). |
| 3         | The next triple term (`triple_terms`). |

The **number of run values** *m* of a column is the total number of values in its lists: `len(name_ids) + len(lex_values) + len(bnodes) + len(triple_terms)`. The run values of the column are obtained by going through the term types in order, and taking the next value from the list of that type. Then the `layouts` of the column are applied to these run values.

If all run values of a column are of one type, `kinds` SHOULD be empty. A consumer then reads the run values from the one list that has values, in order.

The consumer MUST throw an error if any of the following is true:

- `kinds` is empty, and more than one of the lists has values.
- `kinds` is not empty, and does not have exactly ⌈*m* / 4⌉ bytes.
- The unused bits of the last byte of `kinds` are not 0.
- `kinds` refers to more values of a type than the list of that type has.

!!! note

    Many columns contain terms of a single type, so they do not need the `kinds` field. A column with mixed types costs 2 bits per run value. The values of each type are still in flat lists: the IRIs of any column are two lists of integers, and its literals are a list of strings.

??? example "Example (click to expand)"

    A column containing, in five consecutive rows:

    ```
    https://a.org/x
    _:b1
    "hello"
    "hello"
    https://a.org/y
    ```

    Assume the prefix lookup contains `https://a.org/` at id 1, and the name lookup has `x` at 1 and `y` at 2. The run values are `x`, `_:b1`, `"hello"`, `y`, with the term types 0, 2, 1, 0, and `"hello"` occupies two cells.

    ```protobuf
    RdfColumn {
        kinds: "\x18"
        # 0b00_01_10_00: IRI, blank node, literal, IRI (least significant bits first)
        layouts: [64]
        # skip = 2, repeat run of 2 cells
        name_ids: [0, 0]
        prefix_ids: [1]
        lex_values: ["hello"]
        bnodes: ["b1"]
    }
    ```

#### Sequence layout

The `layouts` field of every column is a flat list of **exceptions** to the rule "each run value occupies exactly one cell". When every cell of a column is bound and no value repeats in consecutive rows, `layouts` is empty.

Each exception is one varint token, optionally followed by one extension varint:

```
token = (skip << 5) | (kind << 4) | len_code
```

- `skip` – bits 5 and up. The number of run values that occupy exactly one cell each since the previous exception, or since the start of the column.
- `kind` – bit 4. `0` = repeat run, `1` = unbound run.
- `len_code` – bits 0–3. If its value is 0–14, the run length code `len` is equal to it. If its value is 15, then `len` is 15 plus the value of the next varint in the `layouts` list (the *extension varint*).

The run lengths are interpreted as follows:

- **Repeat run** – the run value at the current position occupies `len + 2` cells.
- **Unbound run** – there are `len + 1` consecutive unbound cells.

An unbound run is **before** the run value at the current position, or after the last run value once all run values have been consumed. This makes the order of an unbound run and a repeat run at the same position unambiguous.

Decoding a column proceeds as follows, where *m* is the number of run values and *n* is `row_count`:

```
i = 0      # index into the run values
pos = 0    # index into the cells

for each exception (skip, kind, len) in layouts:
    emit run values i .. i+skip, one cell each;  i += skip;  pos += skip
    if kind == 0:   # repeat run
        emit run value i into (len + 2) cells;  i += 1;  pos += len + 2
    else:           # unbound run
        emit (len + 1) unbound cells;  pos += len + 1

emit run values i .. m, one cell each      # implicit tail
emit unbound cells until pos == n          # padding
```

A batch is corrupt, and the consumer MUST throw an error, if any of the following is true for any of its columns:

- `i + skip > m` – a `skip` runs past the last run value.
- A repeat run starts when `i == m` – the run points past the last run value.
- `len_code` is 15 and the token is not followed by an extension varint.
- The column decodes to more than `row_count` cells.

Producers SHOULD merge adjacent runs. In particular, a producer SHOULD NOT emit two unbound runs separated by `skip == 0`. Producers SHOULD omit trailing unbound runs and rely on the padding rule instead (see: [Columns](#columns)).

Consumers MUST decode a column in which runs were not merged (e.g., equal values in consecutive cells stored as separate run values) as described above, with each run value in its own cells.

!!! note

    A token stays a single byte as long as `skip <= 3`. Repeat runs of up to 16 cells and unbound runs of up to 15 cells fit in the token without an extension varint.

    The `skip` field occupies the upper 27 bits of the token, which is where the [maximum row count](#column-batches) of 2<sup>27</sup> − 1 comes from.

??? example "Example (click to expand)"

    Consider a column of 8 cells with the following contents (`_` marks an unbound cell):

    ```
    A  B  B  B  _  _  C  C
    ```

    The run values are `A`, `B`, `C` – three values for eight cells. The layout is:

    - `skip = 1` (the single `A`), `kind = 0` (repeat run), `len = 1` (because `B` occupies `1 + 2 = 3` cells) → token = `(1 << 5) | (0 << 4) | 1` = `33`.
    - `skip = 0`, `kind = 1` (unbound run), `len = 1` (because there are `1 + 1 = 2` unbound cells) → token = `(0 << 5) | (1 << 4) | 1` = `17`.
    - `skip = 0`, `kind = 0` (repeat run), `len = 0` (because `C` occupies `0 + 2 = 2` cells) → token = `0`.

    So `layouts = [33, 17, 0]`.

    Now consider a column of 42 cells: `A`, then `B` repeated 40 times, then `C`. The repeat run of `B` needs `len = 40 − 2 = 38`, which does not fit in `len_code`. So `len_code = 15`, and the extension varint is `38 − 15 = 23`:

    - `skip = 1` (the single `A`), `kind = 0` (repeat run), `len_code = 15` → token = `(1 << 5) | (0 << 4) | 15` = `47`, followed by the extension varint `23`.

    The `C` at the end is covered by the implicit tail, so `layouts = [47, 23]`.

#### IRIs in columns

The IRIs of a column are stored in two fields of `RdfColumn`:

- `name_ids` (3) – the name identifiers of the IRIs, in row order. The length of this list is the number of IRIs among the run values.
- `prefix_ids` (4) – the prefix identifiers of the IRIs, in row order.

The IRIs are reconstructed as described in [IRIs](#iris).

The IRIs of a column are one [IRI sequence](#iris), which starts at the start of the column, in every batch. The `name_ids` list follows the `name_id` inference rule: a value of 0 means "previous `name_id` + 1", and in the first IRI of the column it means `name_id = 1`.

The `prefix_ids` list MUST have one of three lengths:

| Length            | Meaning |
| ----------------- | ------- |
| 0                 | Every IRI has `prefix_id = 0`, that is, no prefix. This is the case when the prefix lookup is disabled. |
| 1                 | Every IRI uses the prefix given by the single entry. This is the case for a column of IRIs sharing one namespace. |
| `len(name_ids)`   | One entry per IRI. |

In the third form, the `prefix_id` inference rule applies along the list: a value of 0 means "the same prefix as the previous IRI in this column", and in the first IRI of the column it means no prefix.

The consumer MUST throw an error if the length of `prefix_ids` is none of the three allowed values.

??? example "Example (click to expand)"

    A column containing four IRIs, in four consecutive rows:

    ```
    https://a.org/x1
    https://a.org/x2
    https://a.org/x1
    https://b.org/z
    ```

    Assume the prefix lookup contains `https://a.org/` at id 1 and `https://b.org/` at id 2, and the name lookup contains `x1` at 1, `x2` at 2, and `z` at 3.

    ```protobuf
    RdfColumn {
        name_ids: [0, 0, 1, 3]
        # 0 -> 0 + 1 = 1 (x1)
        # 0 -> 1 + 1 = 2 (x2)
        # 1 -> 1      (x1)
        # 3 -> 3      (z)
        prefix_ids: [1, 0, 0, 2]
        # 0 means "same prefix as the previous IRI"
        # kinds is empty: every value is an IRI
        # layouts is empty: every cell is bound, no two consecutive cells are equal
    }
    ```

    The same column in a batch where every IRI is in the `https://a.org/` namespace would have `prefix_ids: [1]` instead – one entry for the whole column.

#### Literals in columns

The literals of a column are stored in four fields of `RdfColumn`:

- `lex_values` (5) – the lexical forms of the literals, in row order. The length of this list is the number of literals among the run values.
- `literal_kinds` (6) – the literal kinds of the literals, in row order, see below.
- `langtags` (7) – the language tags that the literal kinds refer to, as UTF-8 strings.
- `langtag_directions` (8) – the [base directions](#base-direction) of the language tags, parallel to `langtags`, as [`RdfBaseDirection`](reference.md#rdfbasedirection) values.

Each literal is a lexical form plus a **literal kind**, which indicates what type of literal it is. A literal kind is an unsigned integer *v*:

| Literal kind *v*       | Meaning |
| ---------------------- | ------- |
| 0                      | A simple literal, that is, a literal with the datatype `http://www.w3.org/2001/XMLSchema#string`. |
| odd *v*                | A literal with the datatype of the [datatype lookup](#prefix-name-and-datatype-lookup-entries) entry with identifier (*v* + 1) / 2. |
| even *v* > 0           | A language-tagged string with the language tag `langtags[`*v* / 2 − 1`]` (a 0-based index), and the base direction `langtag_directions[`*v* / 2 − 1`]`. |

The `literal_kinds` list MUST have one of three lengths:

| Length              | Meaning |
| ------------------- | ------- |
| 0                   | Every literal is a simple literal. |
| 1                   | Every literal has the literal kind given by the single entry. This is the case for a column of values that share one datatype, or one language tag and base direction. |
| `len(lex_values)`   | One entry per literal. |

The consumer MUST throw an error if the length of `literal_kinds` is none of the three allowed values, or if a literal kind refers to an index past the end of `langtags`.

The following rules apply to the language tags:

- Each entry of `langtags` SHOULD be a valid [BCP 47](https://tools.ietf.org/html/bcp47) language tag.
- Producers SHOULD list the language tags in the order in which the literals first use them, and SHOULD NOT list a language tag that is not used by any literal.
- The same language tag MAY appear in `langtags` more than once, with different base directions. Producers SHOULD NOT list the same pair of language tag and base direction twice.
- `langtag_directions` MUST be empty, or have exactly as many entries as `langtags`. An empty list means that no language tag of the column has a base direction. The consumer MUST throw an error if the list has any other length.
- Consumers are not required to check the entries of `langtag_directions` that are not used by any literal.
- Producers SHOULD leave `langtag_directions` empty in a stream that declares `RDF_VERSION_1_1`, because such a stream has no [base directions](#base-direction).

A literal kind that refers to a datatype MUST NOT refer to an entry containing `http://www.w3.org/1999/02/22-rdf-syntax-ns#langString` or `http://www.w3.org/1999/02/22-rdf-syntax-ns#dirLangString`, because a literal with that datatype and no language tag is not a valid RDF term. Language-tagged strings always use a language tag from `langtags`. The consumer SHOULD throw an error otherwise.

A simple literal does not need an `xsd:string` entry in the datatype lookup: the producer can use the literal kind 0 instead. A literal kind referring to an `xsd:string` entry is also legal and produces the same result.

!!! note

    This design allows for efficiently storing columns in which every value has the same literal kind – think of a column of `xsd:integer` values, or a column of language strings in one language.

??? example "Example (click to expand)"

    Consider a column containing, in four consecutive rows:

    ```
    "cat"@en
    "42"^^xsd:integer
    "chat"@fr
    "dog"@en
    ```

    Assume the datatype lookup contains `xsd:integer` at id 1.

    ```protobuf
    RdfColumn {
        lex_values: ["cat", "42", "chat", "dog"]
        literal_kinds: [2, 1, 4, 2]
        # 2 -> langtags[0] (en)
        # 1 -> datatype 1 (xsd:integer)
        # 4 -> langtags[1] (fr)
        langtags: ["en", "fr"]
        # langtag_directions is empty: no base directions
        # kinds is empty: every value is a literal
    }
    ```

    A column of the same four rows, but with every value tagged `@en`, would have `literal_kinds: [2]` and `langtags: ["en"]` instead.

#### Blank nodes in columns

The blank nodes of a column are stored in the `bnodes` field (9) of `RdfColumn`: the [blank node labels](#blank-nodes), in row order, as plain UTF-8 strings.

#### Triple terms in columns

The triple terms of a column are stored in the `triple_terms` field (10) of `RdfColumn`, as [`RdfTripleTerm`](#triple-terms) messages, in row order. Triple terms cannot occur in a stream that declares `RDF_VERSION_1_1` or `RDF_VERSION_1_2_BASIC`. If `triple_terms` is not empty in such a stream, the consumer MAY throw an error (see [RDF version](#rdf-version)).

The IRIs of all the triple terms of one column are one [IRI sequence](#iris), which starts at the start of the column, in every batch. It advances through the triple terms in order, and through the IRIs of each triple term in the order subject, predicate, object, recursively into nested triple terms. This sequence is separate from the sequence of the other IRIs of the column (`name_ids` and `prefix_ids`). See [triple terms](#triple-terms) for how a triple term and its nested triple terms are encoded, and [IRIs](#iris) for the inference rules of an IRI sequence.

### RDF terms

#### IRIs

An IRI is encoded as two identifiers: a *prefix identifier*, referring to an entry in the prefix lookup, and a *name identifier*, referring to an entry in the name lookup. In [columns](#iris-in-columns), the identifiers are stored in lists. In [triple terms](#triple-terms) and [namespace declarations](#namespace-declarations), they are stored in an [`RdfIri`](reference.md#rdfiri) message, which has two fields:

- `prefix_id` (1) – 1-based identifier of the prefix of the IRI, corresponding to an entry in the prefix lookup.
- `name_id` (2) – 1-based identifier of the name (suffix) of the IRI, corresponding to an entry in the name lookup.

Both identifiers may be written as 0, in which case their value is inferred from the previous IRI. The inference works along an **IRI sequence**: a series of IRIs, processed in a fixed order. Each place where IRIs are stored defines its own IRI sequences:

- The IRIs of a column (`name_ids` and `prefix_ids`) – one sequence per column, per batch. See [IRIs in columns](#iris-in-columns).
- The IRIs in the triple terms of a column – one sequence per column, per batch. See [triple terms in columns](#triple-terms-in-columns).
- The IRIs of the namespace declarations – one sequence per batch. See [namespace declarations](#namespace-declarations).

Within an IRI sequence, the following rules apply:

- A `name_id` of 0 MUST be interpreted as `previous_name_id + 1`, that is, the name identifier of the previous IRI in the sequence incremented by one. In the first IRI of the sequence, it MUST be interpreted as 1. Multiple `0` values in a row may occur, in which case the name identifier MUST be interpreted as incrementing by one for each `0` value.
- A `prefix_id` of 0 MUST be interpreted as the same prefix identifier as in the previous IRI of the sequence. In the first IRI of the sequence, it MUST be interpreted as no prefix (an empty, zero-length string). This is for example used when the prefix lookup table is disabled.

The IRI is then constructed by first resolving the prefix and the name using the [prefix and name lookup tables](#prefix-name-and-datatype-lookup-entries), and then concatenating the prefix and the name. The IRI SHOULD be a valid IRI, as defined in [RFC 3987](https://tools.ietf.org/html/rfc3987).

!!! note "Difference from Jelly-RDF 1.1"

    In Jelly-RDF 1.1, there is one IRI sequence for the whole stream, in the strict order of rows and terms. In Jelly-RDF 1.2, there is one sequence per column, per batch. This lets a consumer decode the columns of a batch in any order, or in parallel, given only the lookup tables.

!!! note

    The spec does not specify how to split the IRIs into names and prefixes. You can use any strategy you want, as long as you follow the rules above. The simplest way is to split the IRI at the last occurrence of the `#` or `/` character – this is what the Java implementation uses. 
    
    **These prefixes are not meant to be user-facing**, they can be entirely arbitrary and DO NOT correspond to, for example, `PREFIX` declarations in Turtle. If you want to preserve such user-facing namespace declarations, use the [namespace declarations](#namespace-declarations) feature instead.

!!! note

    The behavior of the default values is designed to save space in the stream. Usually in RDF many IRIs share the same prefix, so you can save space by not repeating the prefix in the stream. At the same time the name part of the IRI is often unique, so for each name you will need a new entry in the lookup table – which is often the next entry after the one you have just created.

#### Literals

Literals in [columns](#literals-in-columns) are stored in lists. Literals in the object position of [triple terms](#triple-terms) are stored as [`RdfLiteral`](reference.md#rdfliteral) messages, which have the following fields:

- `lex` (1) – the lexical form of the literal in UTF-8. This field is OPTIONAL and defaults to an empty string.
- `literalKind` oneof. At most one of the following fields MUST be set:
    - `langtag` (2) – UTF-8 language tag, indicating that the literal is a language-tagged string. The language tag SHOULD be a valid [BCP 47](https://tools.ietf.org/html/bcp47) language tag.
    - `datatype` (3) – 1-based identifier of the datatype in the [datatype lookup](#prefix-name-and-datatype-lookup-entries), indicating that the literal is a typed literal.
- `direction` (4) – the [base direction](#base-direction) of a language-tagged string.

If no field in the `literalKind` oneof is set, then the literal MUST be interpreted as a simple literal (has datatype IRI equal to `http://www.w3.org/2001/XMLSchema#string`).

The following rules apply:

- `direction` MUST NOT be set unless `langtag` is set. The consumer MUST throw an error otherwise.
- `datatype` MUST NOT be 0, and MUST NOT refer to `rdf:langString` or `rdf:dirLangString`. The consumer MUST throw an error if it is 0, and SHOULD throw an error if it refers to `rdf:langString` or `rdf:dirLangString`.

!!! note

    Using the default value of `0` for the `datatype` field is not allowed, in contrast to names and prefixes in `RdfIri`. This is because the `datatype` field itself is optional and the default value would be ambiguous.

#### Base direction

In RDF 1.2, a language-tagged string may have a base direction: `ltr` (left-to-right) or `rtl` (right-to-left). Such a literal has the datatype `http://www.w3.org/1999/02/22-rdf-syntax-ns#dirLangString`.

A base direction is an [`RdfBaseDirection`](reference.md#rdfbasedirection) value: `RDF_BASE_DIRECTION_UNSPECIFIED` (0, the default: no base direction), `RDF_BASE_DIRECTION_LTR` (1), or `RDF_BASE_DIRECTION_RTL` (2). It is encoded in the `langtag_directions` field of [columns](#literals-in-columns), and in the `direction` field of [`RdfLiteral`](#literals).

The following rules apply:

- The consumer SHOULD throw an error if the base direction of a literal has a value that is not listed above.
- A stream that declares `RDF_VERSION_1_1` MUST NOT contain a literal with a base direction other than `RDF_BASE_DIRECTION_UNSPECIFIED`.

#### Blank nodes

RDF blank nodes are represented using their labels: simple UTF-8 strings.

Blank node labels are scoped as follows:

- In a stream with stream type `RDF_STREAM_TYPE_FLAT`, the scope is the whole stream, also across [restated stream options](#restating-the-stream-options).
- In a stream with stream type `RDF_STREAM_TYPE_MESSAGES`, the scope is one RDF Message.

Two occurrences of the same label within one scope MUST be interpreted as referring to the same blank node. Two different labels MUST be interpreted as referring to different blank nodes. Two occurrences of the same label in different scopes MUST be interpreted as referring to different blank nodes.

!!! note

    Many RDF libraries (e.g., Eclipse RDF4J, Apache Jena) use internal identifiers for blank nodes, which can be used as the labels in Jelly streams. You can also use a different format, for example with shorter labels to preserve space.

#### Triple terms

An RDF 1.2 triple term is encoded as an [`RdfTripleTerm`](reference.md#rdftripleterm) message. Triple terms may occur only in the `objects` column of a column batch (see [column batches](#column-batches)), and as objects of other triple terms. `RdfTripleTerm` has the following fields:

- the `subject` oneof – `s_iri` (1), an [`RdfIri`](#iris), or `s_bnode` (2), a [blank node label](#blank-nodes).
- `p_iri` (5) – the predicate, an [`RdfIri`](#iris).
- the `object` oneof – `o_iri` (9), an [`RdfIri`](#iris); `o_bnode` (10), a [blank node label](#blank-nodes); `o_literal` (11), an [`RdfLiteral`](#literals); or `o_triple_term` (12), a nested `RdfTripleTerm`.

The following rules apply:

- The subject, the predicate, and the object MUST all be set. The consumer MUST throw an error if any of them is missing.
- The IRIs in the triple terms follow the rules of the [IRI sequence](#iris) of the triple terms of their column, see [triple terms in columns](#triple-terms-in-columns).
- Triple terms may be nested up to arbitrary depth. The consumer SHOULD throw an error if the depth of the nesting exceeds the capabilities of the implementation.

### Namespace declarations

IRI namespace declarations are not a formal part of the RDF abstract data model. They are a convenience / cosmetic feature of the serialization format to allow preserving associations between short namespace names and full IRIs. Namespace declarations are stored in the `namespaces` field (5) of a [column batch](#column-batches), as `RdfNamespaceDeclaration` messages ([reference](reference.md#rdfnamespacedeclaration)). The message has the following fields:

- `name` (1) – the short name of the namespace, encoded in UTF-8. It SHOULD conform to the [`PN_PREFIX` production in RDF 1.2 Turtle](https://www.w3.org/TR/rdf12-turtle/#grammar-production-PN_PREFIX). Note that the `:` character (colon) is not part of the name. An empty string (the default value) is allowed.
- `value` (2) – the IRI of the namespace as an [`RdfIri`](#iris) message. This field is REQUIRED.

The following rules apply:

- The IRIs of the namespace declarations of one batch are one [IRI sequence](#iris), in the order of the declarations. It is separate from the IRI sequences of the columns.
- A namespace declaration stays in effect until the same name is declared again. Namespace declarations are kept from one RDF Message to the next, and when the stream options are [restated](#restating-the-stream-options).
- The namespace declarations of a batch are processed before its statements.

??? example "Example (click to expand)"

    To encode the Turtle namespace declaration `PREFIX ex: <http://example.com/>` you would use the following column batch:

    ```protobuf
    RdfColumnBatch {
        prefixes: [{ values: ["http://example.com/"] }]
        # id 0, interpreted as 1
        names: [{ values: [""] }]
        # We must define an empty name entry, because the name part is always required
        namespaces: [{
            name: "ex"
            value: {
                prefix_id: 1
                # name_id 0, interpreted as 1 (first IRI of the sequence)
            }
        }]
    }
    ```

    Alternatively, if not using the prefix lookup table:

    ```protobuf
    RdfColumnBatch {
        names: [{ values: ["http://example.com/"] }]
        namespaces: [{
            name: "ex"
            value: {}
            # prefix_id 0, interpreted as no prefix (first IRI of the sequence)
            # name_id 0, interpreted as 1
        }]
    }
    ```

### Example

??? example "A small stream (click to expand)"

    The following stream has two frames. The first frame encodes this Turtle document:

    ```turtle
    PREFIX ex: <http://example.org/>
    ex:alice ex:knows ex:bob .
    ex:alice ex:name "Alice" .
    ex:bob ex:name "Bob"@en .
    ```

    The second frame restates the stream options, as it would after concatenating two files. It encodes one more triple: `ex:carol ex:name "Carol" .`

    ```protobuf
    # Frame 1
    RdfStreamFrame {
        rows: [{
            options: {
                physical_type: PHYSICAL_STREAM_TYPE_TRIPLES
                # stream_type not set: RDF_STREAM_TYPE_FLAT
                rdf_version: RDF_VERSION_1_1
                max_name_table_size: 128
                max_prefix_table_size: 16
                version: 3
            }
        }]
        columns: {
            row_count: 3
            names: [{ values: ["", "alice", "bob", "knows", "name"] }]
            # id 0, interpreted as 1: the names get ids 1 to 5
            prefixes: [{ values: ["http://example.org/"] }]
            # id 0, interpreted as 1
            namespaces: [{
                name: "ex"
                value: { prefix_id: 1 }
                # name_id 0, interpreted as 1 ("")
            }]
            subjects: {
                layouts: [0]
                # skip = 0, repeat run of 2 cells: alice, alice, bob
                name_ids: [2, 0]
                # 2 (alice), 0 -> 2 + 1 = 3 (bob)
                prefix_ids: [1]
            }
            predicates: {
                layouts: [32]
                # skip = 1, repeat run of 2 cells: knows, name, name
                name_ids: [4, 0]
                # 4 (knows), 0 -> 4 + 1 = 5 (name)
                prefix_ids: [1]
            }
            objects: {
                kinds: "\x14"
                # 0b00_01_01_00: IRI, literal, literal
                name_ids: [3]
                # 3 (bob)
                prefix_ids: [1]
                lex_values: ["Alice", "Bob"]
                literal_kinds: [0, 2]
                # 0 -> simple literal, 2 -> langtags[0] (en)
                langtags: ["en"]
            }
        }
    }

    # Frame 2
    RdfStreamFrame {
        rows: [{
            options: {
                physical_type: PHYSICAL_STREAM_TYPE_TRIPLES
                rdf_version: RDF_VERSION_1_1
                max_name_table_size: 128
                max_prefix_table_size: 16
                version: 3
            }
        }]
        # The lookups are emptied, the namespace "ex" stays in effect
        columns: {
            row_count: 1
            names: [{ values: ["carol", "name"] }]
            # id 0, interpreted as 1 again: ids 1 and 2
            prefixes: [{ values: ["http://example.org/"] }]
            subjects: {
                name_ids: [0]
                # 0 -> 1 (carol)
                prefix_ids: [1]
            }
            predicates: {
                name_ids: [2]
                # 2 (name) – the sequence of each column starts again, so 0 would mean 1
                prefix_ids: [1]
            }
            objects: {
                lex_values: ["Carol"]
                # literal_kinds is empty: a simple literal
            }
        }
    }
    ```

## Delimited variant of Jelly

!!! note

    By default, Protobuf messages [are not delimited](https://protobuf.dev/programming-guides/techniques/#streaming), so if you write multiple messages to the same file / socket / byte stream, you need to add some kind of delimiter between them. Jelly uses the convention already implemented in some protobuf libraries of prepending a varint before the message, to specify the length of the message. 

A byte stream (or file) in the delimited variant MUST consist of a series of delimited `RdfStreamFrame` messages. A delimited message is a message that has a Protobuf varint prepended before it, specifying the length of the message in bytes.

A producer that writes a Jelly-RDF stream to a file, or sends it in an HTTP message body with the `application/x-jelly-rdf` [media type](#internet-media-type-and-file-extension), MUST use the delimited variant. This applies also when the stream consists of a single frame. Consumers SHOULD also be able to read a file that contains a single, non-delimited `RdfStreamFrame` message.

Transports that provide their own message framing (for example gRPC, MQTT, or Kafka) send one bare, non-delimited `RdfStreamFrame` message per transport message.

### Delimited variant implementations

The delimiting convention is implemented in Protobuf libraries for:

- C++: [delimited_message_util.cc](https://github.com/protocolbuffers/protobuf/blob/main/src/google/protobuf/util/delimited_message_util.cc)
- Java: [writeDelimitedTo](https://developers.google.com/protocol-buffers/docs/reference/java/com/google/protobuf/MessageLite#writeDelimitedTo-java.io.OutputStream-) and [parseDelimitedFrom](https://developers.google.com/protocol-buffers/docs/reference/java/com/google/protobuf/Parser#parseDelimitedFrom-java.io.InputStream-)
- Python: [serialize_length_prefixed and parse_length_prefixed](https://github.com/protocolbuffers/protobuf/blob/v30.2/python/google/protobuf/proto.py)

The JVM implementation of Jelly also supports the delimited variant – [see the documentation]({{ jvm_link('user/reactive#byte-streams-delimited-variant') }}).

## Internet media type and file extension

The RECOMMENDED media type for Jelly is `application/x-jelly-rdf`. The RECOMMENDED file extension is `.jelly`.

The same media type and file extension are used for all versions of Jelly-RDF. The version of a stream is set in its [stream options](#version-tag).

The files MUST be saved in the [delimited variant of Jelly](#delimited-variant-of-jelly).

## Security considerations

*This section is not part of the specification.*

### Protocol Buffers

The Jelly serialization format is based on Protocol Buffers, which handles all binary manipulation, and therefore is most likely to be the main security concern. Please refer to the [Protobuf Version Support page](https://protobuf.dev/support/version-support/) for information on security patches and support. See also the published [CVE Records for Protocol Buffers](https://www.cve.org/CVERecord/SearchResults?query=Protocol+Buffers).

### Overly large lookup tables

For untrusted input, consumers must always validate that the requested sizes of the name, prefix, and datatype lookup tables are not overly large and are supported by the consumer. A malicious producer could attempt to exhaust the memory of the consumer by requesting a lookup table of several gigabytes or more. This would constitute a denial-of-service vector.

The recommended mitigation is for each implementation to define a maximum allowed lookup size and check the requested size against it, rejecting the stream if it is larger. The limit should be configurable, so that a user who trusts the producer can raise it. See [stream options](#stream-options) for the recommended defaults.

!!! info

    The Jelly-JVM implementation uses a configurable limit. The mechanism is described [here]({{ jvm_link('user/utilities/#jelly-options-presets') }}).

    The Jelly gRPC streaming protocol has a built-in mechanism for stream options handling that does include such checks. See the [gRPC streaming protocol specification](streaming.md#stream-options-handling).

### Invalid lookup entry IDs and references

For untrusted input, consumers must always validate that the lookup entry IDs in the stream are valid and within the bounds of the lookup table. A malicious producer could attempt to reference a non-existent entry in the lookup table, which could lead to it reading or writing arbitrary memory.

This is automatically handled by languages that include array bounds checking, such as Java or Python. In languages without array bounds checking, the consumer must manually check that the lookup entry ID is within the bounds of the lookup table.

### Overly large row counts

The `row_count` field of a batch is not bounded by the size of the batch: a batch of a few bytes can declare a row count in the tens of millions. For a consumer that allocates a per-row buffer of `row_count` elements before decoding the columns, this would be a denial-of-service vector.

The recommended mitigation is to grow the decoding buffers to the size actually needed as the columns are decoded, and to validate `row_count` against a configurable limit before allocating anything.

### Column layouts

The layout tokens of a column decide how many cells the consumer will emit when decoding the column. A consumer must validate every token against the number of run values it actually has and against `row_count`, as described in [sequence layout](#sequence-layout), before emitting anything. In particular, the extension varint of an escaped length token is attacker-controlled and must not be trusted to fit into the remaining space of the row buffer.

### Deeply nested triple terms

`RdfTripleTerm` is a recursive message: the object of a triple term may be another triple term. A malicious producer could send a triple term nested deeply enough to overflow the consumer's stack while parsing or converting it, which could be used as a denial-of-service vector.

The official Protobuf implementations are not vulnerable to this type of attack, as they include a message recursion limit (100 by default). Implementations should verify that their Protobuf library supports this limit and that it is set to a reasonable value.

!!! info

    In practice, there are very few (if any) use cases where very deep recursive nesting would be needed for Jelly. Unless you are working with some very exotic data, you should be fine with setting the recursion limit to as low as 10 messages. But still, even the default limit of 100 should not cause you any problems, unless operating under extremely constrained environments.

### RDF content

Jelly is a general serialization format for RDF data, and as such, may be used to transmit malicious or misleading content, such as links to phishing websites or false information. Please refer to the [RDF 1.2 Turtle specification](https://www.w3.org/TR/rdf12-turtle/#sec-mediaReg) for information on security considerations related to RDF content.

### Encryption, authentication, and authorization

Jelly does not provide any built-in mechanisms for encryption, authentication, or authorization, as it only handles data serialization. If you need to secure your data, you should use a secure transport layer (e.g., HTTPS) and implement encryption, authentication, and authorization on the application level.

## Implementations

*This section is not part of the specification.*

The following implementations of the Jelly RDF serialization format specification are available:

- [Jelly-JVM]({{ jvm_link() }})
    - Specification version: {{ proto_version() }}
    - Implemented actors: producer, consumer
    - Supported RDF libraries: [Apache Jena](https://jena.apache.org/), [RDF4J](https://rdf4j.org/), [Titanium RDF API](https://github.com/filip26/titanium-rdf-api)
- [pyjelly]( {{ python_link() }} )
    - Specification version: 1.1.x
    - Implemented actors: producer, consumer
    - Supported RDF libraries: [rdflib](https://rdflib.readthedocs.io/), generic integration (no RDF library)
- [rdfjs-jelly](https://github.com/pietercolpaert/rdfjs-jelly) *(unofficial, community-led)*
    - Specification version: 1.2.x
    - Implemented actors: producer, consumer
    - Supported RDF libraries: any [RDF/JS](https://rdf.js.org/) library
- [Locorda](https://locorda.dev/rdf/jelly/) *(unofficial, community-led)*
    - Specification version: 1.1.x
    - Implemented actors: producer, consumer
    - Supported RDF libraries: [Locorda RDF](https://github.com/locorda/rdf)

See the **[conformance reports](../conformance/rdf-reports.md)** for details on the supported features of each implementation.

## Changes from Jelly-RDF 1.1

*This section is not part of the specification.*

This section lists the main differences between Jelly-RDF 1.1 (row layout) and Jelly-RDF 1.2 (column layout).

- **Frame contents.** In Jelly-RDF 1.1, a frame is a list of rows, each containing one statement, lookup entry, or other element. In Jelly-RDF 1.2, the contents of a frame are a [column batch](#column-batches), and the rows of a frame store only the stream options.
- **Lookup entries** are [packed](#packed-lookup-entries): one entry may set the values of many consecutive identifiers.
- **Repeated terms** are replaced by [repeat runs](#sequence-layout) in columns.
- **IRI inference** (the meaning of 0 in `prefix_id` and `name_id`) works per column, per batch, instead of across the whole stream. See [IRIs](#iris).
- **Physical stream types.** `GRAPHS` is not available. Use `QUADS` instead.
- **Logical stream types** (RDF-STaX) are replaced by [stream types](#stream-types). A 1.1 stream of a "flat" logical type (flat triples, flat quads) corresponds to a `FLAT` stream. A 1.1 stream of the other logical types (graphs, datasets, and their subtypes), where each frame is one element, corresponds to a `MESSAGES` stream with one message per frame. The subtypes of RDF-STaX (e.g., [subject graph stream]({{ stax_link('ontology#subjectGraphStream') }})) have no equivalent in Jelly-RDF 1.2.
- **RDF-star and RDF 1.2.** The RDF-star quoted triples of Jelly-RDF 1.1 are replaced by RDF 1.2 [triple terms](#triple-terms), which can occur only in the object position. Quoted triples in the subject or predicate position cannot be represented. Literals may have a [base direction](#base-direction). The `rdf_star` option is replaced by [`rdf_version`](#rdf-version).
- **Generalized statements** are not supported. Literals in the subject, predicate, or graph position, and blank nodes in the predicate position cannot be represented.
- **Stream options** can be [restated](#restating-the-stream-options) with different values, which makes streams concatenable. In Jelly-RDF 1.1, repeated stream options had to be identical to the first ones.
- **Name lookup size.** The minimum `max_name_table_size` is 128, instead of 8.
- **Delimited variant.** Files and HTTP responses MUST be written in the [delimited variant](#delimited-variant-of-jelly). In Jelly-RDF 1.1, this was a SHOULD.
