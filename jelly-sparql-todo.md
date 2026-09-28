# Jelly-SPARQL: changes needed in the proto and the implementations

Temporary tracking doc for the draft spec in [`docs/specification/sparql.md`](docs/specification/sparql.md). Delete once the work below is done.

The spec is currently **ahead of both `sparql.proto` and Jelly-JVM**. Everything in sections 1 and 2 has to land before the spec text is true.

---

## 1. `jelly-protobuf`

### 1.1 `proto/sparql.proto` – new messages and fields ✅ done

**New message.** The [stream trailer](docs/specification/sparql.md#stream-trailer):

```protobuf
// End-of-stream marker, saying whether the result set is complete.
//
// A frame carrying a trailer must not be followed by any frame that does not
// carry the stream options. Producers should write a trailer in the last frame
// they write: without one, a reader cannot tell a complete result set from a
// truncated one.
message SparqlResultsTrailer {
  // Empty (the default) means the result set is complete.
  // A non-empty value is a human-readable explanation of why the producer
  // could not produce the complete result.
  string error = 1;
}
```

**New field** in `SparqlResultsFrame` (12, 13 and 14 are all free):

```protobuf
  // End-of-stream marker. See SparqlResultsTrailer.
  SparqlResultsTrailer trailer = 12;
```

### 1.2 `proto/sparql.proto` – comment changes ✅ done

| Where | Current comment says | Must now say |
| --- | --- | --- |
| `SparqlResultsFrame.options` | "Must be set in the first frame of the stream and unset in all subsequent frames" | May be set again in a later frame. Doing so resets the lookup tables (numbering restarts at 1) and drops the header, which the same frame must restate with the same variables. Intended only for concatenating files. |
| `SparqlResultsFrame.row_count` | "Number of rows (solutions) in this frame (required)" | also: must not exceed 2^27 − 1, the largest number of cells the layout encoding can address |
| `SparqlResultsFrame.variables` | "An empty variables list **in the first frame of the stream** declares a zero-variable result set" | "in a frame that carries the options" (so the rule still works after an options reset) |
| `SparqlResultsFrame` column fields | "Every frame must contain the same number of columns of each type, as established by the most recent header" | A frame must contain either exactly the columns the header establishes, or no columns at all. The no-columns form is only valid when `row_count` is 0 (or the result set has no variables), and is the recommended encoding for an empty frame. |
| `SparqlResultsFrame.metadata` | "implementations may use it in any way they see fit" | add the well-known `link` key: UTF-8, zero or more IRIs separated by LF, describing the result set (not the frame). Values of well-known keys must be valid UTF-8; all other keys stay arbitrary bytes. |
| `SparqlResultsFrame.ask_result` | "It must be set in the first frame … no further result content may follow" | note that `metadata` and `trailer` are not result content and may be set on that frame |

The `SparqlResultsOptions` table size comments need **no** change: the `>= 128` floor stays, and there are deliberately no maxima in the format – see 2.5.

### 1.3 `proto/rdf2.proto`

Nothing to do – the single `RdfLookupEntryPacked` message is what the spec describes, and it is on `main` now.

### 1.4 Conformance test suite (`test/sparql/`) ✅ done (uncommitted)

195 tests: 167 from Jelly (91 positive, 76 negative) and 28 to Jelly (22 positive, 6 negative), in four categories: `select_rdf_1_1`, `ask`, `select_rdf_1_2_basic`, `select_rdf_1_2`. New vocabulary terms: `jellyt:TestSparql`, `jellyt:TestSparqlFromJelly`, `jellyt:TestSparqlToJelly`, `jellyt:requirementRdf12Basic`, `jellyt:requirementRdf12`.

All files are written by `test/sparql/generator/generate.py` (plain Python, no dependencies; `--check` verifies the files are up to date). It checks each case against a reference decoder and encoder written from the spec. Every negative case must fail for its intended reason.

Consumer rules that produce undefined results when ignored are now MUST in the spec: corrupt layouts, literal-column form conflicts, an empty polymorphic term, the `prefix_ids` length, column indices that are not a permutation, and a restated header with other variables. Unknown `rdf_version` values are now an explicit MUST as well. Tests of rules that stay SHOULD (15 of them) carry `mf:notable jellyt:featureShouldLevel`.

Run against Jelly-JVM (Jena), with an untracked runner `integration-tests/.../sparql/SparqlConformanceSpec.scala`: 189 of 195 pass. The 6 failures are negative tests the JVM accepts:

- MUST-level, to fix in the JVM:
    - `from_jelly/select_rdf_1_1/neg_002` – a truncated last frame is silently accepted.
    - `from_jelly/select_rdf_1_1/neg_010` – unknown `rdf_version` value 4 is not rejected.
    - `from_jelly/select_rdf_1_2_basic/neg_007`, `neg_008` – unknown base direction values (3, 7) are not rejected.
- SHOULD-level:
    - `from_jelly/select_rdf_1_1/neg_003` – version tag 0 is not rejected.
    - `from_jelly/ask/neg_004` – a trailer-only frame after the ASK frame is accepted on purpose (see 2.1), but the spec says consumers SHOULD throw on any frame after it. Either the spec or the JVM should change.

---

## 2. `jelly-jvm`

### 2.1 `core-sparql` – trailer support (new feature) ✅ done

Done as `SparqlEncoder.endStream()` / `endStream(String error)` (end the stream, encoder unusable afterwards; `endStream(error)` also works after a failed `appendRow`, dropping the half-written frame's content), `SparqlResultsHandler.handleTrailer(String)` (default no-op), and `askResultFrame` now includes an empty trailer. The decoder also now rejects any result content after an ASK result, but accepts a trailer-only frame there.

- `SparqlEncoder` – a way to attach a trailer to the frame being finished. Something like `endFrame(String error)` alongside the current `endFrame()`, or a `setTrailer` called before `endFrame`.
- `SparqlResultsHandler` – a new callback, e.g. `handleTrailer(String error)`, with a default no-op so existing handlers keep compiling.
- `SparqlDecoderImpl` – read `frame.getTrailer()`, push it to the handler, and reject a frame that follows a trailer unless it carries the options.
- The decoder cannot know where the stream ends, so "no trailer was seen" is the **reader's** job, not the decoder's – see 2.4.

### 2.2 `core-sparql` – `SparqlDecoderImpl` ✅ done

| What | Where | Change |
| --- | --- | --- |
| Options reset | `handleOptions` | Currently `if (currentOptions == null) currentOptions = options;` – a repeat is validated and then silently dropped. Must now: adopt the new options, empty the name/prefix/datatype lookups (recreating them if the sizes changed), and mark the header as no longer in effect so the frame is required to restate it. |
| Zero-variable detection | `ingestFrame` | The condition `variableNames == null && frame.getOptions() != null && !askResultReceived` breaks after a reset, when `variableNames` is no longer null. Key it off "this frame carries the options" plus "the header is not in effect". |
| Column count | `ingestFrame` | `totalColumns != variableNames.length` must now also accept `totalColumns == 0` when `rows == 0` (or when there are no variables). |
| Row count bound | `ingestFrame` | Currently only rejects `rows < 0` (over 2^31). Must reject anything above 2^27 − 1. |
| Header after reset | `handleHeader` | The "restated header must declare the same variables" check already does the right thing – confirm it still fires when the header was dropped by a reset rather than restated normally. |

### 2.3 `core-sparql` – `SparqlEncoderImpl` ✅ done

- `endFrame` – when `rowCount == 0`, omit the column messages entirely instead of emitting one empty message per variable. The four per-type loops currently always append.
- Trailer plumbing (see 2.1).

### 2.4 `core-sparql` – lookup table size limits ✅ done

The spec does **not** set maxima on the lookup table sizes, matching Jelly-RDF, which has only a minimum (8 names) and leaves the ceiling to implementations via the security considerations. Jelly-SPARQL's minimum is 128 names; the recommended *default* ceiling a consumer accepts is 16384 names / 4096 prefixes / 256 datatypes, and it should be configurable.

`JellySparqlOptions` needs two changes to match:

- `checkCompatibility` currently does `Math.min(supportedOptions.getMaxNameTableSize(), MAX_NAME_TABLE_SIZE)` for each table, so `MAX_*` is a hard ceiling that a caller cannot raise however generous its supported options are. Drop the `Math.min` and compare against the supported options alone, as `JellyOptions.checkCompatibility` does on the RDF side.
- `DEFAULT_SUPPORTED_OPTIONS` is currently `BIG` (8192 / 1024 / 64), i.e. the reader accepts exactly what the writer emits by default. Jelly-RDF deliberately separates the two – `JellyOptions.DEFAULT_SUPPORTED_OPTIONS` is 4096 / 1024 / 256 while the `BIG_*` writer preset is 4000 / 150 / 32. Set the Jelly-SPARQL reader default to the recommended 16384 / 4096 / 256 (the current `MAX_*` values) and leave `BIG` as the writer preset.

A reader whose acceptance limit equals the writer preset rejects any stream written with slightly more generous options, which is the bug the current setup has – note `BIG`'s 64 datatypes in particular.

### 2.5 `jena-sparql` and `rdf4j-sparql` ✅ done

- Writers always end with `endStream()`; when the rows end exactly on a frame boundary, that adds a tiny trailer-only frame. Jena writes the error trailer when the `RowSet` throws. RDF4J never tells a writer about failures, so it got a public `AbstractJellySparqlWriter.endQueryResultWithError(String)` that callers must use themselves.
- Readers throw after handing out all rows received before the error. A missing trailer is accepted by default, and an opt-in strict mode rejects it: Jena `SYMBOL_REQUIRE_TRAILER`, RDF4J `JellySparqlParserSettings.REQUIRE_TRAILER`. No logging.
- Framing: the non-delimited option stays, and its docs now say the media type is delimited-only.
- `link` metadata: done for RDF4J only (`handleLinks` on both the writer and the parser). Jena has no API for links: its readers skip them and its writers never write them. Core got `JellySparqlMetadata`, which encodes and decodes `link` and adds metadata to a frame the encoder already built (the encoder itself keeps no metadata state).

- **Write a trailer.** `RowSetWriterJelly.write` and `AbstractJellySparqlWriter` should set an empty trailer on the last frame of a successful write, and – if iterating the row set throws – write a trailer carrying the error message before rethrowing. That is the whole point of the feature.
- **Read a trailer.** `RowSetReaderJelly` and `AbstractJellySparqlParser` should throw when they see a non-empty `error`, and decide what to do when the stream ends with no trailer at all. Probably: do not throw (too many producers will not write one yet), but expose it somehow. Jena's `RowSet` has no slot for this, so it may end up being a log line – worth thinking about.
- **Framing.** The spec now says `application/x-jelly-sparql` is delimited-only. `RowSetWriterJelly.Options.delimited` defaults to `true`, which is right; the question is whether the `false` path should stay reachable for the registered Jena `Lang` / RDF4J format at all. Suggestion: keep the option for callers embedding a single frame somewhere else, but never use it behind the media type. `IoUtils.autodetectDelimiting` on the read side can stay as leniency.
- **`link` metadata.** Optional, low priority: map the well-known `link` key to whatever Jena and RDF4J expose for `head.link`.

### 2.6 `core-sparql` – per-column language tag ✅ done (JVM side)

Encoder: no new fields in `ColumnState` – `columnDatatype` got one more state, "every literal so far has the same tag", and the tag itself is kept in the column's `PolyBuffers` side object (one new field there). Matching values store only their lexical form, so the strings buffer is directly `lex_values`. Tags are compared with `equals`. The encoder never writes a `datatype` for language-tagged strings. Decoder: new `LangLiteralReader`, and it rejects `langtag` without `lex_values` and `langtag` together with `datatype`. A new `lit-lang-one` preset in `SparqlDataGen` puts the single-language case into the fuzz tests. The conformance test bullet below is still open (1.4).

The spec and the proto now have `SparqlLiteralColumn.langtag` (5), see 3.

- `SparqlEncoderImpl` – put a literal column in the lexical form when every run value is a language-tagged string with the same tag (compared as a plain string, no case folding). Never write `datatype` pointing at `rdf:langString`.
- `SparqlDecoderImpl` – when `lex_values` is non-empty and `langtag` is set, build language-tagged literals. Reject `langtag` with empty `lex_values`, and `langtag` together with `datatype`.
- Conformance tests (1.4) should cover a single-language column, a column mixing two tags (full form), and a column mixing a tagged and an untagged literal (full form).

### 2.7 RDF 1.2 terms

The spec and the proto now support RDF 1.2, see 3. New in `rdf2.proto`: `RdfVersion`, `RdfBaseDirection`, `RdfLiteral2`, `RdfTripleTerm`. New fields: `SparqlResultsOptions.rdf_version` (5), `SparqlTerm.triple_term` (4), `SparqlLiteralColumn.direction` (6). `SparqlTerm.literal` and `SparqlLiteralColumn.values` are now `RdfLiteral2` (wire-compatible with `RdfLiteral`).

- `JellySparqlOptions` – expose `rdf_version`, and check it in `checkCompatibility` against what the reader supports.
- `SparqlEncoderImpl` – write base directions (both in `RdfLiteral2` and in the lexical-form `direction`) and triple terms (poly columns only). The IRIs inside a triple term go through the column's `name_id` inference state in subject, predicate, object order. Throw on a term the declared version doesn't allow.
- `SparqlDecoderImpl` – read both. Reject: `direction` without `langtag`, unknown `direction` values, a triple term with a missing position, and any term the declared version doesn't allow.
- `jena-sparql` / `rdf4j-sparql` – map to the RDF 1.2 terms of each library (triple terms and literals with a base direction). Pick the writer's default `rdf_version` from what the library supports. Drop RDF4J's "no triple term support" declaration.
- Conformance tests (1.4) should cover each `rdf_version` value, `ltr` and `rtl` literals in both column forms, nested triple terms, IRI inference through a triple term, and negative cases for terms not allowed by the declared version.

---

## 3. Backlog – after 1.0

Nothing left: both items were moved into version 1.

- ~~**Per-column language tag.**~~ ✅ Moved into version 1: a `langtag` field (5) on `SparqlLiteralColumn`, mutually exclusive with `datatype`, used with `lex_values`. No version bump, since version 1 is still a draft. Spec and proto done; the JVM work is in 2.6.
- ~~**RDF 1.2 / SPARQL 1.2 terms.**~~ ✅ Moved into version 1. A new `RdfVersion` enum in the stream options (`1.1` / `1.2-basic` / `1.2`; unspecified means no version is announced, as in Turtle 1.2; a declared version is binding), `RdfLiteral2` with a base direction, and a typed `RdfTripleTerm` in `rdf2.proto`. Triple terms are only allowed in polymorphic columns. Spec and proto done; the JVM work is in 2.7.

---

## 4. Decisions taken (for the record)

| # | Question | Decision |
| --- | --- | --- |
| 1 | Which proto is authoritative | Single `RdfLookupEntryPacked`, merged to `main` |
| 2 | Versioning track | Independent of Jelly-RDF and Jelly-Patch |
| 3 | RDF 1.2 terms | In version 1: `rdf_version` enum in the options, `RdfLiteral2` and `RdfTripleTerm` in `rdf2.proto`, triple terms in poly columns only |
| 4 | Options repeated in later frames | Allowed |
| 5 | Zero-variable result sets | Layout unchanged; a repeated options message resets the lookups and the header, which must be restated. For concatenating files only |
| 6 | Lookup table bounds | Minimum 128 names is normative; **no** maxima in the format. Recommended default consumer limit (configurable): 16384 / 4096 / 256. Matches how Jelly-RDF handles it |
| 7 | Frame working-set rule | Unchanged – producer-side MUST, consumer cannot detect |
| 8 | Max `row_count` | 2^27 − 1 as the theoretical bound; frame byte size is the practical one |
| 9 | Per-column language tag | In version 1: `SparqlLiteralColumn.langtag` (5), mutually exclusive with `datatype` |
| 10 | Blank node scoping | Scoped to the whole stream; **not** reset by repeated options |
| 11 | Self-contained frames | A note, not a normative mode. `stream_name` keeps its Jelly-RDF meaning |
| 12 | Error signalling | Trailer with a single `error` string |
| 13 | `head.link` | Well-known `metadata` key `link`, UTF-8, IRIs separated by LF |
| 14 | Variable names | Producer-side SHOULD (unique, `VARNAME`); consumers need not check |
| 15 | gRPC | Skipped |
| 16 | Conformance test suite | Describe the planned layout in the spec – done |
| 17 | Media type / content negotiation | `application/x-jelly-sparql` + `.jellys` confirmed; content negotiation guidance written |
| 18 | `reserved` field numbers | No |
| 19 | Framing | Delimited only for the media type |
| 20 | Never-bound column type | No recommendation – streams are not byte-level canonical |
| 21 | Two `xsd:string` encodings | Both legal |
| 22 | Frames with no rows | May omit their columns |
