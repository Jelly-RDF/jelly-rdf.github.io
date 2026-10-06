# Jelly SPARQL query results format specification

**This document is the specification of the Jelly SPARQL query results format, also known as Jelly-SPARQL. It is intended for implementers of Jelly libraries and applications.** If you are looking for a user-friendly introduction to Jelly, see the [Jelly index page](index.md).

Jelly-SPARQL is a binary serialization format for **SPARQL query results** – solution sequences (`SELECT`) and boolean results (`ASK`). It is binary, streamable, and reuses the RDF term encoding of [Jelly-RDF](serialization.md).

This document is accompanied by the [Jelly Protobuf reference](reference.md) and the Protobuf definitions themselves ([`sparql.proto`]({{ git_proto_link('sparql.proto') }}) and [`rdf2.proto`]({{ git_proto_link('rdf2.proto') }})).

The following assumptions are used in this document:

- Jelly-SPARQL reuses Protobuf messages and encoding rules from the [Jelly RDF serialization format](serialization.md), version `{{ proto_version() }}`. Concepts, definitions, and Protobuf messages defined there apply also here, unless explicitly stated otherwise.
- The basis for the terms used is the RDF 1.2 specification ([W3C Candidate Recommendation Snapshot 07 April 2026](https://www.w3.org/TR/rdf12-concepts/)). The format support a RDF 1.1 mode as well.
- The basis for the terms related to query results is the SPARQL 1.2 Query Language specification ([W3C Working Draft 21 September 2026](https://www.w3.org/TR/sparql12-query/)), in particular the definitions of a *solution*, a *solution sequence*, and a *query variable*.
- In parts referring to the semantics of result sets, the SPARQL 1.2 Query Results JSON Format ([W3C Working Draft 13 August 2026](https://www.w3.org/TR/sparql12-results-json/)) is used.
- All strings in the serialization are assumed to be UTF-8 encoded.

| Document information | |
| --- | --- |
| **Author:** | [Piotr Sowiński](https://ostrzyciel.eu) ([Ostrzyciel](https://github.com/Ostrzyciel)), Anastasiya Danilenka ([adanilenka](https://github.com/adanilenka)) |
| **Version:** | experimental (dev) |
| **Date:** | {{ git_revision_date_localized }} |
| **Permanent URL:** | [`https://w3id.org/jelly/{{ proto_version() }}/specification/sparql`](https://w3id.org/jelly/{{ proto_version() }}/specification/sparql) |
| **Document status**: | Experimental draft specification |
| **License:** | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

{% include "./includes/start_info.md" %}

## Conformance

{% include "./includes/conformance.md" %}

To claim conformance with this specification, an implementation MUST pass all applicable tests from the [Jelly-SPARQL conformance test suite](../conformance/sparql-test-cases.md), and MUST provide a conformance report as described on the [reporting conformance](../conformance/reporting-conformance.md) page. Implementations SHOULD pass the conformance tests marked with the `SHOULD` conformance level (`jellyt:featureShouldLevel`).

!!! note

    Conformance tests are a way to verify that implementations correctly follow the specification. However, passing all tests does not guarantee that the implementation perfectly implements the specification, is free of bugs, or that it will work in all scenarios.

    Implementations typically also employ extensive unit tests, integration tests, and other quality assurance measures to ensure correctness and reliability.


## Versioning

The format follows the [Semantic Versioning 2.0](https://semver.org/) scheme. Each MAJOR.MINOR semantic version corresponds to an integer version tag in the format. The version tag is encoded in the `version` field of the [`SparqlResultsOptions`](reference.md#sparqlresultsoptions) message. See also the [section on stream options](#stream-options) for more information on how to handle the version tags in serialized streams.

The following versions of the format are defined:

| Version tag | Semantic version    | Last release date                 | Changes                         |
| ----------- | ------------------- | --------------------------------- | ------------------------------- |
| 1           | 1.0.0               | Not finalized yet (draft)         | (initial version)               |

Jelly-SPARQL has its own version tag, which is independent of the version tags of [Jelly-RDF](serialization.md#versioning) and [Jelly-Patch](patch.md#versioning).

!!! note

    Releases of the protocol are published on [GitHub](https://github.com/Jelly-RDF/jelly-protobuf/releases).

### Backward compatibility

{% include "./includes/back_compat.md" %}

### Forward compatibility

{% include "./includes/forward_compat.md" %}

!!! note

    See also the notes about the practical implications of this in the [Jelly-RDF specification](serialization.md#forward-compatibility).

## Actors and implementations

Jelly-SPARQL assumes there to be two actors involved in processing the stream: the producer (writer) and the consumer (reader). The producer is responsible for serializing the SPARQL query results into the Jelly-SPARQL format, and the consumer is responsible for parsing the Jelly-SPARQL format into SPARQL query results.

Implementations may include only the producer, only the consumer, or both.

## Format specification

Jelly-SPARQL uses [Protocol Buffers version 3](https://protobuf.dev/programming-guides/proto3/) as the underlying serialization format. All implementations MUST use a compliant Protocol Buffers implementation. The Protocol Buffers schema for Jelly-SPARQL is defined in `sparql.proto` ([source code]({{ git_proto_link('sparql.proto') }}), [reference](reference.md#sparqlproto)), which imports `rdf2.proto` and `rdf.proto`.

A Jelly-SPARQL **result stream** is an ordered sequence of **result frames**. The frames may be sent one-by-one using a streaming protocol (e.g., gRPC, MQTT, Kafka) or written in sequence to a byte stream (e.g., a file or socket) – see the [delimited variant](#delimited).

A result stream contains one or more result sets – see [stream types](#stream-types). Each result set is one of the two kinds of SPARQL query results:

- A **solution sequence** – an ordered sequence of solutions (rows). Each solution binds a subset of the result variables to RDF terms.
- A **boolean result** – a single `true` or `false` value, as produced by an `ASK` query.

The kind of a result set is determined by the [first frame of the result set](#stream-types): if the `ask_result` field is set in it, the result set is a boolean result. Otherwise, it is a solution sequence.

Within a frame, solutions are stored **column-wise**: one column per result variable, with the columns grouped by the type of the RDF terms they contain. Most variables in real result sets are bound to terms of a single type, which lets the values of such a column be stored efficiently as a flat list of primitives.

!!! note "Why columns?"

    In a row-oriented layout, every bound value needs its own length-delimited sub-message with a `oneof` selecting the term type, which costs several bytes of framing per value and one object per value on the consumer's side. Grouping the values of one variable together means the term type is stated once per column instead of once per value, values that repeat in consecutive rows can be collapsed cheaply, and a reader can keep a whole column in a primitive array.

### Stream types

A result stream represents either a single result set, or a sequence of result sets. This is set by the `stream_type` field (2) of the [stream options](#stream-options), a [`SparqlStreamType`](reference.md#sparqlstreamtype) value:

- `SPARQL_STREAM_TYPE_FLAT` (0) – default value. The entire stream is a single result set.
- `SPARQL_STREAM_TYPE_PUNCTUATED` (1) – the stream is a sequence of result sets, each ended by a [trailer](#stream-trailer).

The consumer MUST throw an error if `stream_type` has a value that is not listed above.

In a `FLAT` stream, the **first frame of the result set** is the first frame of the stream. In a `PUNCTUATED` stream, the first frame of each result set is the first frame of the stream, and every frame that directly follows a frame with a trailer.

The following rules apply to `PUNCTUATED` streams:

- A result set consists of one or more consecutive frames, starting with the first frame of the result set and ending with the first frame that has a trailer.
- Each result set is either a solution sequence or a boolean result, decided by its own first frame. The result sets are independent of each other: they may declare different variables. Solution sequences and boolean results may be mixed in one stream.
- The [lookup tables](#prefix-name-and-datatype-lookup-entries) are kept from one result set to the next.
- [Blank node labels](#blank-node-columns) are scoped to a single result set.
- The stream options MUST NOT be set in a frame other than the first frame of a result set. The consumer MUST throw an error otherwise.

The value of `stream_type` MUST be the same in all stream options of a stream. The consumer MUST throw an error otherwise.

Consumers are not required to support `PUNCTUATED` streams. A consumer that does not support them SHOULD throw an error when it reads the stream options.

!!! note "What `PUNCTUATED` streams are for"

    Some applications produce many result sets, one after another: a continuous query that is evaluated once per window, a pub/sub topic with the answers to a stream of queries, or a file with the results of a batch of queries.

!!! note

    Concatenating two `PUNCTUATED` streams gives a valid `PUNCTUATED` stream with the result sets of both, in order, as long as the last result set of the first stream ends with a trailer. If it does not (for example, because the producer crashed), the stream options of the second stream end up in the middle of a result set, which is not allowed.

### Result frames

A result frame is a message of type [`SparqlResultsFrame`](reference.md#sparqlresultsframe). A frame contains a batch of rows (solutions), together with any [lookup entries](#prefix-name-and-datatype-lookup-entries) it needs. It is RECOMMENDED to keep the serialized size of a frame below 1 MB.

A result stream MUST contain at least one frame. The consumer MUST throw an error otherwise. The first frame MUST contain the [stream options](#stream-options) and either the [result set header](#result-set-header) or the [boolean result](#boolean-results).

The number of rows in a frame is given by the `row_count` field (3). It MUST NOT be greater than 2<sup>27</sup> − 1, which is the largest number of cells the [sequence layout](#sequence-layout) of a column can address. The consumer MUST throw an error otherwise.

!!! note

    In practice the row count is bounded far below 2<sup>27</sup> − 1 by the recommended frame size.

The frames of a result stream have no meaning of their own – they are purely a batching mechanism. In particular, a frame boundary on its own does not separate one result set from another – only a [trailer](#stream-trailer) in a [`PUNCTUATED` stream](#stream-types) does.

!!! note

    Because a frame is just a batch of rows, the producer is free to choose the batch size. A good default is to size the frames in *values* (cells) rather than rows, since the cost of a row grows with the number of variables: 4096 values means 4096 rows of a one-variable result set, but only 204 rows of a 20-variable one.

    The producer may also have to end a frame early, when the [lookup tables fill up](#the-working-set-of-a-frame).

#### Ordering

Result frames MUST be processed strictly in order. Each frame MUST be processed in its entirety before the next frame is processed.

The order of rows within a frame, and the order of the frames, together define the order of the solution sequence, and the order of the result sets in a [`PUNCTUATED` stream](#stream-types). Consumers MUST preserve this order.

Implementations MAY choose to adopt a **non-standard** solution where the order or delivery of the frames is not guaranteed. The implementation MUST clearly specify in the documentation that it uses such a non-standard solution.

!!! note

    See also the notes about the practical implications of this in the [Jelly-RDF specification](serialization.md#ordering).

!!! note "Making frames independently decodable"

    Because the [IRI inference state resets per column, per frame](#iri-columns), a frame can be decoded using only the stream options, the lookup table state, and the header in effect. A producer that re-emits all the lookup entries and restates the header, in **every** frame makes each frame decodable on its own, given the stream options.

    This costs space, but it is the way to build a stream whose frames can be dropped or processed out of order.

#### Frame metadata

`SparqlResultsFrame` messages have a `metadata` field (15) of type `map<string, bytes>`. This field is OPTIONAL and does not influence the processing of the results in any manner.

The general rules for the metadata field are identical to those of the [Jelly-RDF stream frame metadata](serialization.md#stream-frame-metadata). In particular, consumers SHOULD ignore unknown keys, and MUST NOT assume that the value of a key this specification does not define is a character string or valid UTF-8.

##### Well-known metadata keys

This specification defines the following well-known keys for the `metadata` field. The value of a well-known key MUST be valid UTF-8. Consumers SHOULD validate this, and SHOULD ignore the key if the value does not parse.

| Key      | Value |
| -------- | ----- |
| `link`   | Zero or more IRIs, separated by the LF character (U+000A). Corresponds to `head.link` in the [SPARQL Query Results JSON Format](https://www.w3.org/TR/sparql11-results-json/) and to the `<link>` elements of the [XML format](https://www.w3.org/TR/rdf-sparql-XMLres/). |

The `link` key describes the result set the frame belongs to as a whole, not the frame it appears in. Producers SHOULD set it only in the [first frame of the result set](#stream-types), and consumers SHOULD apply it to the whole result set.

All other keys are implementation-defined. Future versions of this specification may define further well-known keys.

### Stream options

The stream options is a message of type [`SparqlResultsOptions`](reference.md#sparqlresultsoptions). It MUST be set in the first frame of the stream. It MAY also be set in a later frame, which [resets the stream state](#repeating-the-stream-options). In a [`PUNCTUATED` stream](#stream-types), it may be set again only in the first frame of a result set.

The stream options instruct the consumer on the sizes of the lookup tables needed to decode the stream, and on the version of the format used.

The stream options message contains the following fields:

- `stream_name` (1) – name of the stream. This field is OPTIONAL and the manner in which it should be used is not defined by this specification. It MAY be used to identify the stream.
- `stream_type` (2) – the [stream type](#stream-types), as a [`SparqlStreamType`](reference.md#sparqlstreamtype) value. This field is OPTIONAL and defaults to `SPARQL_STREAM_TYPE_FLAT`, a single result set.
- `rdf_version` (5) – the version of RDF whose terms may occur in the stream, as an [`RdfVersion`](reference.md#rdfversion) value. This field is OPTIONAL and defaults to `RDF_VERSION_UNSPECIFIED`: no version is announced, and the consumer can assume RDF 1.2. See [RDF version](#rdf-version).
- `max_name_table_size` (9) – maximum size of the [name lookup](#prefix-name-and-datatype-lookup-entries). This field is REQUIRED and MUST be set to a value greater than or equal to 128. The consumer SHOULD throw an error otherwise. The size of the name lookup MUST NOT exceed the value of this field.
- `max_prefix_table_size` (10) – maximum size of the [prefix lookup](#prefix-name-and-datatype-lookup-entries). This field is OPTIONAL and defaults to 0 (no lookup). If the field is set to 0, the prefix lookup MUST NOT be used in the stream, and the consumer SHOULD throw an error if it is. If the field is set to a positive value, the prefix lookup SHOULD be used in the stream and the size of the prefix lookup MUST NOT exceed the value of this field.
- `max_datatype_table_size` (11) – maximum size of the [datatype lookup](#prefix-name-and-datatype-lookup-entries). This field is OPTIONAL and defaults to 0 (no lookup). If the field is set to 0, the datatype lookup MUST NOT be used in the stream, which effectively prohibits the use of datatype literals. The consumer SHOULD throw an error if it is used. If the field is set to a positive value, the datatype lookup SHOULD be used in the stream and the size of the lookup MUST NOT exceed the value of this field.
- `version` (15) – [version tag](#versioning) of the stream. This field is REQUIRED. The rules are the same as for the [Jelly-RDF `version` field](serialization.md#stream-options):
    - The version tag is encoded as a varint. The version tag MUST be greater than 0.
    - The producer of the stream MUST set the version tag to the version tag of the format that was used to serialize the stream.
    - It is RECOMMENDED that the producer uses the lowest possible version tag that is compatible with the features used in the stream.
    - The consumer SHOULD throw an error if the version tag is greater than the version tag of the implementation.
    - The consumer SHOULD throw an error if the version tag is zero.
    - The consumer SHOULD NOT throw an error if the version tag is not zero but lower than the version tag of the implementation.
    - The producer may use version tags greater than 10000 to indicate non-standard versions of the format.

This specification sets no upper bound on the lookup table sizes. Instead, as in [Jelly-RDF](serialization.md#overly-large-lookup-tables), each consumer SHOULD define the largest tables it is willing to allocate and reject a stream that asks for more – see [security considerations](#overly-large-lookup-tables). The RECOMMENDED defaults are **16384** names, **4096** prefixes, and **256** datatypes, and consumers SHOULD let the user raise or lower them.

#### Repeating the stream options (stream concatenation) { #repeating-the-stream-options }

This section describes `FLAT` streams. In a [`PUNCTUATED` stream](#stream-types), the stream options may be repeated only in the first frame of a result set. There, the lookups are emptied as described below, and the new options (such as the lookup sizes and `rdf_version`) apply from that frame on. They MUST be valid on their own, and the consumer MAY throw an error if it does not support them. The other rules of this section do not apply to `PUNCTUATED` streams.

A frame other than the first one MAY contain the stream options. Doing so **resets the state of the stream**:

- The name, prefix, and datatype lookups are emptied, and their identifier numbering restarts from 1.
- The [result set header](#result-set-header) ceases to be in effect – the same frame MUST restate it.
- A [trailer](#stream-trailer) without an error, seen earlier in the stream, ceases to apply. A trailer with an error does not – the result set stays incomplete.

The reset takes effect before anything else in the frame is processed. The restated header MUST declare the same variables, with the same names, in the same order, as the header of the first frame, because a `FLAT` stream always describes exactly one result set. The consumer MUST throw an error otherwise.

The repeated stream options need not be identical to the previous ones, but they MUST be valid on their own. The consumer MAY throw an error if it does not support the new options.

Blank node labels are **not** reset – they remain [scoped to the whole stream](#blank-node-columns).

!!! note "What this is for"

    This exists so that two Jelly-SPARQL files holding results of the same query can be concatenated into one valid file.

    It is **not** a general mid-stream reconfiguration mechanism, and it is **not** a way for a consumer to join a stream that is already in progress. If you want frames that can be decoded independently, see the [note on independently decodable frames](#ordering) instead.

!!! warning

    Because blank node labels are not reset, concatenating two files that happen to use the same blank node label will merge those blank nodes into one. If that matters for your use case, rename the labels of one of the files before concatenating.

### Result set header

The result set header declares the variables of the result set and maps each of them to one column. The header is stored in the `variables` field (2) of `SparqlResultsFrame` (repeated `SparqlVariable`).

The header MUST be present in the [first frame of a result set](#stream-types) with a solution sequence, and in every frame that [repeats the stream options](#repeating-the-stream-options). It MUST NOT be present in a frame with a [boolean result](#boolean-results).

The `SparqlVariable` message contains the following fields:

- `name` (1) – the name of the variable, without the leading `?` or `$`. It SHOULD conform to the [`VARNAME` production of SPARQL 1.1](https://www.w3.org/TR/2013/REC-sparql11-query-20130321/#rVARNAME). It MUST NOT be empty. Consumers are not required to check this.
- `column_index` (2) – 0-based index of the [column](#columns) that contains the values of this variable.

The variables MUST be listed in projection order, that is, in the order in which they appear in the `SELECT` clause of the query. Consumers MUST preserve this order.

The variable names in one header SHOULD be unique. Consumers are not required to check this.

#### Column indices

The `column_index` of a variable is an index into the *virtual concatenation* of all the column lists of a frame, taken in field number order: `iri_columns` (7) first, then `bnode_columns` (8), `literal_columns` (9), and finally `poly_columns` (10).

??? example "Example (click to expand)"

    If a frame has 2 IRI columns, 1 blank node column, and 2 literal columns, the column indices are assigned as follows:

    | Column               | `column_index` |
    | -------------------- | -------------- |
    | `iri_columns[0]`     | 0              |
    | `iri_columns[1]`     | 1              |
    | `bnode_columns[0]`   | 2              |
    | `literal_columns[0]` | 3              |
    | `literal_columns[1]` | 4              |

Let *N* be the number of variables declared by the header in effect for a frame. The following rules apply:

- A frame MUST contain either exactly *N* columns in total, counting all four column lists together, or no columns at all. The consumer MUST throw an error otherwise.
- A frame that contains no columns MUST have `row_count` equal to 0, unless *N* is 0. The consumer MUST throw an error otherwise.
- The `column_index` values of the header MUST form a permutation of the integers from 0 to *N* − 1, that is, every column MUST be referenced by exactly one variable. The consumer MUST throw an error otherwise.

!!! note

    Because the columns are grouped by type, the column order within a frame is generally not the projection order of the variables. The producer is free to assign the columns in any order that respects the grouping.

#### Restating the header

A later frame MAY restate the header to change the column layout in the middle of a stream. This is needed when the values of a variable stop fitting the column type used so far – for example, when a variable that was only bound to IRIs encounters a literal and has to move to a [polymorphic column](#polymorphic-columns).

The following rules apply to a restated header:

- It MUST list exactly the same variables, with the same names, in the same order, as the header of the first frame of the result set. Only the `column_index` values may differ. The consumer MUST throw an error if a restated header declares different variables.
- It takes effect for the frame it appears in, and for all subsequent frames, until it is restated again.
- A frame MAY restate a header identical to the one currently in effect. Producers SHOULD NOT do this, unless they are deliberately making every frame [independently decodable](#ordering).

#### Zero-variable result sets

A result set may have no variables at all. In this case the `variables` field is empty, and the `row_count` of each frame conveys the number of empty solutions in it. Frames of such a stream contain no columns.

An empty `variables` field in the [first frame of a result set](#stream-types), or in a frame with the [stream options](#stream-options) set, MUST be interpreted as declaring a zero-variable result set, unless the frame has a [boolean result](#boolean-results). An empty `variables` field in any other frame MUST be interpreted as "the header is not restated in this frame".

### Boolean results

A boolean result (the result of an `ASK` query) consists of exactly one frame, with the `ask_result` field (11) set to a [`SparqlAskResult`](reference.md#sparqlaskresult) message. The `SparqlAskResult` message has a single field:

- `value` (1) – the boolean value of the result. This field is OPTIONAL and defaults to `false`.

The following rules apply:

- The `ask_result` field MUST NOT be set in any frame other than the [first frame of a result set](#stream-types). The consumer SHOULD throw an error otherwise.
- The frame with a boolean result MUST NOT declare any variables, MUST NOT contain any columns, and MUST have `row_count` equal to 0. The consumer SHOULD throw an error otherwise.
- The frame with the boolean result is the only frame of its result set. In a `FLAT` stream, no frame may follow it. In a `PUNCTUATED` stream, the next frame, if any, MUST start a new result set, so the frame with the boolean result MUST then have a trailer. The consumer SHOULD throw an error otherwise.

Consequently, `FLAT` streams with boolean results cannot be concatenated the way [solution sequences can](#repeating-the-stream-options). To send several boolean results in one stream, use a [`PUNCTUATED` stream](#stream-types).

!!! note

    The `metadata` and `trailer` fields may still be used in a frame with a boolean result.

### Stream trailer

The `trailer` field (12) of `SparqlResultsFrame` contains a [`SparqlResultsTrailer`](reference.md#sparqlresultstrailer) message, which marks the end of a result set and says whether the result set is complete. The message has a single field:

- `error` (1) – an empty string (the default value) means the result set is complete. A non-empty value is a human-readable, UTF-8 explanation of why the producer could not produce the complete result.

The following rules apply:

- A producer MUST set the `trailer` field in the last frame of every result set, both when the result set is complete and when the producer stops because of an error it can report. The only case in which a result set ends without a trailer is when the producer cannot write one at all, for example because its process died or the connection was lost.
- In a `FLAT` stream, a frame with a trailer MUST NOT be followed by any frame without the [stream options](#stream-options). The consumer SHOULD throw an error otherwise. In other words: a trailer either ends the stream, or ends a segment of a concatenated stream. In a [`PUNCTUATED` stream](#stream-types), the frame after a trailer starts a new result set.
- A frame with a trailer MAY also contain rows, lookup entries, a header, or a boolean result. A producer that has nothing left to write MAY write a frame that contains only the trailer, with `row_count` equal to 0.
- If a consumer reaches the end of the stream without having seen a trailer for the last result set, it SHOULD treat that result set as truncated, and SHOULD report this to the caller.
- If a consumer sees a trailer with a non-empty `error`, it MUST treat the result set it ends as incomplete, and MUST signal an error to the caller. It MAY still hand over the rows it read before the trailer, and SHOULD include the message in the error. In a `FLAT` stream, this applies even if the stream options are [repeated](#repeating-the-stream-options) after the trailer, and the stream ends with a trailer without an error. In a `PUNCTUATED` stream, the error applies only to the result set it ends, and the stream may go on with the next result set.

!!! note "Why a trailer"

    A producer that fails part-way through a query (e.g., due to a federation timeout or a broken backend) has already written some rows by the time it finds out. Without a trailer, the bytes it has written are indistinguishable from a complete, shorter result set, and a consumer would silently return wrong answers.

!!! note

    A producer whose process dies outright cannot write a trailer at all. That is why the absence of a trailer means "likely truncated" rather than "complete".

### Prefix, name, and datatype lookup entries

Jelly-SPARQL uses the same lookup table mechanism as [Jelly-RDF](serialization.md#prefix-name-and-datatype-lookup-entries) to compress IRIs and datatypes. All the rules specified there apply here as well, with two differences: the entries are transmitted in a [packed form](#packed-lookup-entries), and there is an additional constraint on [the working set of a frame](#the-working-set-of-a-frame).

The lookup tables are stream-scoped: their contents are kept from one frame to the next, and their identifier numbering continues across frames – also from one result set to the next in a [`PUNCTUATED` stream](#stream-types).

#### Packed lookup entries

Lookup entries are stored in the following fields of `SparqlResultsFrame`. Each field contains a repeated [`RdfLookupEntryPacked`](reference.md#rdflookupentrypacked) message:

- `names` (4) – entries of the name lookup.
- `prefixes` (5) – entries of the prefix lookup.
- `datatypes` (6) – entries of the datatype lookup.

Lookup entries are often assigned consecutive identifiers. A packed entry states the identifier once and then lists the values of a whole run of consecutive entries, which saves the framing of every entry after the first.

The `RdfLookupEntryPacked` message contains the following fields:

- `id` (1) – 1-based identifier of the **first** value in this entry. The default value of 0 follows the same rule as in Jelly-RDF: it MUST be interpreted as `previous_id + 1`, where `previous_id` is the last identifier assigned by the previous entry of *the same lookup table* in the stream. If 0 appears in the first entry of a given lookup table in the stream, it MUST be interpreted as 1.
- `values` (2) – the values of the entries, in UTF-8. The first value is assigned the identifier `id`, and every following value is assigned the identifier of the previous one plus 1.

A packed entry with zero values MUST NOT be written. Consumers MAY throw an error if they encounter one.

#### The working set of a frame

All lookup entries of a frame are applied **before any column of the frame is decoded**. This allows the columns of a frame to be decoded independently of each other.

As a consequence, every lookup identifier referenced by the columns of a frame MUST still contain the intended value after all of the frame's entries have been applied. In other words: **the working set of a single frame must fit in the lookup tables.** A producer MUST NOT overwrite, within one frame, an identifier that the same frame's columns still refer to.

If a producer cannot satisfy this, it MUST end the frame and start a new one. If a single row cannot be encoded even in an otherwise empty frame, the producer MUST throw an error – the configured lookup table sizes are too small for these results.

!!! warning

    A consumer cannot detect a violation of this rule. It will silently decode the affected terms to the wrong values. This is a producer-side obligation.

!!! note

    A simple way to implement this on the producer's side is to track which identifiers the current frame has touched (assigned or referenced), and to end the frame before a row could touch an identifier that is already in that set. If the lookup uses an LRU eviction policy, everything the frame has touched sits at the recent end, so the frame stays safe exactly as long as it has not touched every identifier of the table.

### Columns

A column stores the cells of one variable across all `row_count` rows of a frame, in row order. A cell is either a **bound** RDF term or **unbound**.

There are four column types, each in its own repeated field of `SparqlResultsFrame`:

| Field                  | Message type                                            | Contains                   |
| ---------------------- | ------------------------------------------------------- | -------------------------- |
| `iri_columns` (7)      | [`SparqlIriColumn`](reference.md#sparqliricolumn)         | IRIs only                  |
| `bnode_columns` (8)    | [`SparqlBnodeColumn`](reference.md#sparqlbnodecolumn)     | blank nodes only           |
| `literal_columns` (9)  | [`SparqlLiteralColumn`](reference.md#sparqlliteralcolumn) | literals only              |
| `poly_columns` (10)    | [`SparqlPolyColumn`](reference.md#sparqlpolycolumn)       | RDF terms of any type      |

Producers SHOULD use a monomorphic column (IRI, blank node, or literal) whenever all the values of a variable in a frame are of the same type, and use a polymorphic column only for variables whose values mix term types.

Every column of a frame contains:

- A list of **run values** – the values of the column, with each run of consecutive equal values stored exactly once, and unbound cells not stored at all.
- The `layouts` list – a description of where the sequence of cells deviates from "each run value occupies exactly one cell", see [sequence layout](#sequence-layout).

A column whose cells are all unbound in a frame is encoded as an empty message, of any of the four types. A column MUST NOT decode to more than `row_count` cells. If it decodes to fewer, the remaining cells at the end of the column are unbound.

#### Sequence layout

The `layouts` field of every column type is a flat list of **exceptions** to the rule "each run value occupies exactly one cell". When every cell of a column is bound and no value repeats in consecutive rows, `layouts` is empty.

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

An unbound run sits **before** the run value at the current position, or after the last run value once all run values have been consumed. This makes the order of an unbound run and a repeat run at the same position unambiguous.

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

A frame is corrupt, and the consumer MUST throw an error, if any of the following is true for any of its columns:

- `i + skip > m` – a `skip` runs past the last run value.
- A repeat run starts when `i == m` – the run points past the last run value.
- `len_code` is 15 and the token is not followed by an extension varint.
- The column decodes to more than `row_count` cells.

Producers MUST merge adjacent runs. In particular, a producer MUST NOT emit two unbound runs separated by `skip == 0`. Producers SHOULD omit trailing unbound runs and rely on the padding rule instead (see: [Columns](#columns)).

!!! note

    A token stays a single byte as long as `skip <= 3`. Repeat runs of up to 16 cells and unbound runs of up to 15 cells fit in the token without an extension varint.

    The `skip` field occupies the upper 27 bits of the token, which is where the [maximum row count](#result-frames) of 2<sup>27</sup> − 1 comes from.

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

#### IRI columns

An IRI column is a [`SparqlIriColumn`](reference.md#sparqliricolumn) message with the following fields:

- `name_ids` (1) – the name identifiers of the run values, in row order. The length of this list is the number of run values in the column.
- `layouts` (2) – the [sequence layout](#sequence-layout).
- `prefix_ids` (3) – the prefix identifiers of the run values, in row order.

The IRIs are reconstructed exactly as in [Jelly-RDF](serialization.md#iris): the prefix and the name are resolved through the prefix and name lookups and concatenated.

The `name_ids` list follows the `name_id` inference rule of [`RdfIri`](serialization.md#iris): a value of 0 means "previous `name_id` + 1". **The inference state resets at the start of every column in every frame**, where 0 means `name_id = 1`.

The `prefix_ids` list MUST have one of three lengths:

| Length            | Meaning |
| ----------------- | ------- |
| 0                 | Every run value has `prefix_id = 0`, that is, no prefix. This is the case when the prefix lookup is disabled. |
| 1                 | Every run value uses the prefix given by the single entry. This is the case for a column of IRIs sharing one namespace. |
| `len(name_ids)`   | One entry per run value. |

In the third form, the `prefix_id` inference rule of `RdfIri` applies along the list: a value of 0 means "the same prefix as the previous IRI in this column". **The inference state resets at the start of every column in every frame**, starting from prefix 0 (no prefix).

The consumer MUST throw an error if the length of `prefix_ids` is none of the three allowed values.

!!! note "Difference from Jelly-RDF"

    In Jelly-RDF, the `prefix_id` and `name_id` inference state runs across the whole stream, in a strict order of rows and terms within rows. In Jelly-SPARQL it is **per column, per frame**. That is what lets a consumer decode the columns of a frame in any order, or in parallel, given only the lookup tables.

??? example "Example (click to expand)"

    A column holding, in four consecutive rows:

    ```
    https://a.org/x1
    https://a.org/x2
    https://a.org/x1
    https://b.org/z
    ```

    Assume the prefix lookup holds `https://a.org/` at id 1 and `https://b.org/` at id 2, and the name lookup holds `x1` at 1, `x2` at 2, and `z` at 3.

    ```protobuf
    SparqlIriColumn {
        name_ids: [0, 0, 1, 3]
        # 0 -> 0 + 1 = 1 (x1)
        # 0 -> 1 + 1 = 2 (x2)
        # 1 -> 1      (x1)
        # 3 -> 3      (z)
        prefix_ids: [1, 0, 0, 2]
        # 0 means "same prefix as the previous IRI"
        # layouts is empty: every cell is bound, no two consecutive cells are equal
    }
    ```

    The same column in a frame where every IRI is in the `https://a.org/` namespace would have `prefix_ids: [1]` instead – one entry for the whole column.

#### Blank node columns

A blank node column is a [`SparqlBnodeColumn`](reference.md#sparqlbnodecolumn) message with the following fields:

- `values` (1) – the run values, that is, the blank node labels, in row order.
- `layouts` (2) – the [sequence layout](#sequence-layout).

Blank node labels are represented as plain UTF-8 strings.

Blank node labels are **scoped to the result set**. In a `FLAT` stream, that is the entire result stream. In a [`PUNCTUATED` stream](#stream-types), it is each result set on its own. Two cells in one result set with the same label MUST be interpreted as referring to the same blank node, regardless of which frame they are in, and regardless of whether the [stream options were repeated](#repeating-the-stream-options) between them. Two cells with different labels MUST be interpreted as referring to different blank nodes. Two cells in different result sets of a `PUNCTUATED` stream MUST be interpreted as referring to different blank nodes, even if they have the same label.

#### Literal columns

A literal column is a [`SparqlLiteralColumn`](reference.md#sparqlliteralcolumn) message with the following fields:

- `lex_values` (1) – the lexical forms of the run values, in row order. The length of this list is the number of run values in the column.
- `layouts` (2) – the [sequence layout](#sequence-layout).
- `literal_kinds` (3) – the literal kinds of the run values, in row order, see below.
- `langtags` (4) – the language tags that the literal kinds refer to, as UTF-8 strings.
- `langtag_directions` (5) – the [base directions](#base-direction) of the language tags, parallel to `langtags`, as [`RdfBaseDirection`](reference.md#rdfbasedirection) values.

Each run value is a lexical form plus a **literal kind**, which says what sort of literal it is. A literal kind is an unsigned integer *v*:

| Literal kind *v*       | Meaning |
| ---------------------- | ------- |
| 0                      | A simple literal, that is, a literal with the datatype `http://www.w3.org/2001/XMLSchema#string`. |
| odd *v*                | A literal with the datatype of the [datatype lookup](#prefix-name-and-datatype-lookup-entries) entry with identifier (*v* + 1) / 2. |
| even *v* > 0           | A language-tagged string with the language tag `langtags[`*v* / 2 − 1`]` (a 0-based index), and the base direction `langtag_directions[`*v* / 2 − 1`]`. |

So the datatype identifiers 1, 2, 3, … are the literal kinds 1, 3, 5, …, and the language tags at the indices 0, 1, 2, … are the literal kinds 2, 4, 6, ….

The `literal_kinds` list MUST have one of three lengths:

| Length              | Meaning |
| ------------------- | ------- |
| 0                   | Every run value is a simple literal. |
| 1                   | Every run value has the literal kind given by the single entry. This is the case for a column of values that share one datatype, or one language tag and base direction. |
| `len(lex_values)`   | One entry per run value. |

The consumer MUST throw an error if the length of `literal_kinds` is none of the three allowed values, or if a literal kind refers to an index past the end of `langtags`.

The following rules apply to the language tags:

- Each entry of `langtags` SHOULD be a valid [BCP 47](https://tools.ietf.org/html/bcp47) language tag.
- Producers SHOULD list the language tags in the order in which the run values first use them, and SHOULD NOT list a language tag that is not used by any run value. Consumers are not required to check this.
- The same language tag MAY appear in `langtags` more than once, with different base directions. Producers SHOULD NOT list the same pair of language tag and base direction twice.
- `langtag_directions` MUST be empty, or have exactly as many entries as `langtags`. An empty list means that no language tag of the column has a base direction. The consumer MUST throw an error if the list has any other length.
- Consumers are not required to check the entries of `langtag_directions` that are not used by any run value.
- Producers SHOULD leave `langtag_directions` empty in a stream that declares `RDF_VERSION_1_1`, because such a stream has no [base directions](#base-direction).

A literal kind that refers to a datatype MUST NOT refer to an entry containing `http://www.w3.org/1999/02/22-rdf-syntax-ns#langString` or `http://www.w3.org/1999/02/22-rdf-syntax-ns#dirLangString`, because a literal with that datatype and no language tag is not a valid RDF term. Language-tagged strings always use a language tag from `langtags`. The consumer SHOULD throw an error otherwise.

A simple literal does not need an `xsd:string` entry in the datatype lookup: the producer can use the literal kind 0 instead. A literal kind referring to an `xsd:string` entry is also legal and produces the same result.

!!! note

    This design allows for efficiently storing columns in which every value has the same literal kind – think of a `?count` column, or a `?label` column filtered to one language.

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
    SparqlLiteralColumn {
        lex_values: ["cat", "42", "chat", "dog"]
        literal_kinds: [2, 1, 4, 2]
        # 2 -> langtags[0] (en)
        # 1 -> datatype 1 (xsd:integer)
        # 4 -> langtags[1] (fr)
        langtags: ["en", "fr"]
        # langtag_directions is empty: no base directions
    }
    ```

    A column of the same four rows, but with every value tagged `@en`, would have `literal_kinds: [2]` and `langtags: ["en"]` instead.

#### Polymorphic columns

A polymorphic column is a [`SparqlPolyColumn`](reference.md#sparqlpolycolumn) message. It stores RDF terms of any type. Its run values are split by term type into **sub-columns**, one per type, and the `kinds` field says which sub-column stores each run value. The message has the following fields:

- `kinds` (1) – the term kind of each run value, in row order, see below.
- `layouts` (2) – the [sequence layout](#sequence-layout) of the whole column.
- `iris` (3) – the IRIs of the column, as a [`SparqlIriColumn`](reference.md#sparqliricolumn).
- `literals` (4) – the literals of the column, as a [`SparqlLiteralColumn`](reference.md#sparqlliteralcolumn).
- `bnodes` (5) – the blank nodes of the column, as a [`SparqlBnodeColumn`](reference.md#sparqlbnodecolumn).
- `triple_terms` (6) – the [triple terms](#triple-terms) of the column, each an [`RdfTripleTerm`](reference.md#rdftripleterm) message.

The run values of each sub-column are read exactly as in the monomorphic column of the same type: an IRI sub-column as an [IRI column](#iri-columns), with its own `name_id` and `prefix_id` inference state, a literal sub-column as a [literal column](#literal-columns), with its own literal kinds and language tags, and a blank node sub-column as a [blank node column](#blank-node-columns). The sub-columns do not have a sequence layouts of their own: the producer MUST NOT set their `layouts` field. The consumer SHOULD ignore it, and MAY throw an error if it is set. A sub-column that is not set has no run values.

The **number of run values** of a polymorphic column is the total number of run values in its sub-columns, including the triple terms.

The `kinds` field packs one term kind per run value into 2 bits, four run values per byte, starting from the least significant bits of the first byte:

| Term kind | Meaning |
| --------- | ------- |
| 0         | The next run value of `iris`. |
| 1         | The next run value of `literals`. |
| 2         | The next run value of `bnodes`. |
| 3         | The next run value of `triple_terms`. |

The run values of the column are obtained by going through the term kinds in order, and taking the next run value from the sub-column corresponding to that kind. Then the `layouts` of the column are applied to these run values, as in any other column.

The consumer MUST throw an error if any of the following is true:

- `kinds` does not have exactly ⌈*m* / 4⌉ bytes, where *m* is the number of run values of the column.
- The unused bits of the last byte of `kinds` are not 0.
- The `kinds` field refers to more run values of a sub-column than the sub-column has.

Like in the monomorphic columns, the inference state of each sub-column resets at the start of every column in every frame.

!!! note

    Keeping the values of each type in their own sub-column means that the IRIs of a polymorphic column are still two flat lists of integers, and its literals are a list of strings. The cost of mixing types is 2 bits per run value.

??? example "Example (click to expand)"

    A column containing, in five consecutive rows:

    ```
    https://a.org/x
    _:b1
    "hello"
    "hello"
    https://a.org/y
    ```

    Assume the prefix lookup contains `https://a.org/` at id 1, and the name lookup has `x` at 1 and `y` at 2. The run values are `x`, `_:b1`, `"hello"`, `y`, with the term kinds 0, 2, 1, 0, and `"hello"` occupies two cells.

    ```protobuf
    SparqlPolyColumn {
        layouts: [64]
        # skip = 2, repeat run of 2 cells
        kinds: "\x18"
        # 0b00_01_10_00: iri, bnode, literal, iri (least significant bits first)
        iris: { name_ids: [0, 0], prefix_ids: [1] }
        literals: { lex_values: ["hello"] }
        bnodes: { values: ["b1"] }
    }
    ```

### RDF terms

#### RDF version

The `rdf_version` field (5) of the [stream options](#stream-options) announces which RDF terms may occur in the stream. Its values follow the [version labels of RDF 1.2](https://www.w3.org/TR/rdf12-concepts/#defined-version-labels):

| `RdfVersion` value            | Version label | Base directions | Triple terms |
| ----------------------------- | ------------- | --------------- | ------------ |
| `RDF_VERSION_UNSPECIFIED` (0) | none          | yes             | yes          |
| `RDF_VERSION_1_1` (1)         | `1.1`         | no              | no           |
| `RDF_VERSION_1_2_BASIC` (2)   | `1.2-basic`   | yes             | no           |
| `RDF_VERSION_1_2` (3)         | `1.2`         | yes             | yes          |

The following rules apply:

- If `rdf_version` is `RDF_VERSION_UNSPECIFIED`, no version is announced, and the consumer can assume RDF 1.2: the stream MAY contain any term of RDF 1.2.
- The consumer MUST throw an error if `rdf_version` has a value that is not listed above.
- Producers SHOULD declare a version. It is RECOMMENDED to declare the lowest version that allows every term the producer knows in advance it may write. A producer that cannot know in advance which terms the results will contain (for example, because it streams them from a store that supports RDF 1.2) MAY declare a higher version than the terms turn out to need.
- If a version is declared, the stream MUST NOT contain a term that the version does not allow. If it does, the consumer MAY throw an error, or it MAY ignore the declared version and read the term.
- A consumer that does not support the declared version SHOULD throw an error when it reads the stream options, rather than when it first meets a term it cannot represent.
- When the stream options are [repeated](#repeating-the-stream-options), the new `rdf_version` applies from that frame on.

#### Base direction

In RDF 1.2, a language-tagged string may have a base direction: `ltr` (left-to-right) or `rtl` (right-to-left). Such a literal has the datatype `http://www.w3.org/1999/02/22-rdf-syntax-ns#dirLangString`.

A base direction is an [`RdfBaseDirection`](reference.md#rdfbasedirection) value: `RDF_BASE_DIRECTION_UNSPECIFIED` (0, the default: no base direction), `RDF_BASE_DIRECTION_LTR` (1), or `RDF_BASE_DIRECTION_RTL` (2). It is encoded in the `langtag_directions` field of [literal columns](#literal-columns), and in the `direction` field of [literals in triple terms](#literals-in-triple-terms).

The following rules apply:

- The consumer MUST throw an error if the base direction of a literal has a value that is not listed above.
- A stream that declares `RDF_VERSION_1_1` MUST NOT contain a literal with a base direction other than `RDF_BASE_DIRECTION_UNSPECIFIED`.

<!-- Note for editors: the following 3 sub-sections are here temporarily until we move them to Jelly-RDF 1.2 -->

#### Triple terms

A triple term is encoded as an [`RdfTripleTerm`](reference.md#rdftripleterm) message. Triple terms can only occur in [polymorphic columns](#polymorphic-columns), in the `triple_terms` field (6) of `SparqlPolyColumn`, and not in a stream that declares `RDF_VERSION_1_1` or `RDF_VERSION_1_2_BASIC`. If `triple_terms` is not empty in such a stream, the consumer MAY throw an error (see [RDF version](#rdf-version)).

`RdfTripleTerm` has the following fields:

- the `subject` oneof – `s_iri` (1), an `RdfIri`, or `s_bnode` (2), a blank node label;
- `p_iri` (5) – the predicate, an `RdfIri`;
- the `object` oneof – `o_iri` (9), an `RdfIri`; `o_bnode` (10), a blank node label; `o_literal` (11), an `RdfLiteral2` (see [below](#literals-in-triple-terms)); or `o_triple_term` (12), a nested `RdfTripleTerm`.

The following rules apply:

- The subject, the predicate, and the object MUST all be set. The consumer MUST throw an error if any of them is missing.
- The IRIs of all the triple terms of one polymorphic column share one `RdfIri` inference state. It follows the rules of [`RdfIri`](serialization.md#iris) in Jelly-RDF: a `name_id` of 0 means "previous `name_id` + 1", and a `prefix_id` of 0 means "the same prefix as the previous IRI". It advances through the triple terms in order, and through the IRIs of each triple term in the order subject, predicate, object, recursively into nested triple terms.
- This state is separate from the state of the `iris` sub-column. Like the other inference states, it resets at the start of every column in every frame, where a `name_id` of 0 means 1 and a `prefix_id` of 0 means no prefix.
- The blank node labels of a triple term have the same [scope](#blank-node-columns) as all other blank node labels in the stream.
- Triple terms may be nested up to arbitrary depth. The consumer SHOULD throw an error if the depth of the nesting exceeds the capabilities of the implementation.

##### Literals in triple terms

A literal in the object position of a triple term is an [`RdfLiteral2`](reference.md#rdfliteral2) message. Its fields 1–3 (`lex`, `langtag`, `datatype`) are the same as in the [`RdfLiteral`](serialization.md#literals) message of Jelly-RDF, so a literal without a base direction is encoded in exactly the same bytes in both. `RdfLiteral2` adds the `direction` field (4), with the [base direction](#base-direction) of a language-tagged string.

The following rules apply:

- `direction` MUST NOT be set unless `langtag` is set. The consumer MUST throw an error otherwise.
- `datatype` MUST NOT be 0, and MUST NOT refer to `rdf:langString` or `rdf:dirLangString`. The consumer MUST throw an error if it is 0, and SHOULD throw an error if it refers to `rdf:langString` or `rdf:dirLangString`.

<!-- DONE SO FAR -->

## Delimited variant of Jelly-SPARQL {#delimited}

Protobuf messages [are not self-delimiting](https://protobuf.dev/programming-guides/techniques/#streaming), so a byte stream holding more than one message needs a delimiter between them. Jelly-SPARQL uses the same convention as [Jelly-RDF](serialization.md#delimited-variant-of-jelly): a Protobuf varint holding the length of the message in bytes, prepended before it.

A byte stream in the **delimited variant** consists of a series of delimited `SparqlResultsFrame` messages.

A Jelly-SPARQL stream stored in a file, or sent in an HTTP message body, with the `application/x-jelly-sparql` [media type](#internet-media-type-and-file-extension) MUST use the delimited variant. This applies also when the stream consists of a single frame.

Transports that provide their own message framing (for example gRPC, MQTT, or Kafka) send one bare, non-delimited `SparqlResultsFrame` message per transport message.

## Internet media type and file extension

The RECOMMENDED media type for Jelly-SPARQL is `application/x-jelly-sparql`. The RECOMMENDED file extension is `.jellys`.

The same media type is used for solution sequences and for boolean results – the two are distinguished by the contents of the first frame of each result set, not by the media type. The same holds for the [stream type](#stream-types), which is set in the stream options.

The bytes MUST be in the [delimited variant](#delimited).

### Use with the SPARQL 1.1 Protocol

A service implementing the [SPARQL 1.1 Protocol](https://www.w3.org/TR/sparql11-protocol/) MAY offer Jelly-SPARQL as a query results format. The following applies:

- Jelly-SPARQL is a results format for `SELECT` and `ASK` queries. `CONSTRUCT` and `DESCRIBE` queries return RDF graphs, and should use [Jelly-RDF](serialization.md) (`application/x-jelly-rdf`) instead.
- A service that streams the response SHOULD flush the connection after each frame, so that the client can start processing solutions before the query has finished.
- A service that fails part-way through a query MUST write a [trailer](#stream-trailer) with a non-empty `error` before closing the connection, unless it cannot write anything more. The HTTP status line has already been sent by then, so the trailer is the only place left to say what went wrong.

!!! note

    The last point is the main practical reason for the trailer. A `200 OK` response whose body stops early looks exactly like a complete, shorter result set.

## Security considerations

*This section is not part of the specification.*

The same security considerations apply to Jelly-SPARQL as to [Jelly-RDF](serialization.md#security-considerations), in particular those about Protocol Buffers, [overly large lookup tables](#overly-large-lookup-tables), and invalid lookup entry identifiers.

### Overly large lookup tables

For untrusted input, consumers must always validate that the requested sizes of the name, prefix, and datatype lookup tables are not overly large and are supported by the consumer. A malicious producer could attempt to exhaust the memory of the consumer by requesting a lookup table of several gigabytes or more. This would constitute a denial-of-service vector. See also the [Jelly-RDF specification](serialization.md#overly-large-lookup-tables).

The recommended mitigation is the same as in Jelly-RDF: each implementation defines a maximum allowed lookup size and checks the requested size against it, rejecting the stream if it is larger. The limit should be configurable, so that a user who trusts the producer can raise it.

The sizes RECOMMENDED as defaults for that limit are 16384 names, 4096 prefixes, and 256 datatypes. They are larger than the Jelly-RDF defaults because a frame of SPARQL results touches more distinct terms than a frame of RDF statements does, and because [the working set of a frame must fit in the tables](#the-working-set-of-a-frame).

### Overly large row counts

The `row_count` field of a frame is not bounded by the size of the frame: a frame of a few bytes can declare a row count in the tens of millions. A consumer that allocates a per-row buffer of `row_count` elements before decoding the columns would be a denial-of-service vector.

The recommended mitigation is to grow the decoding buffers to the size actually needed as the columns are decoded, and to validate `row_count` against a configurable limit before allocating anything.

### Column layouts

The layout tokens of a column decide how many cells the consumer will emit when decoding the column. A consumer must validate every token against the number of run values it actually has and against `row_count`, as described in [sequence layout](#sequence-layout), before emitting anything. In particular, the extension varint of an escaped length token is attacker-controlled and must not be trusted to fit into the remaining space of the row buffer.

### Deeply nested triple terms

`RdfTripleTerm` is a recursive message: the object of a triple term may be another triple term. A malicious producer could send a triple term nested deeply enough to overflow the consumer's stack while parsing or converting it. The recommended mitigation is the same as in [Jelly-RDF](serialization.md#infinite-recursion-of-rdf-star-quoted-triples): limit the nesting depth accepted by the Protocol Buffers parser. A consumer that does not support triple terms can also reject any stream that declares `RDF_VERSION_1_2` up front. It cannot do so for a stream that declares no version, so it still needs the depth limit.

### Query results content

Jelly-SPARQL is a general serialization format for SPARQL query results, and as such may be used to transmit malicious or misleading content. Please refer to the [security considerations of the SPARQL 1.1 Query Results JSON Format](https://www.w3.org/TR/sparql11-results-json/) and to the [RDF 1.1 Turtle W3C Recommendation](https://www.w3.org/TR/turtle/#sec-mediaReg).

## Implementations

*This section is not part of the specification.*

The following implementations of Jelly-SPARQL are available:

- [Jelly-JVM implementation]({{ jvm_link() }})
    - Implemented actors: producer, consumer
    - Supported libraries: [Apache Jena](https://jena.apache.org/), [RDF4J](https://rdf4j.org/)

## See also

- [Jelly-RDF serialization format specification](serialization.md)
- [Jelly-Patch format specification](patch.md)
- [Jelly Protobuf reference](reference.md)
