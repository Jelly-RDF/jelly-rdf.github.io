# Jelly SPARQL query results format specification

**This document is the specification of the Jelly SPARQL query results format, also known as Jelly-SPARQL. It is intended for implementers of Jelly libraries and applications.** If you are looking for a user-friendly introduction to Jelly, see the [Jelly index page](index.md).

Jelly-SPARQL is a binary serialization format for **SPARQL query results** – solution sequences (`SELECT`) and boolean results (`ASK`). It is binary, streamable, and reuses the RDF term encoding of [Jelly-RDF](serialization.md).

This document is accompanied by the [Jelly Protobuf reference](reference.md) and the Protobuf definitions themselves ([`sparql.proto`]({{ git_proto_link('sparql.proto') }}) and [`rdf.proto`]({{ git_proto_link('rdf.proto') }})).

The following assumptions are used in this document:

- Jelly-SPARQL reuses Protobuf messages and encoding rules from the [Jelly RDF serialization format](serialization.md), version `{{ proto_version() }}`. Concepts, definitions, and Protobuf messages defined there apply also here, unless explicitly stated otherwise.
- The basis for the terms used is the RDF 1.2 specification ([W3C Candidate Recommendation Snapshot 07 April 2026](https://www.w3.org/TR/rdf12-concepts/)). The format also supports an RDF 1.1 mode.
- The basis for the terms related to query results is the SPARQL 1.2 Query Language specification ([W3C Working Draft 21 September 2026](https://www.w3.org/TR/sparql12-query/)), in particular the definitions of a *solution*, a *solution sequence*, and a *query variable*.
- In parts referring to the semantics of result sets, the SPARQL 1.2 Query Results JSON Format ([W3C Working Draft 13 August 2026](https://www.w3.org/TR/sparql12-results-json/)) is used.
- All strings in the serialization are assumed to be UTF-8 encoded.

| Document information | |
| --- | --- |
| **Author:** | [Piotr Sowiński](https://ostrzyciel.eu) ([Ostrzyciel](https://github.com/Ostrzyciel)), Anastasiya Danilenka ([adanilenka](https://github.com/adanilenka)) |
| **Version:** | {{ sparql_version() }} |
| **Date:** | {{ git_revision_date_localized }} |
| **Permanent URL:** | [`https://w3id.org/jelly/{{ proto_version() }}/specification/sparql`](https://w3id.org/jelly/{{ proto_version() }}/specification/sparql) |
| **Document status**: | {{ specification_status(sparql_version()) }} |
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

| Version tag | Semantic version | Last release date | Changes                         |
| ----------- | ---------------- | ----------------- | ------------------------------- |
| 1           | 1.0.0            | October 23, 2026  | (initial version)               |

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

Jelly-SPARQL uses [Protocol Buffers version 3](https://protobuf.dev/programming-guides/proto3/) as the underlying serialization format. All implementations MUST use a compliant Protocol Buffers implementation. The Protocol Buffers schema for Jelly-SPARQL is defined in `sparql.proto` ([source code]({{ git_proto_link('sparql.proto') }}), [reference](reference.md#sparqlproto)), which imports `rdf.proto`.

A Jelly-SPARQL **result stream** is an ordered sequence of **result frames**. The frames may be sent one-by-one using a streaming protocol (e.g., gRPC, MQTT, Kafka) or written in sequence to a byte stream (e.g., a file or socket) – see the [delimited variant](#delimited).

A result stream contains one or more result sets – see [stream types](#stream-types). Each result set is one of the two kinds of SPARQL query results:

- A **solution sequence** – an ordered sequence of solutions (rows). Each solution binds a subset of the result variables to RDF terms.
- A **boolean result** – a single `true` or `false` value, as produced by an `ASK` query.

The kind of a result set is determined by the [first frame of the result set](#stream-types): if the `ask_result` field is set in it, the result set is a boolean result. Otherwise, it is a solution sequence.

Within a frame, solutions are stored **column-wise**: one column per result variable. The columns are the same as in Jelly-RDF – see [columns](#columns). Most variables in real result sets are bound to terms of a single type, so most columns are just one or two flat lists of primitives.

!!! note

    See the [Jelly-RDF specification](serialization.md#format-specification) for why Jelly uses columns.

### Stream types

A result stream represents either a single result set, or a sequence of result sets. This is set by the `stream_type` field (2) of the [stream options](#stream-options), a [`SparqlStreamType`](reference.md#sparqlstreamtype) value:

- `SPARQL_STREAM_TYPE_FLAT` (0) – default value. The entire stream is a single result set, ended by a [trailer](#stream-trailer).
- `SPARQL_STREAM_TYPE_PUNCTUATED` (1) – the stream is a sequence of result sets, each ended by a [trailer](#stream-trailer).

The consumer MUST throw an error if `stream_type` has a value that is not listed above.

The first frame of the stream is the **first frame of a result set**. In a `PUNCTUATED` stream, every frame that directly follows a frame with a trailer is also the first frame of a result set.

The following rules apply to `PUNCTUATED` streams:

- A result set consists of one or more consecutive frames, starting with the first frame of the result set and ending with the first frame that has a trailer.
- Each result set is either a solution sequence or a boolean result, decided by its own first frame. The result sets are independent of each other: they may declare different variables. Solution sequences and boolean results may be mixed in one stream.
- The [lookup tables](#prefix-name-and-datatype-lookup-entries) are kept from one result set to the next.
- [Blank node labels](#blank-nodes) are scoped to a single result set.
- The stream options MUST NOT be set in a frame other than the first frame of a result set. The consumer MUST throw an error otherwise.

The value of `stream_type` MUST be the same in all stream options of a stream. The consumer MUST throw an error otherwise.

Consumers are not required to support `PUNCTUATED` streams. A consumer that does not support them SHOULD throw an error when it reads the stream options.

!!! note "What `PUNCTUATED` streams are for"

    Some applications produce many result sets, one after another: a continuous query that is evaluated once per window, a pub/sub topic with the answers to a stream of queries, or a file with the results of a batch of queries.

!!! note

    Concatenating two `PUNCTUATED` streams gives a valid `PUNCTUATED` stream with the result sets of both, in order, as long as the last result set of the first stream ends with a trailer. If it does not (for example, because the producer crashed), the stream options of the second stream end up in the middle of a result set, which is not allowed.

### Result frames

A result frame is a message of type [`SparqlResultsFrame`](reference.md#sparqlresultsframe). A frame contains a batch of rows (solutions), together with any [lookup entries](#prefix-name-and-datatype-lookup-entries) it needs. It is RECOMMENDED to keep the serialized size of a frame below 1 MB.

A result stream MUST contain at least one frame. An empty input (zero bytes) is not a valid result stream, and the consumer MUST throw an error if it reads one. The first frame MUST contain the [stream options](#stream-options) and either the [result set header](#result-set-header) or the [boolean result](#boolean-results).

The number of rows in a frame is given by the `row_count` field (3). It MUST NOT be greater than 2<sup>27</sup> − 1, which is the largest number of cells the [sequence layout](serialization.md#sequence-layout) of a column can address. The consumer MUST throw an error otherwise.

!!! note

    In practice the row count is bounded far below 2<sup>27</sup> − 1 by the recommended frame size.

The frames of a result stream have no meaning of their own – they are purely a batching mechanism. In particular, a frame boundary on its own does not separate one result set from another – only a [trailer](#stream-trailer) in a [`PUNCTUATED` stream](#stream-types) does.

!!! note

    Because a frame is just a batch of rows, the producer is free to choose the batch size. A good default is to size the frames in *values* (cells) rather than rows, since the cost of a row grows with the number of variables: 4096 values means 4096 rows of a one-variable result set, but only 204 rows of a 20-variable one.

    The producer may also have to end a frame early, when the [lookup tables fill up](serialization.md#the-working-set-of-a-batch).

#### Ordering

Result frames MUST be processed strictly in order. Each frame MUST be processed in its entirety before the next frame is processed.

The order of rows within a frame, and the order of the frames, together define the order of the solution sequence, and the order of the result sets in a [`PUNCTUATED` stream](#stream-types). Consumers MUST preserve this order.

Implementations MAY choose to adopt a **non-standard** solution where the order or delivery of the frames is not guaranteed. The implementation MUST clearly specify in the documentation that it uses such a non-standard solution.

!!! note

    See also the notes about the practical implications of this in the [Jelly-RDF specification](serialization.md#ordering).

!!! note "Making frames independently decodable"

    As in [Jelly-RDF](serialization.md#ordering), a producer that re-emits all the lookup entries it needs in **every** frame makes each frame decodable on its own. In Jelly-SPARQL, decoding a frame also needs the header of its result set.

#### Frame metadata

`SparqlResultsFrame` messages have a `metadata` field (15) of type `map<string, bytes>`. This field is OPTIONAL and does not influence the processing of the results in any manner.

The general rules for the metadata field are identical to those of the [Jelly-RDF stream frame metadata](serialization.md#stream-frame-metadata). In particular, consumers SHOULD ignore unknown keys, and MUST NOT assume that the value of a key this specification does not define is a character string or valid UTF-8.

##### Well-known metadata keys

This specification defines the following well-known keys for the `metadata` field. The value of a well-known key MUST be valid UTF-8. Consumers SHOULD validate this, and SHOULD ignore the key if the value does not parse.

| Key      | Value |
| -------- | ----- |
| `link`   | Zero or more IRIs, separated by the LF character (U+000A). Corresponds to `head.link` in the [SPARQL 1.2 Query Results JSON Format](https://www.w3.org/TR/sparql12-results-json/) and to the `<link>` elements of the [XML format](https://www.w3.org/TR/sparql12-results-xml/). |

The `link` key describes the result set the frame belongs to as a whole, not the frame it appears in. Producers SHOULD set it only in the [first frame of the result set](#stream-types), and consumers SHOULD apply it to the whole result set.

All other keys are implementation-defined. Future versions of this specification may define further well-known keys.

### Stream options

The stream options is a message of type [`SparqlResultsOptions`](reference.md#sparqlresultsoptions). It MUST be set in the first frame of the stream. It MAY also be set in a later frame, which [resets the stream state](#repeating-the-stream-options). In a [`PUNCTUATED` stream](#stream-types), it may be set again only in the first frame of a result set.

The stream options instruct the consumer on the sizes of the lookup tables needed to decode the stream, and on the version of the format used.

The stream options message contains the following fields:

- `stream_name` (1) – name of the stream. This field is OPTIONAL and the manner in which it should be used is not defined by this specification. It MAY be used to identify the stream.
- `stream_type` (2) – the [stream type](#stream-types), as a [`SparqlStreamType`](reference.md#sparqlstreamtype) value. This field is OPTIONAL and defaults to `SPARQL_STREAM_TYPE_FLAT`, a single result set.
- `rdf_version` (5) – the [version of RDF](#rdf-version) whose terms may occur in the stream, as an [`RdfVersion`](reference.md#rdfversion) value. This field is OPTIONAL and defaults to `RDF_VERSION_UNSPECIFIED`.
- `max_name_table_size` (9), `max_prefix_table_size` (10), and `max_datatype_table_size` (11) – maximum sizes of the [lookup tables](#prefix-name-and-datatype-lookup-entries). The rules for these fields are the same as for the fields with the same names in the [Jelly-RDF stream options](serialization.md#stream-options). In particular, `max_name_table_size` is REQUIRED and MUST be at least 128.
- `version` (15) – [version tag](#versioning) of the stream. This field is REQUIRED. The rules listed in the [Jelly-RDF version tag](serialization.md#version-tag) section apply, using the version tags of Jelly-SPARQL. The Jelly-RDF rule about version tags 1 and 2 does not apply.

The limits on the lookup table sizes that consumers SHOULD apply, and their RECOMMENDED defaults, are the same as in [Jelly-RDF](serialization.md#stream-options).

#### Repeating the stream options (stream concatenation) { #repeating-the-stream-options }

This section describes `FLAT` streams. In a [`PUNCTUATED` stream](#stream-types), the stream options may be repeated only in the first frame of a result set. There, the lookups are emptied as described below, and the new options (such as the lookup sizes and `rdf_version`) apply from that frame on. They MUST be valid on their own, and the consumer MAY throw an error if it does not support them. The other rules of this section do not apply to `PUNCTUATED` streams.

A frame other than the first one MAY contain the stream options. Doing so **resets the state of the stream**:

- The name, prefix, and datatype lookups are emptied, and their identifier numbering restarts from 1, as in [Jelly-RDF](serialization.md#restating-the-stream-options).
- The [result set header](#result-set-header) ceases to be in effect – the same frame MUST repeat it.
- A [trailer](#stream-trailer) without an error, seen earlier in the stream, ceases to apply: the result set does not end there, and the rows of the following frames are added to it. A trailer with an error does not cease to apply – the result set stays incomplete.

The reset takes effect before anything else in the frame is processed. The repeated header MUST declare the same variables, with the same names, in the same order, as the header of the first frame, because a `FLAT` stream always describes exactly one result set. The consumer MUST throw an error otherwise.

The repeated stream options need not be identical to the previous ones, but they MUST be valid on their own. The consumer MAY throw an error if it does not support the new options.

Blank node labels are **not** reset – they remain [scoped to the whole stream](#blank-nodes).

!!! note "What this is for"

    This exists so that two Jelly-SPARQL files holding results of the same query can be concatenated into one valid file.

    It is **not** a general mid-stream reconfiguration mechanism, and it is **not** a way for a consumer to join a stream that is already in progress. If you want frames that can be decoded independently, see the [note on independently decodable frames](#ordering) instead.

!!! warning

    Because blank node labels are not reset, concatenating two files that happen to use the same blank node label will merge those blank nodes into one. If that matters for your use case, rename the labels of one of the files before concatenating.

### Result set header

The result set header declares the variables of the result set. It is stored in the `variables` field (2) of `SparqlResultsFrame`, as a list of strings: the names of the variables.

The header MUST be present in the [first frame of a result set](#stream-types) with a solution sequence, and in every frame that [repeats the stream options](#repeating-the-stream-options), unless the frame has a [boolean result](#boolean-results). It MUST NOT be present in a frame with a boolean result, or in any other frame. The consumer MUST throw an error if a header is present in a frame that is neither the first frame of a result set nor a frame with the stream options.

The following rules apply to the variable names:

- A name is given without the leading `?` or `$`. It SHOULD conform to the [`VARNAME` production of SPARQL 1.2](https://www.w3.org/TR/sparql12-query/#rVARNAME). It MUST NOT be empty. Consumers MAY check this.
- The variables MUST be listed in projection order, that is, in the order in which they appear in the `SELECT` clause of the query. Consumers MUST preserve this order.
- The variable names in one header SHOULD be unique. Consumers MAY check this.

#### Zero-variable result sets

A result set may have no variables at all. In this case the `variables` field is empty, and the `row_count` of each frame conveys the number of empty solutions in it. Frames of such a stream contain no columns.

An empty `variables` field in the [first frame of a result set](#stream-types), or in a frame with the [stream options](#stream-options) set, MUST be interpreted as declaring a zero-variable result set, unless the frame has a [boolean result](#boolean-results).

### Boolean results

A boolean result (the result of an `ASK` query) consists of exactly one frame, with the `ask_result` field (8) set to a [`SparqlAskResult`](reference.md#sparqlaskresult) message. The `SparqlAskResult` message has a single field:

- `value` (1) – the boolean value of the result. This field is OPTIONAL and defaults to `false`.

The following rules apply:

- The `ask_result` field MUST NOT be set in any frame other than the [first frame of a result set](#stream-types). The consumer SHOULD throw an error otherwise.
- The frame with a boolean result MUST NOT declare any variables, MUST NOT contain any columns, and MUST have `row_count` equal to 0. The consumer SHOULD throw an error otherwise.
- The frame with the boolean result is the only frame of its result set. In a `FLAT` stream, no frame may follow it. In a `PUNCTUATED` stream, the next frame, if any, MUST start a new result set, so the frame with the boolean result MUST then have a trailer. The consumer SHOULD throw an error otherwise.

Consequently, `FLAT` streams with boolean results cannot be concatenated the way [solution sequences can](#repeating-the-stream-options). To send several boolean results in one stream, use a [`PUNCTUATED` stream](#stream-types).

!!! note

    The `metadata` and `trailer` fields may still be used in a frame with a boolean result.

### Stream trailer

The `trailer` field (9) of `SparqlResultsFrame` contains a [`SparqlResultsTrailer`](reference.md#sparqlresultstrailer) message, which marks the end of a result set and says whether the result set is complete. The message has a single field:

- `error` (1) – an empty string (the default value) means the result set is complete. A non-empty value is a human-readable, UTF-8 explanation of why the producer could not produce the complete result.

The following rules apply:

- A producer MUST set the `trailer` field in the last frame of every result set, both when the result set is complete and when the producer stops because of an error it can report. The only case in which a result set ends without a trailer is when the producer cannot write one at all, for example because its process died or the connection was lost.
- In a `FLAT` stream, a frame with a trailer MUST NOT be followed by any frame without the [stream options](#stream-options). The consumer SHOULD throw an error otherwise. In other words: a trailer either ends the stream, or ends a segment of a concatenated stream. In a [`PUNCTUATED` stream](#stream-types), the frame after a trailer starts a new result set.
- A frame with a trailer MAY also contain rows, lookup entries, a header, or a boolean result. A producer that has nothing left to write MAY end a solution sequence with a frame that contains only the trailer, with `row_count` equal to 0. This is not possible after a frame with a boolean result, which must have the trailer itself. In a `PUNCTUATED` stream, a frame with only a trailer that directly follows another frame with a trailer does not end the previous result set: it is a result set of its own, with zero variables and no solutions.
- If a consumer reaches the end of the stream without having seen a trailer for the last result set, it SHOULD treat that result set as truncated, and SHOULD report this to the caller. A missing trailer is not an error in the stream: the consumer MUST NOT reject the rows it has read only because the trailer is missing.
- If a consumer sees a trailer with a non-empty `error`, it MUST treat the result set it ends as incomplete, and MUST signal an error to the caller. It MAY still hand over the rows it read before the trailer, and SHOULD include the message in the error. In a `FLAT` stream, this applies even if the stream options are [repeated](#repeating-the-stream-options) after the trailer, and the stream ends with a trailer without an error. In a `PUNCTUATED` stream, the error applies only to the result set it ends, and the stream may go on with the next result set.

!!! note "Why a trailer"

    A producer that fails part-way through a query (e.g., due to a federation timeout or a broken backend) has already written some rows by the time it finds out. Without a trailer, the bytes it has written are indistinguishable from a complete, shorter result set, and a consumer would silently return wrong answers.

!!! note

    A producer whose process dies outright cannot write a trailer at all. That is why the absence of a trailer means "likely truncated" rather than "complete".

!!! note "Trailers in boolean results"

    A [boolean result](#boolean-results) (the result of an `ASK` query) is a single frame, so that frame is both the first and the last frame of its result set. It therefore also contains the trailer, next to the `ask_result` field. The trailer works the same as in a solution sequence: an empty `error` means the result is complete, and a non-empty `error` means the consumer must treat the result as incomplete and signal an error to the caller.

### Prefix, name, and datatype lookup entries

Jelly-SPARQL uses the same lookup table mechanism as [Jelly-RDF](serialization.md#prefix-name-and-datatype-lookup-entries) to compress IRIs and datatypes, including [packed lookup entries](serialization.md#packed-lookup-entries) and the rule that [the working set of a batch](serialization.md#the-working-set-of-a-batch) must fit in the lookup tables. All the rules specified there apply here as well, where a batch is one `SparqlResultsFrame`, and a statement is one row (solution).

The packed lookup entries are stored in the following fields of `SparqlResultsFrame`:

- `names` (4) – entries of the name lookup.
- `prefixes` (5) – entries of the prefix lookup.
- `datatypes` (6) – entries of the datatype lookup.

The lookup tables are stream-scoped: their contents are kept from one frame to the next, and their identifier numbering continues across frames – also from one result set to the next in a [`PUNCTUATED` stream](#stream-types).

### Columns

The columns of a frame are stored in the `columns` field (7) of `SparqlResultsFrame`, each as an [`RdfColumn`](reference.md#rdfcolumn) message. The *i*-th column contains the values of the *i*-th variable of the [result set header](#result-set-header), in row order. A bound cell is the value of the variable in that solution. An unbound cell means that the variable is not bound in that solution.

The columns are encoded as described in the [Jelly-RDF specification](serialization.md#columns): [term types](serialization.md#term-types), [sequence layout](serialization.md#sequence-layout), [IRIs](serialization.md#iris-in-columns), [literals](serialization.md#literals-in-columns), [blank nodes](serialization.md#blank-nodes-in-columns), and [triple terms](serialization.md#triple-terms-in-columns). A column may contain any type of RDF term, and any of its cells may be unbound.

Let *N* be the number of variables of the result set. The following rules apply:

- A frame MUST contain either exactly *N* columns, or zero columns. The consumer MUST throw an error otherwise.
- A frame that contains no columns MUST have `row_count` equal to 0, unless *N* is 0. The consumer MUST throw an error otherwise.

#### Blank nodes

Blank node labels are **scoped to the result set**. In a `FLAT` stream, that is the entire result stream. In a [`PUNCTUATED` stream](#stream-types), it is each result set on its own. Two cells in one result set with the same label MUST be interpreted as referring to the same blank node, regardless of which frame they are in, and regardless of whether the [stream options were repeated](#repeating-the-stream-options) between them. Two cells with different labels MUST be interpreted as referring to different blank nodes. Two cells in different result sets of a `PUNCTUATED` stream MUST be interpreted as referring to different blank nodes, even if they have the same label. The same applies to the blank node labels in triple terms.

### RDF version

The `rdf_version` field (5) of the [stream options](#stream-options) announces which RDF terms may occur in the stream. Its values and rules are the same as for the [`rdf_version` field of Jelly-RDF](serialization.md#rdf-version). The [base directions](serialization.md#base-direction) of literals and [triple terms](serialization.md#triple-terms) are also encoded as in Jelly-RDF.

## Delimited variant of Jelly-SPARQL { #delimited }

Jelly-SPARQL uses the same [delimited variant as Jelly-RDF](serialization.md#delimited-variant-of-jelly), and the same rules apply: a byte stream in the delimited variant consists of a series of delimited `SparqlResultsFrame` messages. A producer that writes a Jelly-SPARQL stream to a file, or sends it in an HTTP message body with the `application/x-jelly-sparql` [media type](#internet-media-type-and-file-extension), MUST use the delimited variant.

!!! note "Delimited streams and `PUNCTUATED` streams"

    The two are unrelated and work at different levels:

    - The **delimited variant** is about how the **frames** are separated in a byte stream. Each frame is prefixed with its length, so that a consumer reading a file or a socket knows where one frame ends and the next one starts. It is not needed with transports that send each frame as a separate message (for example gRPC, MQTT, or Kafka).
    - The [**`PUNCTUATED` stream type**](#stream-types) is about how the **result sets** are separated in a stream. Each result set ends with a [trailer](#stream-trailer). It is set in the stream options and does not depend on the transport.

## Internet media type and file extension

The RECOMMENDED media type for Jelly-SPARQL is `application/x-jelly-sparql`. The RECOMMENDED file extension is `.jellys`.

The same media type is used for solution sequences and for boolean results – the two are distinguished by the contents of the first frame of each result set, not by the media type. The same holds for the [stream type](#stream-types), which is set in the stream options.

The bytes MUST be in the [delimited variant](#delimited).

### Use with the SPARQL 1.2 Protocol

A service implementing the [SPARQL 1.2 Protocol](https://www.w3.org/TR/sparql12-protocol/) MAY offer Jelly-SPARQL as a query results format. The following applies:

- Jelly-SPARQL is a results format for `SELECT` and `ASK` queries. `CONSTRUCT` and `DESCRIBE` queries return RDF graphs, and should use [Jelly-RDF](serialization.md) (`application/x-jelly-rdf`) instead.
- A service that streams the response SHOULD flush the connection after each frame, so that the client can start processing solutions before the query has finished.
- A service that fails part-way through a query MUST write a [trailer](#stream-trailer) with a non-empty `error` before closing the connection, unless it cannot write anything more. The HTTP status line has already been sent by then, so the trailer is the only place left to say what went wrong.

!!! note

    The last point is the main practical reason for the trailer. A `200 OK` response whose body stops early looks exactly like a complete, shorter result set.

## Security considerations

*This section is not part of the specification.*

The same security considerations apply to Jelly-SPARQL as to [Jelly-RDF](serialization.md#security-considerations): Protocol Buffers, [overly large lookup tables](serialization.md#overly-large-lookup-tables), invalid lookup entry identifiers, [overly large row counts](serialization.md#overly-large-row-counts), [column layouts](serialization.md#column-layouts), and [deeply nested triple terms](serialization.md#deeply-nested-triple-terms).

### Query results content

Jelly-SPARQL is a general serialization format for SPARQL query results, and as such may be used to transmit malicious or misleading content. Please refer to the [security considerations of the SPARQL 1.2 Query Results JSON Format](https://www.w3.org/TR/sparql12-results-json/#security) and to the [RDF 1.2 Turtle specification](https://www.w3.org/TR/rdf12-turtle/#sec-mediaReg).

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
