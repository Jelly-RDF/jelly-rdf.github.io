# Jelly SPARQL results format specification

!!! warning

    Jelly-SPARQL is an early draft and is **not** finalized. Both the Protobuf definition and this document are expected to change. Do not use it in production, and do not write long-lived files with it yet. Feedback is very welcome – **[open an issue on GitHub](https://github.com/Jelly-RDF/jelly-protobuf/issues/new/choose)**.

!!! danger "This document is ahead of the Protobuf definition"

    Some of the rules below are not yet reflected in `sparql.proto`, and are not yet implemented anywhere:

    - the [stream trailer](#stream-trailer) needs a new `SparqlResultsTrailer` message and a new field in `SparqlResultsFrame`;
    - [repeated stream options](#repeating-the-stream-options), the [maximum row count](#result-frames), and [frames that omit their columns](#frames-with-no-rows) need the Protobuf comments and the implementations to be updated.

**This document is the specification of the Jelly SPARQL results format, also known as Jelly-SPARQL. It is intended for implementers of Jelly libraries and applications.** If you are looking for a user-friendly introduction to Jelly, see the [Jelly index page](index.md).

Jelly-SPARQL is a binary serialization format for **SPARQL query results** – solution sequences (`SELECT`) and boolean results (`ASK`). It plays the same role as the [SPARQL Query Results XML](https://www.w3.org/TR/rdf-sparql-XMLres/), [JSON](https://www.w3.org/TR/sparql11-results-json/), and [CSV/TSV](https://www.w3.org/TR/sparql11-results-csv-tsv/) formats, but it is binary, streamable, and reuses the RDF term encoding of [Jelly-RDF](serialization.md).

This document is accompanied by the [Jelly Protobuf reference](reference.md) and the Protobuf definitions themselves ([`sparql.proto`]({{ git_proto_link('sparql.proto') }}) and [`rdf2.proto`]({{ git_proto_link('rdf2.proto') }})).

The following assumptions are used in this document:

- Jelly-SPARQL reuses Protobuf messages and encoding rules from the [Jelly RDF serialization format](serialization.md), version `{{ proto_version() }}`. Concepts, definitions, and Protobuf messages defined there apply also here, unless explicitly stated otherwise.
- The basis for the terms used is the RDF 1.1 specification ([W3C Recommendation 25 February 2014](https://www.w3.org/TR/2014/REC-rdf11-concepts-20140225/)).
- The basis for the terms related to query results is the SPARQL 1.1 Query Language specification ([W3C Recommendation 21 March 2013](https://www.w3.org/TR/2013/REC-sparql11-query-20130321/)), in particular the definitions of a *solution*, a *solution sequence*, and a *query variable*.
- In parts referring to the semantics of result sets, the SPARQL 1.1 Query Results JSON Format ([W3C Recommendation 21 March 2013](https://www.w3.org/TR/2013/REC-sparql11-results-json-20130321/)) is used.
- All strings in the serialization are assumed to be UTF-8 encoded.

| Document information | |
| --- | --- |
| **Author:** | [Piotr Sowiński](https://ostrzyciel.eu) ([Ostrzyciel](https://github.com/Ostrzyciel)) |
| **Version:** | experimental (dev) |
| **Date:** | {{ git_revision_date_localized }} |
| **Permanent URL:** | [`https://w3id.org/jelly/{{ proto_version() }}/specification/sparql`](https://w3id.org/jelly/{{ proto_version() }}/specification/sparql) |
| **Document status**: | Experimental draft specification |
| **License:** | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

{% include "./includes/start_info.md" %}

## Conformance

{% include "./includes/conformance.md" %}

### Test suite

The Jelly-SPARQL conformance test suite does not exist yet. Until it does, implementations cannot claim conformance with this specification in the sense used by [Jelly-RDF](serialization.md#conformance).

The planned shape of the test suite, for implementers who want to prepare for it, is the following:

- Machine-readable manifests live in the [jelly-protobuf repository](https://github.com/Jelly-RDF/jelly-protobuf) under `test/sparql`, using the same manifest vocabulary as the [Jelly-RDF test cases](../conformance/rdf-test-cases.md).
- There are two directions of tests, as in Jelly-RDF:
    - **From Jelly (parse)** – the input is a `.jellys` file, and the expected output is the same result set in another format.
    - **To Jelly (serialize)** – the input is a result set in another format plus a file holding the stream options to use, and the expected output is a `.jellys` file.
- Test cases beginning with `pos_` are positive tests and those beginning with `neg_` are negative tests, exactly as in Jelly-RDF.
- Expected result sets are expressed in the [SPARQL Query Results JSON Format](https://www.w3.org/TR/sparql11-results-json/) (`.srj`), which can express everything Jelly-SPARQL can: bound and unbound variables, all three term types, and boolean results.
- Two result sets are considered equivalent when they have the same variables in the same order, the same number of solutions in the same order, and there is a bijection between the blank node labels of the two result sets under which the solutions are pairwise equal.
- All test files use the [delimited variant](#framing).

!!! note

    Comparing result sets is stricter than comparing RDF graphs: the order of solutions and the number of duplicates both matter, because both are significant in SPARQL. Only blank node labels are compared up to renaming.

## Versioning

The format follows the [Semantic Versioning 2.0](https://semver.org/) scheme. Each MAJOR.MINOR semantic version corresponds to an integer version tag in the format. The version tag is encoded in the `version` field of the [`SparqlResultsOptions`](reference.md#sparqlresultsoptions) message. See also the [section on stream options](#stream-options) for more information on how to handle the version tags in serialized streams.

The following versions of the format are defined:

| Version tag | Semantic version    | Last release date                 | Changes                         |
| ----------- | ------------------- | --------------------------------- | ------------------------------- |
| 1           | 1.0.0               | Not finalized yet (draft)         | (initial version)               |

Jelly-SPARQL has its own version tag, which is independent of the version tags of [Jelly-RDF](serialization.md#versioning) and [Jelly-Patch](patch.md#versioning). A version tag value MUST NOT be compared across formats.

!!! note

    Releases of the protocol are published on [GitHub](https://github.com/Jelly-RDF/jelly-protobuf/releases).

### Backward compatibility

{% include "./includes/back_compat.md" %}

### Forward compatibility

{% include "./includes/forward_compat.md" %}

!!! note

    See also the notes about the practical implications of this in the [Jelly-RDF specification](serialization.md#forward-compatibility).

### Planned for future versions

*This section is not part of the specification.*

Two features are known to be missing from version 1 and are planned for a future version of Jelly-SPARQL:

- **RDF 1.2 terms** – [`SparqlTerm`](#polymorphic-columns) has no field for triple terms, and `RdfLiteral` cannot carry a base direction, so SPARQL 1.2 result sets using these cannot be represented. See [RDF terms](#rdf-terms).
- **Per-column language tags** – a single language-tagged literal currently forces a whole literal column out of its compact form. See [literal columns](#literal-columns).

## Actors and implementations

Jelly-SPARQL assumes there to be two actors involved in processing the stream: the producer (writer) and the consumer (reader). The producer is responsible for serializing the SPARQL query results into the Jelly-SPARQL format, and the consumer is responsible for parsing the Jelly-SPARQL format into SPARQL query results.

Implementations may include only the producer, only the consumer, or both.

## Format specification

Jelly-SPARQL uses [Protocol Buffers version 3](https://protobuf.dev/programming-guides/proto3/) as the underlying serialization format. All implementations MUST use a compliant Protocol Buffers implementation. The Protocol Buffers schema for Jelly-SPARQL is defined in `sparql.proto` ([source code]({{ git_proto_link('sparql.proto') }}), [reference](reference.md#sparqlproto)), which imports `rdf.proto` and `rdf2.proto`.

A Jelly-SPARQL **result stream** is an ordered sequence of **result frames**. The frames may be sent one-by-one using a streaming protocol (e.g., an HTTP response, MQTT, Kafka) or written in sequence to a byte stream (e.g., a file or socket) – see [framing](#framing).

A result stream carries exactly one of the two kinds of SPARQL query results:

- a **solution sequence** – an ordered sequence of solutions (rows), each binding a subset of the result variables to RDF terms;
- a **boolean result** – a single `true` or `false` value, as produced by an `ASK` query.

The kind of the result is determined by the first frame of the stream and MUST NOT change within a stream. A result stream always describes exactly one result set.

Within a frame, solutions are stored **column-wise**: one column per result variable, with the columns grouped by the type of the RDF terms they hold. Most variables in real result sets are bound to terms of a single type (most often IRIs), which lets the values of such a column be stored as a flat list of primitives instead of one Protobuf message per value.

!!! note "Why columns?"

    In a row-oriented layout, every bound value needs its own length-delimited sub-message with a `oneof` selecting the term type, which costs several bytes of framing per value and one object per value on the consumer's side. Grouping the values of one variable together means the term type is stated once per column instead of once per value, values that repeat in consecutive rows can be collapsed cheaply, and a reader can keep a whole column in a primitive array.

### Result frames

A result frame is a message of type [`SparqlResultsFrame`](reference.md#sparqlresultsframe). A frame carries a batch of rows (solutions), together with any [lookup entries](#prefix-name-and-datatype-lookup-entries) it needs. It is RECOMMENDED to keep the serialized size of a frame below 1 MB.

A result stream MUST contain at least one frame. The first frame MUST carry the [stream options](#stream-options) and either the [result set header](#result-set-header) or the [boolean result](#boolean-results).

The number of rows in a frame is given by the `row_count` field (3). It MUST NOT be greater than 2<sup>27</sup> − 1, which is the largest number of cells the [sequence layout](#sequence-layout) of a column can address.

!!! note

    In practice the row count is bounded far below 2<sup>27</sup> − 1 by the recommended frame size: a frame of a few hundred kilobytes cannot hold anywhere near a hundred million rows. The limit only exists so that the format has a fixed bound that does not depend on the contents of the columns.

The frames of a result stream carry no semantics of their own – they are purely a batching mechanism. In particular, a frame boundary does not separate one result set from another.

!!! note

    Because a frame is just a batch of rows, the producer is free to choose the batch size. A good default is to size the frames in *values* (cells) rather than rows, since the cost of a row grows with the number of variables: 4096 values means 4096 rows of a one-variable result set, but only 204 rows of a 20-variable one.

    The producer may also have to end a frame early, when the [lookup tables fill up](#the-working-set-of-a-frame).

#### Ordering

Result frames MUST be processed strictly in order. Each frame MUST be processed in its entirety before the next frame is processed.

The order of rows within a frame, and the order of the frames, together define the order of the solution sequence. Consumers MUST preserve this order, and MUST NOT deduplicate rows – both the order and the cardinality of a solution sequence are significant in SPARQL.

Implementations MAY choose to adopt a **non-standard** solution where the order or delivery of the frames is not guaranteed. The implementation MUST clearly specify in the documentation that it uses such a non-standard solution.

!!! note

    See also the notes about the practical implications of this in the [Jelly-RDF specification](serialization.md#ordering).

!!! note "Making frames independently decodable"

    Because the [IRI inference state resets per column, per frame](#iri-columns), a frame can be decoded using only the stream options, the lookup table state, and the header in effect. A producer that re-emits all the lookup entries its columns use, and restates the header, in **every** frame makes each frame decodable on its own, given the stream options.

    This costs space – the lookup entries are repeated in every frame – but it is the way to build a stream whose frames can be dropped or processed out of order. Note that a consumer still needs the stream options from the first frame; [repeating them](#repeating-the-stream-options) is not a way to join a stream mid-way.

#### Frame metadata

`SparqlResultsFrame` messages have a `metadata` field (15) of type `map<string, bytes>`. This field is OPTIONAL and does not influence the processing of the results in any manner.

The general rules for the metadata field are identical to those of the [Jelly-RDF stream frame metadata](serialization.md#stream-frame-metadata). In particular, consumers SHOULD ignore unknown keys, and MUST NOT assume that the value of a key this specification does not define is a character string or valid UTF-8.

##### Well-known metadata keys

This specification defines the following well-known keys. The value of a well-known key MUST be valid UTF-8. Consumers SHOULD validate this, and SHOULD ignore the key if the value does not parse.

| Key      | Value |
| -------- | ----- |
| `link`   | Zero or more IRIs, separated by the LF character (U+000A). Corresponds to `head.link` in the [SPARQL Query Results JSON Format](https://www.w3.org/TR/sparql11-results-json/) and to the `<link>` elements of the [XML format](https://www.w3.org/TR/rdf-sparql-XMLres/). |

The `link` key describes the result set as a whole, not the frame it appears in. Producers SHOULD set it only in the frame that carries the [result set header](#result-set-header), and consumers SHOULD apply it to the whole result set.

All other keys are implementation-defined. Future versions of this specification may define further well-known keys.

!!! note

    An IRI cannot contain an LF character, so splitting the value of `link` on LF is unambiguous. A single link is simply a value with no LF in it.

### Stream options

The stream options is a message of type [`SparqlResultsOptions`](reference.md#sparqlresultsoptions). It MUST be set in the first frame of the stream. It MAY also be set in a later frame, which [resets the stream state](#repeating-the-stream-options). Consumers MAY throw an error if the stream options are not present in the first frame. Alternatively, they MAY use their own, implementation-specified default options.

The stream options instruct the consumer on the sizes of the lookup tables needed to decode the stream, and on the version of the format used.

The stream options message contains the following fields:

- `stream_name` (1) – name of the stream. This field is OPTIONAL and the manner in which it should be used is not defined by this specification. It MAY be used to identify the stream. It has the same meaning as in [Jelly-RDF](serialization.md#stream-options) – it may be used for, e.g., topic names in a pub/sub system.
- `max_name_table_size` (9) – maximum size of the [name lookup](#prefix-name-and-datatype-lookup-entries). This field is REQUIRED and MUST be set to a value greater than or equal to 128. The size of the lookup MUST NOT exceed the value of this field.
- `max_prefix_table_size` (10) – maximum size of the [prefix lookup](#prefix-name-and-datatype-lookup-entries). This field is OPTIONAL and defaults to 0 (no lookup). If the field is set to 0, the prefix lookup MUST NOT be used in the stream. If the field is set to a positive value, the prefix lookup SHOULD be used in the stream and the size of the lookup MUST NOT exceed the value of this field.
- `max_datatype_table_size` (11) – maximum size of the [datatype lookup](#prefix-name-and-datatype-lookup-entries). This field is OPTIONAL and defaults to 0 (no lookup). If the field is set to 0, the datatype lookup MUST NOT be used in the stream, which effectively prohibits the use of datatype literals. If the field is set to a positive value, the datatype lookup SHOULD be used in the stream and the size of the lookup MUST NOT exceed the value of this field.
- `version` (15) – [version tag](#versioning) of the stream. This field is REQUIRED. The rules are the same as for the [Jelly-RDF `version` field](serialization.md#stream-options):
    - The version tag is encoded as a varint. The version tag MUST be greater than 0.
    - The producer of the stream MUST set the version tag to the version tag of the format that was used to serialize the stream.
    - It is RECOMMENDED that the producer uses the lowest possible version tag that is compatible with the features used in the stream.
    - The consumer SHOULD throw an error if the version tag is greater than the version tag of the implementation.
    - The consumer SHOULD throw an error if the version tag is zero.
    - The consumer SHOULD NOT throw an error if the version tag is not zero but lower than the version tag of the implementation.
    - The producer may use version tags greater than 10000 to indicate non-standard versions of the format.

This specification sets no upper bound on the lookup table sizes. Instead, as in [Jelly-RDF](serialization.md#overly-large-lookup-tables), each consumer SHOULD define the largest tables it is willing to allocate and reject a stream that asks for more – see [security considerations](#overly-large-lookup-tables). The RECOMMENDED defaults are **16384** names, **4096** prefixes, and **256** datatypes, and consumers SHOULD let the user raise or lower them.

The minimum name table size of 128 is higher than Jelly-RDF's minimum of 8. A solution sequence is a projection, so one row of results tends to touch far more distinct terms than one RDF statement does. On top of that, [the working set of a whole frame must fit in the tables](#the-working-set-of-a-frame), so a producer given a tiny name table would have to cut the frames down to very few rows, or fail outright.

!!! note

    There are no fields for the physical stream type, logical stream type, generalized statements, or RDF-star. None of them apply to SPARQL results: a result stream is always a sequence of solutions, and only RDF terms that can be bound to a query variable can occur in it.

    The field numbers of `SparqlResultsOptions` are deliberately aligned with those of [`RdfStreamOptions`](reference.md#rdfstreamoptions), which is why there are gaps at 2–8 and 12–14.

#### Repeating the stream options

A frame other than the first one MAY carry the stream options. Doing so **resets the state of the stream**:

- the name, prefix, and datatype lookups are emptied, and their identifier numbering restarts from 1;
- the [result set header](#result-set-header) ceases to be in effect – the same frame MUST restate it;
- any [trailer](#stream-trailer) seen earlier in the stream ceases to apply.

The reset takes effect before anything else in the frame is processed. The restated header MUST declare the same variables, with the same names, in the same order, as the header of the first frame, because a result stream always describes exactly one result set. The consumer SHOULD throw an error otherwise.

The repeated stream options need not be identical to the previous ones, but they MUST be valid on their own. The consumer MAY throw an error if it does not support the new options.

Blank node labels are **not** reset – they remain [scoped to the whole stream](#blank-node-columns).

!!! note "What this is for"

    This exists so that two Jelly-SPARQL files holding results of the same query can be concatenated into one valid file, without either of them having to know about the other. That is the only intended use.

    It is **not** a general mid-stream reconfiguration mechanism, and it is **not** a way for a consumer to join a stream that is already in progress. If you want frames that can be decoded independently, see the [note on independently decodable frames](#ordering) instead.

!!! warning

    Because blank node labels are not reset, concatenating two files that happen to use the same blank node label will merge those blank nodes into one. If that matters for your use case, rename the labels of one of the files before concatenating.

### Result set header

The result set header declares the variables of the result set and maps each of them to one column. It is the `variables` field (2) of `SparqlResultsFrame`, a repeated [`SparqlVariable`](reference.md#sparqlvariable) message.

The header MUST be present in the first frame of a stream carrying a solution sequence, and in every frame that [repeats the stream options](#repeating-the-stream-options). It MUST NOT be present in a stream carrying a [boolean result](#boolean-results).

The `SparqlVariable` message contains the following fields:

- `name` (1) – the name of the variable, without the leading `?` or `$`. It SHOULD conform to the [`VARNAME` production of SPARQL 1.1](https://www.w3.org/TR/2013/REC-sparql11-query-20130321/#rVARNAME). An empty string (the default value) is allowed, but NOT RECOMMENDED.
- `column_index` (2) – 0-based index of the [column](#columns) that holds the values of this variable.

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
- A frame that contains no columns MUST have `row_count` equal to 0, unless *N* is 0. See [frames with no rows](#frames-with-no-rows).
- The `column_index` values of the header MUST form a permutation of the integers from 0 to *N* − 1, that is, every column MUST be referenced by exactly one variable. The consumer SHOULD throw an error otherwise.

!!! note

    Because the columns are grouped by type, the column order within a frame is generally not the projection order of the variables. The `column_index` field is what ties the two together, and the producer is free to assign the columns in any order that respects the grouping.

#### Restating the header

A later frame MAY restate the header to change the column layout in the middle of a stream. This is needed when the values of a variable stop fitting the column type used so far – for example, when a variable that has only held IRIs encounters a literal and has to move to a [polymorphic column](#polymorphic-columns).

The following rules apply to a restated header:

- It MUST list exactly the same variables, with the same names, in the same order, as the header of the first frame. Only the `column_index` values (and, consequently, the number of columns of each type in the frame) may differ. The consumer SHOULD throw an error if a restated header declares different variables.
- It takes effect for the frame it appears in, and for all subsequent frames, until it is restated again.
- A frame MAY restate a header identical to the one currently in effect. Producers SHOULD NOT do this, unless they are deliberately making every frame [independently decodable](#ordering).

#### Zero-variable result sets

A result set may have no variables at all. In this case the `variables` field is empty, and the `row_count` of each frame conveys the number of empty solutions in it. Frames of such a stream contain no columns.

An empty `variables` field in a frame that carries the [stream options](#stream-options) MUST be interpreted as declaring a zero-variable result set, unless the frame carries a [boolean result](#boolean-results). An empty `variables` field in any other frame MUST be interpreted as "the header is not restated in this frame".

### Boolean results

A stream that carries the result of an `ASK` query consists of exactly one frame, with the `ask_result` field (11) set to a [`SparqlAskResult`](reference.md#sparqlaskresult) message. The `SparqlAskResult` message has a single field:

- `value` (1) – the boolean value of the result. This field is OPTIONAL and defaults to `false`.

The following rules apply:

- The `ask_result` field MUST NOT be set in any frame other than the first frame of the stream.
- The frame carrying a boolean result MUST NOT declare any variables, MUST NOT contain any columns, and MUST have `row_count` equal to 0. The consumer SHOULD throw an error otherwise.
- No further result content may follow in the stream. The consumer SHOULD throw an error if any frame follows the frame carrying the boolean result.

Consequently, streams carrying boolean results cannot be concatenated the way [solution sequences can](#repeating-the-stream-options).

!!! note

    The `metadata` and `trailer` fields may be used in a frame carrying a boolean result – neither is result content.

!!! note

    A boolean result frame is tiny (a handful of bytes). It is still a complete Jelly-SPARQL stream, with the stream options and everything else a reader expects.

### Stream trailer

The `trailer` field (12) of `SparqlResultsFrame` holds a [`SparqlResultsTrailer`](reference.md#sparqlresultstrailer) message, which marks the end of the stream and says whether the result set is complete. The message has a single field:

- `error` (1) – an empty string (the default value) means the result set is complete. A non-empty value is a human-readable, UTF-8 explanation of why the producer could not produce the complete result.

The following rules apply:

- The `trailer` field is OPTIONAL. Producers SHOULD set it in the last frame they write.
- A frame that carries a trailer MUST NOT be followed by any frame that does not carry the [stream options](#stream-options). In other words: a trailer ends the stream, or ends a segment of a concatenated stream.
- A frame carrying a trailer MAY also carry rows, lookup entries, a header, or a boolean result. A producer that has nothing left to write MAY write a frame that carries only the trailer, with `row_count` equal to 0.
- If a consumer reaches the end of the stream without having seen a trailer, it SHOULD treat the result set as possibly truncated, and SHOULD report this to the caller.
- If a consumer sees a trailer with a non-empty `error`, it MUST treat the result set as incomplete, and SHOULD report the message to the caller.
- The rows delivered before an `error` trailer are valid solutions and MAY be used. The stream simply stops short of the full solution sequence.

!!! note "Why a trailer"

    A producer that fails part-way through a query – a timeout, a broken backend, a cancelled request – has already written some rows by the time it finds out. Without a trailer, the bytes it has written are indistinguishable from a complete, shorter result set, and a consumer would silently return wrong answers. The same gap exists in the SPARQL Query Results XML and JSON formats.

    The trailer also tells a consumer that a stream ended on purpose rather than because the connection dropped, which is not something the transport can always answer.

!!! note

    A producer whose process dies outright cannot write a trailer at all. That is why the absence of a trailer means "possibly truncated" rather than "complete".

### Prefix, name, and datatype lookup entries

Jelly-SPARQL uses the same lookup table mechanism as [Jelly-RDF](serialization.md#prefix-name-and-datatype-lookup-entries) to compress IRIs and datatypes. All the rules specified there apply here as well, with two differences: the entries are transmitted in a [packed form](#packed-lookup-entries), and there is an additional constraint on [the working set of a frame](#the-working-set-of-a-frame).

The lookup tables are stream-scoped: their contents carry over from one frame to the next, and their identifier numbering continues across frames, until the stream options are [repeated](#repeating-the-stream-options).

#### Packed lookup entries

Lookup entries are carried in the following fields of `SparqlResultsFrame`, each a repeated [`RdfLookupEntryPacked`](reference.md#rdflookupentrypacked) message:

- `names` (4) – entries of the name lookup.
- `prefixes` (5) – entries of the prefix lookup.
- `datatypes` (6) – entries of the datatype lookup.

Lookup entries are almost always assigned consecutive identifiers, because that is what the `id = 0` rule of the unpacked Jelly-RDF entries optimizes for. A packed entry states the identifier once and then lists the values of a whole run of consecutive entries, which saves the framing of every entry after the first.

The `RdfLookupEntryPacked` message contains the following fields:

- `id` (1) – 1-based identifier of the **first** value in this entry. The default value of 0 follows the same rule as in Jelly-RDF: it MUST be interpreted as `previous_id + 1`, where `previous_id` is the identifier assigned by the previous entry of *the same lookup table* in the stream. If 0 appears in the first entry of a given lookup table in the stream, it MUST be interpreted as 1.
- `values` (2) – the values of the entries, in UTF-8. The first value is assigned the identifier `id`, and every following value is assigned the identifier of the previous one plus 1.

A packed entry with no values at all is a no-op and MUST NOT be written. Consumers MAY throw an error if they encounter one.

!!! note

    The packing is per frame: a producer starts a new packed entry in every frame, even when the identifiers would continue the run of the previous frame. The identifier numbering itself, however, does run across frames.

!!! note

    `RdfLookupEntryPacked` is defined in `rdf2.proto` rather than `sparql.proto`, because it is shared with future versions of Jelly-RDF. The same message type is used for all three lookup tables.

#### The working set of a frame

All lookup entries of a frame are applied, in order, **before any column of the frame is decoded**. This is what makes the columns of a frame decodable independently of each other.

As a consequence, every lookup identifier referenced by the columns of a frame MUST still hold the intended value after all of the frame's entries have been applied. In other words: **the working set of a single frame must fit in the lookup tables.** A producer MUST NOT overwrite, within one frame, an identifier that the same frame's columns still refer to.

If a producer cannot satisfy this, it MUST end the frame and start a new one. If a single row cannot be encoded even in an otherwise empty frame, the producer MUST throw an error – the configured lookup table sizes are too small for these results.

!!! warning

    A consumer cannot detect a violation of this rule. It will silently decode the affected terms to the wrong values. This is a producer-side obligation.

!!! note

    A simple way to implement this on the producer's side is to track which identifiers the current frame has touched (assigned or referenced), and to end the frame before a row could touch an identifier that is already in that set. If the lookup uses an LRU eviction policy, everything the frame has touched sits at the recent end, so the frame stays safe exactly as long as it has not touched every identifier of the table.

### Columns

A column stores the cells of one variable across all `row_count` rows of a frame, in row order. A cell is either a **bound** RDF term or **unbound**.

There are four column types, each in its own repeated field of `SparqlResultsFrame`:

| Field                  | Message type                                            | Holds                      |
| ---------------------- | ------------------------------------------------------- | -------------------------- |
| `iri_columns` (7)      | [`SparqlIriColumn`](reference.md#sparqliricolumn)         | IRIs only                  |
| `bnode_columns` (8)    | [`SparqlBnodeColumn`](reference.md#sparqlbnodecolumn)     | blank nodes only           |
| `literal_columns` (9)  | [`SparqlLiteralColumn`](reference.md#sparqlliteralcolumn) | literals only              |
| `poly_columns` (10)    | [`SparqlPolyColumn`](reference.md#sparqlpolycolumn)       | RDF terms of any type      |

Producers SHOULD use a monomorphic column (IRI, blank node, or literal) whenever all the values of a variable in a frame are of the same type, and use a polymorphic column only for variables whose values mix term types.

Every column of a frame contains:

- a list of **run values** – the values of the column, with each run of consecutive equal values stored exactly once, and unbound cells not stored at all;
- the `layouts` list – a description of where the sequence of cells deviates from "each run value occupies exactly one cell", see [sequence layout](#sequence-layout).

A column whose cells are all unbound in a frame is encoded as an empty message, of any of the four types. A column MUST decode to at most `row_count` cells; shorter columns are padded with unbound cells.

!!! note

    Two producers may encode the same result set into different bytes – the choice of column type for an all-unbound variable is one of several places where this happens. Jelly-SPARQL streams are not byte-level canonical, and implementations should compare decoded result sets rather than bytes.

#### Sequence layout

The `layouts` field of every column type is a flat list of **exceptions** to the rule "each run value occupies exactly one cell". When every cell of a column is bound and no value repeats in consecutive rows, `layouts` is empty.

Each exception is one varint token, optionally followed by one extension varint:

```
token = (skip << 5) | (kind << 4) | len_code
```

- `skip` – bits 5 and up. The number of run values that occupy exactly one cell each since the previous exception, or since the start of the column.
- `kind` – bit 4. `0` = repeat run, `1` = unbound run.
- `len_code` – bits 0–3. If its value is 0–14, the run length code `len` is equal to it. If its value is 15, then `len` is 15 plus the value of the next varint in the `layouts` list (the *extension varint*).

The run lengths are offset, because a repeat run of fewer than 2 cells and an unbound run of fewer than 1 cell make no sense:

- **repeat run** – the run value at the current position occupies `len + 2` cells;
- **unbound run** – there are `len + 1` consecutive unbound cells.

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

A frame is corrupt, and the consumer SHOULD throw an error, if any of the following holds for any of its columns:

- `i + skip > m` – a `skip` runs past the last run value;
- a repeat run starts when `i == m` – the run points past the last run value;
- `len_code` is 15 and the token is not followed by an extension varint;
- the column decodes to more than `row_count` cells.

Producers MUST merge adjacent runs. In particular, a producer MUST NOT emit two unbound runs separated by `skip == 0`. Producers SHOULD omit trailing unbound runs and rely on the padding rule.

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

- `name_ids` (1) – the name identifiers of the run values, in row order. **The length of this list is the number of run values in the column.**
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

The consumer SHOULD throw an error if the length of `prefix_ids` is none of the three allowed values.

!!! note "Difference from Jelly-RDF"

    In Jelly-RDF, the `prefix_id` and `name_id` inference state runs across the whole stream, in a strict order of rows and terms within rows. In Jelly-SPARQL it is **per column, per frame**. That is what lets a consumer decode the columns of a frame in any order, or in parallel, given only the lookup tables.

    The price is that a producer has to state the prefix and name identifiers again at the start of every frame, even when the value is the same as in the previous frame.

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

    The same column in a frame where every IRI is in the `https://a.org/` namespace would carry `prefix_ids: [1]` instead – one entry for the whole column.

#### Blank node columns

A blank node column is a [`SparqlBnodeColumn`](reference.md#sparqlbnodecolumn) message with the following fields:

- `values` (1) – the run values, that is, the blank node labels, in row order.
- `layouts` (2) – the [sequence layout](#sequence-layout).

Blank node labels are represented as plain UTF-8 strings, and are not compressed with any lookup table.

Blank node labels are **scoped to the result set**, that is, to the entire result stream. Two cells anywhere in one stream that carry the same label MUST be interpreted as referring to the same blank node, regardless of which frame they are in, and regardless of whether the [stream options were repeated](#repeating-the-stream-options) between them. Two cells carrying different labels MUST be interpreted as referring to different blank nodes.

!!! note "Difference from Jelly-RDF"

    Jelly-RDF deliberately leaves the scope of blank node labels open, because the semantics of its stream frames are not fixed. Jelly-SPARQL fixes it, because a Jelly-SPARQL stream always describes exactly one result set, and both the [SPARQL Query Results XML](https://www.w3.org/TR/rdf-sparql-XMLres/#bnodes) and [JSON](https://www.w3.org/TR/sparql11-results-json/) formats scope blank node labels to the result set.

#### Literal columns

A literal column is a [`SparqlLiteralColumn`](reference.md#sparqlliteralcolumn) message. It has two mutually exclusive forms.

**The lexical form.** A column in which every value has the same datatype – including a column of simple literals, whose datatype is `xsd:string` – states that datatype once and lists only the lexical forms:

- `lex_values` (3) – the lexical forms of the run values, in row order.
- `datatype` (4) – the datatype shared by every run value: a 1-based reference to an entry in the [datatype lookup](#prefix-name-and-datatype-lookup-entries), or 0 for simple literals (that is, literals with the datatype `http://www.w3.org/2001/XMLSchema#string`).
- `values` (1) MUST be empty.

A simple literal does not need an `xsd:string` entry in the datatype lookup: the producer states no datatype at all, and the consumer produces the same term, because a simple literal and an `xsd:string` literal are the same thing. Both encodings are legal and produce the same result.

**The full form.** A column holding language-tagged literals, or literals of more than one datatype, uses [`RdfLiteral`](serialization.md#literals) messages:

- `values` (1) – the run values, in row order, each an `RdfLiteral` message encoded exactly as in [Jelly-RDF](serialization.md#literals).
- `lex_values` (3) MUST be empty and `datatype` (4) MUST NOT be set.

Both forms use `layouts` (2) for the [sequence layout](#sequence-layout).

A column with no run values at all (that is, a column that is unbound in every row of the frame) is an empty message, and is read as the full form.

The consumer SHOULD throw an error if a literal column has both `values` and `lex_values` set, or if it sets `datatype` while `lex_values` is empty.

!!! note

    The lexical form drops the length-delimited sub-message and the datatype reference of every value. It also lets a reader keep the column in a plain string array instead of allocating one object per value. This is the common case in SPARQL results – think of a `?label` or `?count` column.

!!! note "Known limitation"

    A single language-tagged literal forces the whole column into the full form, even when every value in the column carries the same language tag. A per-column language tag, analogous to `datatype`, is [planned for a future version](#planned-for-future-versions).

#### Polymorphic columns

A polymorphic column is a [`SparqlPolyColumn`](reference.md#sparqlpolycolumn) message with the following fields:

- `values` (1) – the run values, in row order, each a [`SparqlTerm`](reference.md#sparqlterm) message.
- `layouts` (2) – the [sequence layout](#sequence-layout).

A `SparqlTerm` message has a `term` oneof with three fields, of which **exactly one** MUST be set:

- `iri` (1) – an IRI, as an `RdfIri` message.
- `bnode` (2) – a blank node label, as a string.
- `literal` (3) – a literal, as an `RdfLiteral` message.

The consumer SHOULD throw an error if none of the fields of the `term` oneof is set.

The `RdfIri` inference state (see [IRI columns](#iri-columns)) is shared by all the IRIs in one polymorphic column: it advances through the run values in order, skipping the values that are not IRIs. Like in the monomorphic columns, the state resets at the start of every column in every frame.

Producers SHOULD use polymorphic columns only for variables whose values in a frame actually mix term types. A variable may be held in a monomorphic column in one frame and in a polymorphic one in another – that is what [restating the header](#restating-the-header) is for.

### RDF terms

The RDF terms that can be bound to a variable in Jelly-SPARQL are IRIs, blank nodes, and literals. They are encoded exactly as in [Jelly-RDF](serialization.md#rdf-terms-and-graph-nodes), with the differences in the scope of the IRI inference state described above.

Two kinds of value that Jelly-RDF can encode are not representable in a Jelly-SPARQL result stream, and no message in `sparql.proto` has a field for them:

- the default graph node ([`RdfDefaultGraph`](reference.md#rdfdefaultgraph)) – it is not an RDF term and cannot be bound to a variable;
- RDF-star quoted triples / RDF 1.2 triple terms ([`RdfTriple`](reference.md#rdftriple)).

A producer that is handed a solution binding a variable to a triple term MUST throw an error, unless it applies an implementation-defined fallback encoding, which it MUST document.

!!! note "Known limitation"

    RDF 1.2 literals with a base direction cannot be represented either. Support for both triple terms and base directions is [planned for a future version](#planned-for-future-versions).

### Frames with no rows

A frame MAY have `row_count` equal to 0. This is the case for a result set with no solutions at all, which is still a valid result set and MUST be serialized as at least one frame carrying the stream options and the header.

A frame with `row_count` equal to 0 SHOULD omit its columns entirely, rather than carrying one empty column message per variable.

!!! note

    This is why the [column count rule](#column-indices) allows a frame to have either exactly *N* columns or none at all: an empty frame of a 20-variable result set would otherwise waste 40 bytes stating twenty times that it has nothing to say.

## Framing

Protobuf messages [are not self-delimiting](https://protobuf.dev/programming-guides/techniques/#streaming), so a byte stream holding more than one message needs a delimiter between them. Jelly-SPARQL uses the same convention as [Jelly-RDF](serialization.md#delimited-variant-of-jelly): a Protobuf varint holding the length of the message in bytes, prepended before it.

A byte stream in the **delimited variant** consists of a series of delimited `SparqlResultsFrame` messages.

A Jelly-SPARQL stream stored in a file, or carried in an HTTP message body, with the `application/x-jelly-sparql` [media type](#internet-media-type-and-file-extension) MUST use the delimited variant. This holds even when the stream consists of a single frame – there is no non-delimited variant of the media type, and consumers do not have to guess which of the two they are reading.

Transports that provide their own message framing (for example gRPC, MQTT, or Kafka) carry one bare, non-delimited `SparqlResultsFrame` message per transport message.

## Internet media type and file extension

The RECOMMENDED media type for Jelly-SPARQL is `application/x-jelly-sparql`. The RECOMMENDED file extension is `.jellys`.

The same media type is used for solution sequences and for boolean results – the two are distinguished by the contents of the first frame, not by the media type.

The bytes MUST be in the [delimited variant](#framing).

### Use with the SPARQL 1.1 Protocol

A service implementing the [SPARQL 1.1 Protocol](https://www.w3.org/TR/sparql11-protocol/) MAY offer Jelly-SPARQL as a query results format. The following applies:

- Jelly-SPARQL is a results format for `SELECT` and `ASK` queries. `CONSTRUCT` and `DESCRIBE` queries return RDF graphs, and should use [Jelly-RDF](serialization.md) (`application/x-jelly-rdf`) instead.
- Clients that can read Jelly-SPARQL SHOULD list `application/x-jelly-sparql` in the `Accept` header of the query request, and SHOULD also list a W3C-defined results format as a fallback with a lower q-value.
- Because Jelly-SPARQL is not one of the results formats defined by W3C, a service SHOULD return it only when the client named it explicitly. A service SHOULD NOT select `application/x-jelly-sparql` for a request whose `Accept` header does not name it – for example `Accept: */*`.
- A service that streams the response SHOULD flush the connection after each frame, so that the client can start processing solutions before the query has finished.
- A service that fails part-way through a query SHOULD write a [trailer](#stream-trailer) with a non-empty `error` before closing the connection. The HTTP status line has already been sent by then, so the trailer is the only place left to say what went wrong.

!!! note

    The last point is the main practical reason for the trailer. A `200 OK` response whose body stops early looks exactly like a complete, shorter result set.

## Streaming over the network

Jelly-SPARQL streams can be transmitted over any transport that can carry an ordered sequence of messages – an HTTP response body, a WebSocket connection, or a message broker such as Kafka or MQTT. See [framing](#framing) for how the frames are delimited in each case.

The [Jelly gRPC streaming protocol](streaming.md) does not cover Jelly-SPARQL: its service definition only carries `RdfStreamFrame` messages. There are no plans to extend it to SPARQL results at the moment.

## Security considerations

*This section is not part of the specification.*

The same security considerations apply to Jelly-SPARQL as to [Jelly-RDF](serialization.md#security-considerations), in particular those about Protocol Buffers, [overly large lookup tables](#overly-large-lookup-tables), and invalid lookup entry identifiers. The considerations about infinite recursion of RDF-star quoted triples do not apply, because Jelly-SPARQL has no recursive messages.

### Overly large lookup tables

For untrusted input, consumers must always validate that the requested sizes of the name, prefix, and datatype lookup tables are not overly large and are supported by the consumer. A malicious producer could attempt to exhaust the memory of the consumer by requesting a lookup table of several gigabytes or more. This would constitute a denial-of-service vector. See also the [Jelly-RDF specification](serialization.md#overly-large-lookup-tables).

The recommended mitigation is the same as in Jelly-RDF: each implementation defines a maximum allowed lookup size and checks the requested size against it, rejecting the stream if it is larger. The limit should be configurable, so that a user who trusts the producer can raise it.

The sizes RECOMMENDED as defaults for that limit are 16384 names, 4096 prefixes, and 256 datatypes. They are larger than the Jelly-RDF defaults because a frame of SPARQL results touches more distinct terms than a frame of RDF statements does, and because [the working set of a frame must fit in the tables](#the-working-set-of-a-frame).

!!! info

    These are limits on what a consumer *accepts*, not on what a producer *should use*. A producer has no reason to ask for tables this large in the first place – the Jelly-JVM writer defaults to 8192 names, 1024 prefixes, and 64 datatypes.

### Overly large row counts

The `row_count` field of a frame is not bounded by the size of the frame: a frame of a few bytes can declare a row count in the tens of millions. A consumer that allocates a per-row buffer of `row_count` elements before decoding the columns would be a denial-of-service vector.

The recommended mitigation is to grow the decoding buffers to the size actually needed as the columns are decoded, and to validate `row_count` against a configurable limit before allocating anything.

### Column layouts

The layout tokens of a column drive how many cells the consumer writes. A consumer must validate every token against the number of run values it actually has and against `row_count`, as described in [sequence layout](#sequence-layout), before writing anything. In particular, the extension varint of an escaped length token is attacker-controlled and must not be trusted to fit into the remaining space of the row buffer.

### Query results content

Jelly-SPARQL is a general serialization format for SPARQL query results, and as such may be used to transmit malicious or misleading content. Please refer to the [security considerations of the SPARQL 1.1 Query Results JSON Format](https://www.w3.org/TR/sparql11-results-json/) and to the [RDF 1.1 Turtle W3C Recommendation](https://www.w3.org/TR/turtle/#sec-mediaReg).

## Implementations

*This section is not part of the specification.*

The following implementations of Jelly-SPARQL are available:

- [Jelly-JVM implementation]({{ jvm_link() }}) *(experimental)*
    - Implemented actors: producer, consumer
    - Supported libraries: [Apache Jena](https://jena.apache.org/), [RDF4J](https://rdf4j.org/)

## See also

- [Jelly-RDF serialization format specification](serialization.md)
- [Jelly-Patch format specification](patch.md)
- [Jelly Protobuf reference](reference.md)
