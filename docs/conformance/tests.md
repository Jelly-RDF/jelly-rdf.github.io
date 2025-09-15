# Protocol conformance — Tests

<style>table{table-layout:fixed;width:100%;} thead th:nth-child(1){width:110px;} thead th:nth-child(2){width:55%;} td,th{vertical-align:top;}</style>

> ### How to approach these tests
> This page lists **Jelly protocol conformance tests**. They are language-agnostic and are used by all Jelly implementations.
>
> Each test is defined in a manifest and includes: **Name**, **Description**, **Type** (`positive`/`negative`), **Category**, Data (`triples`/`quads`/`graphs`), **Input(s)** and **Expected**.
>
> **Finding the right tests:** filter by **Category** (e.g., `rdf_star`, `generalized`) and Data.
>
> **Validate results:**
> ```bash
> jelly-cli rdf validate --compare-ordered=true <your_output> <expected_output>
> ```
> *(see jelly-cli: https://github.com/Jelly-RDF/cli)*
>
> **Run locally (Python):**
> ```bash
> pytest tests/conformance_tests/test_rdf
> ```

**Manifests:** [test\rdf\from_jelly\manifest.ttl](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/manifest.ttl) · [test\rdf\to_jelly\manifest.ttl](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/manifest.ttl)

### Summary

- **All tests:** 187
- **From Jelly:** 110 (positive: 80, negative: 30)
- **To Jelly:** 77 (positive: 75, negative: 2)

## From Jelly (parse)

### Jump to category

- [graphs_rdf_1_1](#graphs-rdf-1-1)
- [graphs_rdf_star](#graphs-rdf-star)
- [quads_rdf_1_1](#quads-rdf-1-1)
- [quads_rdf_1_1_generalized](#quads-rdf-1-1-generalized)
- [quads_rdf_star](#quads-rdf-star)
- [quads_rdf_star_generalized](#quads-rdf-star-generalized)
- [triples_rdf_1_1](#triples-rdf-1-1)
- [triples_rdf_1_1_generalized](#triples-rdf-1-1-generalized)
- [triples_rdf_star](#triples-rdf-star)
- [triples_rdf_star_generalized](#triples-rdf-star-generalized)

### graphs_rdf_1_1

*11 positive, 0 negative*

#### Positive

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| pos_001 | Single frame, a set of quads with all possible graph labels: default graph, IRI, blank node. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_001/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_001/out_000.nq) | graphs_rdf_1_1 |
| pos_002 | Single frame. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_002/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_002/out_000.nq) | graphs_rdf_1_1 |
| pos_003 | Single frame. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_003/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_003/out_000.nq) | graphs_rdf_1_1 |
| pos_004 | Three (3) frames. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_004/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_004/out_000.nq) | graphs_rdf_1_1 |
| pos_005 | Three (3) frames. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_005/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_005/out_000.nq) | graphs_rdf_1_1 |
| pos_006 | Three (3) frames. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_007/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_007/out_000.nq) | graphs_rdf_1_1 |
| pos_007 | Three (3) frames. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_006/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_006/out_000.nq) | graphs_rdf_1_1 |
| pos_008 | Three (3) frames. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_008/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_008/out_000.nq) | graphs_rdf_1_1 |
| pos_009 | Two (2) frames, logical stream type set to LOGICAL_STREAM_TYPE_DATASETS. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_009/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_009/out_000.nq) | graphs_rdf_1_1 |
| pos_010 | Two (2) frames, logical stream type set to LOGICAL_STREAM_TYPE_NAMED_GRAPHS. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_010/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_010/out_000.nq) | graphs_rdf_1_1 |
| pos_011 | Two (2) frames, logical stream type set to LOGICAL_STREAM_TYPE_TIMESTAMPED_NAMED_GRAPHS. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_011/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_1_1/pos_011/out_000.nq) | graphs_rdf_1_1 |

### graphs_rdf_star

*7 positive, 3 negative*

#### Positive

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| pos_012 | Single frame with a set of quads contatining quoted triples in s/o or both in one IRI-labeled graph. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_star/pos_002/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_star/pos_002/out_000.nq) | graphs_rdf_star |
| pos_013 | Single frame with a set of quads contatining quoted triples in s/o or both in the default and BN-/IRI-labeled graphs. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_star/pos_003/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_star/pos_003/out_000.nq) | graphs_rdf_star |
| pos_014 | Single frame with a set of quads contatining quoted triples in s/o or both mixed with the same quoted triples as assertions in the respective default and BN-/IR… | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_star/pos_004/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_star/pos_004/out_000.nq) | graphs_rdf_star |
| pos_015 | Single frame with a set of quads with quoted triples in s/o or both mixed with the same quoted triples as assertions in the respective default and BN-/IRI-label… | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_star/pos_005/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_star/pos_005/out_000.nq) | graphs_rdf_star |
| pos_016 | Single frame with a set of quads with quoted triples nesting level 10 in s and o in the default and BN-/IRI-labeled graphs. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_star/pos_006/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_star/pos_006/out_000.nq) | graphs_rdf_star |
| pos_017 | Single frame with one simple quoted triple in the default graph. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_star/pos_001/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_star/pos_001/out_000.nq) | graphs_rdf_star |
| pos_018 | Three (3) frames with a set of quads with quoted triples. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_star/pos_007/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_star/pos_007/out_000.nq) | graphs_rdf_star |

#### Negative

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| neg_001 | Single frame, o_triple_term is missing a p_iri on level 5 and is repeated on the previous and next nesting levels. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_star/neg_003/in.jelly) | — | graphs_rdf_star |
| neg_002 | Single frame, o_triple_term is missing a s_iri. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_star/neg_001/in.jelly) | — | graphs_rdf_star |
| neg_003 | Single frame, s_triple_term is empty {}. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/graphs_rdf_star/neg_002/in.jelly) | — | graphs_rdf_star |

### quads_rdf_1_1

*8 positive, 5 negative*

#### Positive

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| pos_019 | Single frame, a few basic triples in the default graph. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/pos_001/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/pos_001/out_000.nq) | quads_rdf_1_1 |
| pos_020 | Single frame, a few quads with repeated s/p. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/pos_002/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/pos_002/out_000.nq) | quads_rdf_1_1 |
| pos_021 | Single frame, a mix of quads with repeated terms in s, p, o, g. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/pos_003/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/pos_003/out_000.nq) | quads_rdf_1_1 |
| pos_022 | Three (3) frames, a mix of quads with repeated terms across frames, including frame 2 starting from a fully repeated assertion. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/pos_004/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/pos_004/out_000.nq) | quads_rdf_1_1 |
| pos_023 | Three (3) frames, a mix of quads with repeated terms across frames, including frame 2 starting from a fully repeated assertion. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/pos_005/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/pos_005/out_000.nq) | quads_rdf_1_1 |
| pos_024 | Two (2) frames, logical stream type set to LOGICAL_STREAM_TYPE_DATASETS. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/pos_006/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/pos_006/out_000.nq) | quads_rdf_1_1 |
| pos_025 | Two (2) frames, logical stream type set to LOGICAL_STREAM_TYPE_NAMED_GRAPHS. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/pos_007/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/pos_007/out_000.nq) | quads_rdf_1_1 |
| pos_026 | Two (2) frames, logical stream type set to LOGICAL_STREAM_TYPE_TIMESTAMPED_NAMED_GRAPHS. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/pos_008/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/pos_008/out_000.nq) | quads_rdf_1_1 |

#### Negative

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| neg_004 | Single frame, a 'graph_end' row is in the stream. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/neg_003/in.jelly) | — | quads_rdf_1_1 |
| neg_005 | Single frame, a 'graph_start' row is in the stream. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/neg_002/in.jelly) | — | quads_rdf_1_1 |
| neg_006 | Single frame, a 'quad' row is in the stream. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/neg_001/in.jelly) | — | quads_rdf_1_1 |
| neg_007 | Single frame, a 'triple' row is in the stream. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/neg_001/in.jelly) | — | quads_rdf_1_1 |
| neg_008 | Single frame, no field in the graph oneof is set. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1/neg_002/in.jelly) | — | quads_rdf_1_1 |

### quads_rdf_1_1_generalized

*5 positive, 0 negative*

#### Positive

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| pos_027 | Single frame, a set of generalized RDF quads that features all possible terms in any position and repeated across one (1) frame. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1_generalized/pos_002/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1_generalized/pos_002/out_000.nq) | quads_rdf_1_1_generalized |
| pos_028 | Single frame, a set of generalized RDF quads that features all possible terms in any position. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1_generalized/pos_001/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1_generalized/pos_001/out_000.nq) | quads_rdf_1_1_generalized |
| pos_029 | Three (3) frames. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1_generalized/pos_005/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1_generalized/pos_005/out_000.nq) | quads_rdf_1_1_generalized |
| pos_030 | Three (3) frames. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1_generalized/pos_003/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1_generalized/pos_003/out_000.nq) | quads_rdf_1_1_generalized |
| pos_031 | Three (3) frames. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1_generalized/pos_004/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_1_1_generalized/pos_004/out_000.nq) | quads_rdf_1_1_generalized |

### quads_rdf_star

*7 positive, 3 negative*

#### Positive

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| pos_032 | Single frame with one simple quoted triple. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star/pos_001/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star/pos_001/out_000.nq) | quads_rdf_star |
| pos_033 | Single frame with quoted triples as s/o or both. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star/pos_002/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star/pos_002/out_000.nq) | quads_rdf_star |
| pos_034 | Single frame with quoted triples nested to level 10 in s and o. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star/pos_006/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star/pos_006/out_000.nq) | quads_rdf_star |
| pos_035 | Single frame with quoted triples of different formats and placements. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star/pos_003/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star/pos_003/out_000.nq) | quads_rdf_star |
| pos_036 | Single frame with quoted/asserted triples mix. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star/pos_004/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star/pos_004/out_000.nq) | quads_rdf_star |
| pos_037 | Single frame with quoted/asserted triples mix. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star/pos_005/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star/pos_005/out_000.nq) | quads_rdf_star |
| pos_038 | Three (3) frames with quoted/asserted triples mix across frames. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star/pos_007/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star/pos_007/out_000.nq) | quads_rdf_star |

#### Negative

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| neg_009 | Single frame, o_triple_term is fully empty {}. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star/neg_002/in.jelly) | — | quads_rdf_star |
| neg_010 | Single frame, o_triple_term is missing a s_bnode on the third nesting level, same s_bnode is repeated on the top nested levels. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star/neg_003/in.jelly) | — | quads_rdf_star |
| neg_011 | Single frame, s_triple_term is missing a p_iri. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star/neg_001/in.jelly) | — | quads_rdf_star |

### quads_rdf_star_generalized

*6 positive, 3 negative*

#### Positive

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| pos_039 | Single frame. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star_generalized/pos_005/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star_generalized/pos_005/out_000.nq) | quads_rdf_star_generalized |
| pos_040 | Single frame. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star_generalized/pos_003/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star_generalized/pos_003/out_000.nq) | quads_rdf_star_generalized |
| pos_041 | Single frame. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star_generalized/pos_004/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star_generalized/pos_004/out_000.nq) | quads_rdf_star_generalized |
| pos_042 | Single frame. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star_generalized/pos_001/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star_generalized/pos_001/out_000.nq) | quads_rdf_star_generalized |
| pos_043 | Single frame. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star_generalized/pos_002/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star_generalized/pos_002/out_000.nq) | quads_rdf_star_generalized |
| pos_044 | Three (3) frames. | positive | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star_generalized/pos_006/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star_generalized/pos_006/out_000.nq) | quads_rdf_star_generalized |

#### Negative

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| neg_012 | Single frame, a quad row only has an empty s_triple_term, quad before has three (3) proper s_triple_terms. | negative | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star_generalized/neg_002/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star_generalized/neg_002/out_000.nq) | quads_rdf_star_generalized |
| neg_013 | Single frame, o_triple_term is missing p_literal on the second nesting level, the same p_literal is used before and after in nested triples and in the quad row… | negative | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star_generalized/neg_003/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star_generalized/neg_003/out_000.nq) | quads_rdf_star_generalized |
| neg_014 | Single frame, s_triple_term is missing a p_literal on the first nesting level, p_literal on the deeper levels repeats. | negative | `quads` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star_generalized/neg_001/in.jelly) | [out_000.nq](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/quads_rdf_star_generalized/neg_001/out_000.nq) | quads_rdf_star_generalized |

### triples_rdf_1_1

*17 positive, 10 negative*

#### Positive

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| pos_045 | Four (4) frames, the first frame is empty. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_015/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_015/out_000.nt) | triples_rdf_1_1 |
| pos_046 | Four (4) frames, the last frame is empty. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_016/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_016/out_000.nt) | triples_rdf_1_1 |
| pos_047 | Four (4) frames, the second frame is empty. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_014/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_014/out_000.nt) | triples_rdf_1_1 |
| pos_048 | Single frame (non-delimited), a few basic triples. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_003/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_003/out_000.nt) | triples_rdf_1_1 |
| pos_049 | Single frame, a few basic triples with repeated terms, including multiple subsequent usages of the same term. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_007/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_007/out_000.nt) | triples_rdf_1_1 |
| pos_050 | Single frame, a few basic triples. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_002/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_002/out_000.nt) | triples_rdf_1_1 |
| pos_051 | Single frame, a few basic triples. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_005/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_005/out_000.nt) | triples_rdf_1_1 |
| pos_052 | Single frame, a few basic triples. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_004/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_004/out_000.nt) | triples_rdf_1_1 |
| pos_053 | Single frame, a few basic triples. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_001/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_001/out_000.nt) | triples_rdf_1_1 |
| pos_054 | Single frame, a few basic triples. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_006/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_006/out_000.nt) | triples_rdf_1_1 |
| pos_055 | Single frame, a triple with unusual but valid IRIs. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_011/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_011/out_000.nt) | triples_rdf_1_1 |
| pos_056 | Six (6) frames, the first three (3) frames are empty. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_017/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_017/out_000.nt) | triples_rdf_1_1 |
| pos_057 | Ten (10) frames, the first two (2) frames are empty, frames number 4, 5, and 6 are empty. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_018/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_018/out_000.nt) | triples_rdf_1_1 |
| pos_058 | Three (3) frames. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_009/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_009/out_000.nt) | triples_rdf_1_1 |
| pos_059 | Two (2) frames, a few basic triples with repeated terms. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_008/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_008/out_000.nt) | triples_rdf_1_1 |
| pos_060 | Two (2) frames, logical type = LOGICAL_STREAM_TYPE_GRAPHS. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_012/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_012/out_000.nt) | triples_rdf_1_1 |
| pos_061 | Two (2) frames, logical type = LOGICAL_STREAM_TYPE_SUBJECT_GRAPHS. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_013/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/pos_013/out_000.nt) | triples_rdf_1_1 |

#### Negative

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| neg_015 | Single frame, Literal has datatype index set to 0. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/neg_013/in.jelly) | — | triples_rdf_1_1 |
| neg_016 | Single frame, a quad row present in the PHYSICAL_STREAM_TYPE_TRIPLES stream. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/neg_010/in.jelly) | — | triples_rdf_1_1 |
| neg_017 | Single frame, invalid name table reference (0). | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/neg_008/in.jelly) | — | triples_rdf_1_1 |
| neg_018 | Single frame, invalid prefix table reference. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/neg_007/in.jelly) | — | triples_rdf_1_1 |
| neg_019 | Single frame, max_datatype_table_size set to 10000000. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/neg_003/in.jelly) | — | triples_rdf_1_1 |
| neg_020 | Single frame, max_name_table_size set to 10000000. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/neg_001/in.jelly) | — | triples_rdf_1_1 |
| neg_021 | Single frame, max_prefix_table_size set to 10000000. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/neg_002/in.jelly) | — | triples_rdf_1_1 |
| neg_022 | Single frame, prefix row is in the stream, when prefix lookup table is disabled. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/neg_005/in.jelly) | — | triples_rdf_1_1 |
| neg_023 | Single frame, prefix table entry with ID outside of max_prefix_table_size is in the stream. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/neg_006/in.jelly) | — | triples_rdf_1_1 |
| neg_024 | Single frame, repeated term (s_iri and o_iri) appears in the first statement row. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1/neg_012/in.jelly) | — | triples_rdf_1_1 |

### triples_rdf_1_1_generalized

*5 positive, 0 negative*

#### Positive

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| pos_062 | Four (4) frames, a set of generalized RDF triples that features all possible terms in any position and repeated across four (4) frames, reusing all lookup table… | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1_generalized/pos_005/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1_generalized/pos_005/out_000.nt) | triples_rdf_1_1_generalized |
| pos_063 | Single frame, a set of generalized RDF triples that features all possible terms in any position and repeated across one (1) frame. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1_generalized/pos_002/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1_generalized/pos_002/out_000.nt) | triples_rdf_1_1_generalized |
| pos_064 | Single frame, a set of generalized RDF triples that features all possible terms in any position. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1_generalized/pos_001/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1_generalized/pos_001/out_000.nt) | triples_rdf_1_1_generalized |
| pos_065 | Three (3) frames, a set of generalized RDF triples that features all possible terms in any position and repeated across three (3) frames. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1_generalized/pos_003/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1_generalized/pos_003/out_000.nt) | triples_rdf_1_1_generalized |
| pos_066 | Three (3) frames, a set of generalized RDF triples that features all possible terms in any position and repeated across three (3) frames. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1_generalized/pos_004/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_1_1_generalized/pos_004/out_000.nt) | triples_rdf_1_1_generalized |

### triples_rdf_star

*8 positive, 3 negative*

#### Positive

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| pos_067 | Single frame utilizing BNs/IRIs for subject and BNs/IRI/Literals for objects in quoted triples. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star/pos_008/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star/pos_008/out_000.nt) | triples_rdf_star |
| pos_068 | Single frame, a triple with nesting level 3, subject is repeated in quoted triples. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star/pos_006/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star/pos_006/out_000.nt) | triples_rdf_star |
| pos_069 | Single frame, one triple with a quoted triple as a subject. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star/pos_001/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star/pos_001/out_000.nt) | triples_rdf_star |
| pos_070 | Single frame, three triples showcasing a quoted triple as a subject/object/both. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star/pos_003/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star/pos_003/out_000.nt) | triples_rdf_star |
| pos_071 | Single frame, three triples showing a quoted triple as a subject/object/both. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star/pos_002/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star/pos_002/out_000.nt) | triples_rdf_star |
| pos_072 | Single frame, triples with nesting level 10 as subject/object. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star/pos_005/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star/pos_005/out_000.nt) | triples_rdf_star |
| pos_073 | Single frame, triples with nesting level 3 as subject/object. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star/pos_004/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star/pos_004/out_000.nt) | triples_rdf_star |
| pos_074 | Two (2) frames, triples have quoted triples in s and/or o. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star/pos_007/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star/pos_007/out_000.nt) | triples_rdf_star |

#### Negative

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| neg_025 | Single frame, missing a p_iri on the 7th (out of 10) nesting level of a s_triple_term. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star/neg_003/in.jelly) | — | triples_rdf_star |
| neg_026 | Single frame, o_triple_term is empty in a triple with repeated s/p. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star/neg_002/in.jelly) | — | triples_rdf_star |
| neg_027 | Single frame, o_triple_term is missing an o_literal. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star/neg_001/in.jelly) | — | triples_rdf_star |

### triples_rdf_star_generalized

*6 positive, 3 negative*

#### Positive

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| pos_075 | Single frame. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star_generalized/pos_004/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star_generalized/pos_004/out_000.nt) | triples_rdf_star_generalized |
| pos_076 | Single frame. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star_generalized/pos_003/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star_generalized/pos_003/out_000.nt) | triples_rdf_star_generalized |
| pos_077 | Single frame. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star_generalized/pos_005/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star_generalized/pos_005/out_000.nt) | triples_rdf_star_generalized |
| pos_078 | Single frame. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star_generalized/pos_002/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star_generalized/pos_002/out_000.nt) | triples_rdf_star_generalized |
| pos_079 | Single frame. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star_generalized/pos_001/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star_generalized/pos_001/out_000.nt) | triples_rdf_star_generalized |
| pos_080 | Three (3) frames. | positive | `triples` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star_generalized/pos_006/in.jelly) | [out_000.nt](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star_generalized/pos_006/out_000.nt) | triples_rdf_star_generalized |

#### Negative

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| neg_028 | Single frame, o_triple_term is missing an o_literal on the third nesting level. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star_generalized/neg_001/in.jelly) | — | triples_rdf_star_generalized |
| neg_029 | Single frame, p_triple_term is missing a s_literal used in quoted triples befoere and after and in the basic triple before quoted. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star_generalized/neg_003/in.jelly) | — | triples_rdf_star_generalized |
| neg_030 | Single frame, s_triple_term is empty {}. | negative | `—` | [in.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/from_jelly/triples_rdf_star_generalized/neg_002/in.jelly) | — | triples_rdf_star_generalized |

## To Jelly (serialize)

### Jump to category

- [graphs_rdf_1_1](#graphs-rdf-1-1)
- [graphs_rdf_star](#graphs-rdf-star)
- [quads_rdf_1_1](#quads-rdf-1-1)
- [quads_rdf_1_1_generalized](#quads-rdf-1-1-generalized)
- [quads_rdf_star](#quads-rdf-star)
- [quads_rdf_star_generalized](#quads-rdf-star-generalized)
- [triples_rdf_1_1](#triples-rdf-1-1)
- [triples_rdf_1_1_generalized](#triples-rdf-1-1-generalized)
- [triples_rdf_star](#triples-rdf-star)
- [triples_rdf_star_generalized](#triples-rdf-star-generalized)

### graphs_rdf_1_1

*9 positive, 0 negative*

#### Positive

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| pos_001 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_1_1/pos_007/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_1_1/pos_007/out.jelly) | graphs_rdf_1_1 |
| pos_002 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_1_1/pos_006/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_1_1/pos_006/out.jelly) | graphs_rdf_1_1 |
| pos_003 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=4, max-datatype-table-size=2. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_1_1/pos_008/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_1_1/pos_008/out.jelly) | graphs_rdf_1_1 |
| pos_004 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_1_1/pos_004/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_1_1/pos_004/out.jelly) | graphs_rdf_1_1 |
| pos_005 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=4, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_1_1/pos_005/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_1_1/pos_005/out.jelly) | graphs_rdf_1_1 |
| pos_006 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_1_1/pos_009/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_1_1/pos_009/out.jelly) | graphs_rdf_1_1 |
| pos_007 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_1_1/pos_002/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_1_1/pos_002/out.jelly) | graphs_rdf_1_1 |
| pos_008 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_1_1/pos_003/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_1_1/pos_003/out.jelly) | graphs_rdf_1_1 |
| pos_009 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_1_1/pos_001/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_1_1/pos_001/out.jelly) | graphs_rdf_1_1 |

### graphs_rdf_star

*7 positive, 0 negative*

#### Positive

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| pos_010 | Stream options are: generalized-statements=false, rdf-star=true, max-name-table-size=32, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_star/pos_006/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_star/pos_006/out.jelly) | graphs_rdf_star |
| pos_011 | Stream options are: generalized-statements=false, rdf-star=true, max-name-table-size=24, max-prefix-table-size=8, max-datatype-table-size=2. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_star/pos_007/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_star/pos_007/out.jelly) | graphs_rdf_star |
| pos_012 | Stream options are: generalized-statements=false, rdf-star=true, max-name-table-size=16, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_star/pos_004/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_star/pos_004/out.jelly) | graphs_rdf_star |
| pos_013 | Stream options are: generalized-statements=false, rdf-star=true, max-name-table-size=16, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_star/pos_005/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_star/pos_005/out.jelly) | graphs_rdf_star |
| pos_014 | Stream options are: generalized-statements=false, rdf-star=true, max-name-table-size=16, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_star/pos_003/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_star/pos_003/out.jelly) | graphs_rdf_star |
| pos_015 | Only IRIs as terms. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_star/pos_001/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_star/pos_001/out.jelly) | graphs_rdf_star |
| pos_016 | Only IRIs as terms. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_star/pos_002/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/graphs_rdf_star/pos_002/out.jelly) | graphs_rdf_star |

### quads_rdf_1_1

*6 positive, 0 negative*

#### Positive

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| pos_017 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1/pos_004/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1/pos_004/out.jelly) | quads_rdf_1_1 |
| pos_018 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=4, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1/pos_005/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1/pos_005/out.jelly) | quads_rdf_1_1 |
| pos_019 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1/pos_006/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1/pos_006/out.jelly) | quads_rdf_1_1 |
| pos_020 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1/pos_002/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1/pos_002/out.jelly) | quads_rdf_1_1 |
| pos_021 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1/pos_001/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1/pos_001/out.jelly) | quads_rdf_1_1 |
| pos_022 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1/pos_003/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1/pos_003/out.jelly) | quads_rdf_1_1 |

### quads_rdf_1_1_generalized

*5 positive, 0 negative*

#### Positive

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| pos_023 | Stream options are: generalized-statements=true, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1_generalized/pos_002/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1_generalized/pos_002/out.jelly) | quads_rdf_1_1_generalized |
| pos_024 | Stream options are: generalized-statements=true, rdf-star=false, max-name-table-size=8, max-prefix-table-size=4, max-datatype-table-size=2. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1_generalized/pos_005/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1_generalized/pos_005/out.jelly) | quads_rdf_1_1_generalized |
| pos_025 | Stream options are: generalized-statements=true, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1_generalized/pos_003/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1_generalized/pos_003/out.jelly) | quads_rdf_1_1_generalized |
| pos_026 | Stream options are: generalized-statements=true, rdf-star=false, max-name-table-size=8, max-prefix-table-size=4, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1_generalized/pos_004/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1_generalized/pos_004/out.jelly) | quads_rdf_1_1_generalized |
| pos_027 | Stream options are: generalized-statements=true, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1_generalized/pos_001/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_1_1_generalized/pos_001/out.jelly) | quads_rdf_1_1_generalized |

### quads_rdf_star

*7 positive, 0 negative*

#### Positive

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| pos_028 | Stream options are: generalized-statements=false, rdf-star=true, max-name-table-size=32, max-prefix-table-size=0, max-datatype-table-size=0. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star/pos_006/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star/pos_006/out.jelly) | quads_rdf_star |
| pos_029 | Altered input from pos_004. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star/pos_007/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star/pos_007/out.jelly) | quads_rdf_star |
| pos_030 | Stream options are: generalized-statements=false, rdf-star=true, max-name-table-size=16, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star/pos_005/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star/pos_005/out.jelly) | quads_rdf_star |
| pos_031 | Stream options are: generalized-statements=false, rdf-star=true, max-name-table-size=16, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star/pos_003/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star/pos_003/out.jelly) | quads_rdf_star |
| pos_032 | Stream options are: generalized-statements=false, rdf-star=true, max-name-table-size=16, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star/pos_004/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star/pos_004/out.jelly) | quads_rdf_star |
| pos_033 | Stream options are: generalized-statements=false, rdf-star=true, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=0. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star/pos_002/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star/pos_002/out.jelly) | quads_rdf_star |
| pos_034 | Only IRIs as terms. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star/pos_001/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star/pos_001/out.jelly) | quads_rdf_star |

### quads_rdf_star_generalized

*6 positive, 0 negative*

#### Positive

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| pos_035 | Stream options are: generalized-statements=true, rdf-star=true, max-name-table-size=16, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star_generalized/pos_001/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star_generalized/pos_001/out.jelly) | quads_rdf_star_generalized |
| pos_036 | Stream options are: generalized-statements=true, rdf-star=true, max-name-table-size=16, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star_generalized/pos_002/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star_generalized/pos_002/out.jelly) | quads_rdf_star_generalized |
| pos_037 | Stream options are: generalized-statements=true, rdf-star=true, max-name-table-size=16, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star_generalized/pos_005/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star_generalized/pos_005/out.jelly) | quads_rdf_star_generalized |
| pos_038 | Stream options are: generalized-statements=true, rdf-star=true, max-name-table-size=16, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star_generalized/pos_004/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star_generalized/pos_004/out.jelly) | quads_rdf_star_generalized |
| pos_039 | Stream options are: generalized-statements=true, rdf-star=true, max-name-table-size=16, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star_generalized/pos_003/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star_generalized/pos_003/out.jelly) | quads_rdf_star_generalized |
| pos_040 | Stream options are: generalized-statements=true, rdf-star=true, max-name-table-size=20, max-prefix-table-size=6, max-datatype-table-size=4, rows-per-frame=50. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star_generalized/pos_006/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/quads_rdf_star_generalized/pos_006/out.jelly) | quads_rdf_star_generalized |

### triples_rdf_1_1

*16 positive, 2 negative*

#### Positive

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| pos_041 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_013/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_013/out.jelly) | triples_rdf_1_1 |
| pos_042 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=0. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_001/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_001/out.jelly) | triples_rdf_1_1 |
| pos_043 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_011/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_011/out.jelly) | triples_rdf_1_1 |
| pos_044 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=0. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_016/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_016/out.jelly) | triples_rdf_1_1 |
| pos_045 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_009/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_009/out.jelly) | triples_rdf_1_1 |
| pos_046 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=0. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_008/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_008/out.jelly) | triples_rdf_1_1 |
| pos_047 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_012/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_012/out.jelly) | triples_rdf_1_1 |
| pos_048 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=0. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_014/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_014/out.jelly) | triples_rdf_1_1 |
| pos_049 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=0. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_015/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_015/out.jelly) | triples_rdf_1_1 |
| pos_050 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=0. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_006/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_006/out.jelly) | triples_rdf_1_1 |
| pos_051 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=0. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_005/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_005/out.jelly) | triples_rdf_1_1 |
| pos_052 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=0. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_004/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_004/out.jelly) | triples_rdf_1_1 |
| pos_053 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=0. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_002/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_002/out.jelly) | triples_rdf_1_1 |
| pos_054 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_003/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_003/out.jelly) | triples_rdf_1_1 |
| pos_055 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=0. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_007/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_007/out.jelly) | triples_rdf_1_1 |
| pos_056 | Stream options are: opt.physical-type=TRIPLES, opt.logical-type=FLAT_TRIPLES, generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-ta… | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_010/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/pos_010/out.jelly) | triples_rdf_1_1 |

#### Negative

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| neg_001 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=0. | negative | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/neg_001/stream_options.jelly) | — | triples_rdf_1_1 |
| neg_002 | Stream options are: generalized-statements=false, rdf-star=false, max-name-table-size=7, max-prefix-table-size=0, max-datatype-table-size=0. | negative | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1/neg_002/stream_options.jelly) | — | triples_rdf_1_1 |

### triples_rdf_1_1_generalized

*5 positive, 0 negative*

#### Positive

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| pos_057 | Stream options are: generalized-statements=true, rdf-star=false, max-name-table-size=8, max-prefix-table-size=4, max-datatype-table-size=2. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1_generalized/pos_005/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1_generalized/pos_005/out.jelly) | triples_rdf_1_1_generalized |
| pos_058 | Stream options are: generalized-statements=true, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1_generalized/pos_003/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1_generalized/pos_003/out.jelly) | triples_rdf_1_1_generalized |
| pos_059 | Stream options are: generalized-statements=true, rdf-star=false, max-name-table-size=8, max-prefix-table-size=4, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1_generalized/pos_004/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1_generalized/pos_004/out.jelly) | triples_rdf_1_1_generalized |
| pos_060 | Stream options are: generalized-statements=true, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1_generalized/pos_002/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1_generalized/pos_002/out.jelly) | triples_rdf_1_1_generalized |
| pos_061 | Stream options are: generalized-statements=true, rdf-star=false, max-name-table-size=8, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1_generalized/pos_001/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_1_1_generalized/pos_001/out.jelly) | triples_rdf_1_1_generalized |

### triples_rdf_star

*8 positive, 0 negative*

#### Positive

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| pos_062 | BNs, IRIs, and Literals used. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star/pos_007/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star/pos_007/out.jelly) | triples_rdf_star |
| pos_063 | Only IRIs as terms. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star/pos_005/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star/pos_005/out.jelly) | triples_rdf_star |
| pos_064 | Only IRIs as terms. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star/pos_006/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star/pos_006/out.jelly) | triples_rdf_star |
| pos_065 | Only IRIs as terms. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star/pos_004/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star/pos_004/out.jelly) | triples_rdf_star |
| pos_066 | Only IRIs as terms. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star/pos_002/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star/pos_002/out.jelly) | triples_rdf_star |
| pos_067 | Only IRIs as terms. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star/pos_003/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star/pos_003/out.jelly) | triples_rdf_star |
| pos_068 | Stream options are: generalized-statements=false, rdf-star=true, max-name-table-size=10, max-prefix-table-size=8, max-datatype-table-size=2. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star/pos_008/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star/pos_008/out.jelly) | triples_rdf_star |
| pos_069 | Only IRIs as terms. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star/pos_001/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star/pos_001/out.jelly) | triples_rdf_star |

### triples_rdf_star_generalized

*6 positive, 0 negative*

#### Positive

| Name | Description | Type | Data | Input(s) | Expected | Category |
|---|---|---|---|---|---|---|
| pos_070 | Stream options are: generalized-statements=true, rdf-star=true, max-name-table-size=16, max-prefix-table-size=6, max-datatype-table-size=3. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star_generalized/pos_006/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star_generalized/pos_006/out.jelly) | triples_rdf_star_generalized |
| pos_071 | Stream options are: generalized-statements=true, rdf-star=true, max-name-table-size=16, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star_generalized/pos_001/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star_generalized/pos_001/out.jelly) | triples_rdf_star_generalized |
| pos_072 | Stream options are: generalized-statements=true, rdf-star=true, max-name-table-size=16, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star_generalized/pos_002/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star_generalized/pos_002/out.jelly) | triples_rdf_star_generalized |
| pos_073 | Stream options are: generalized-statements=true, rdf-star=true, max-name-table-size=16, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star_generalized/pos_004/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star_generalized/pos_004/out.jelly) | triples_rdf_star_generalized |
| pos_074 | Stream options are: generalized-statements=true, rdf-star=true, max-name-table-size=16, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star_generalized/pos_003/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star_generalized/pos_003/out.jelly) | triples_rdf_star_generalized |
| pos_075 | Stream options are: generalized-statements=true, rdf-star=true, max-name-table-size=16, max-prefix-table-size=0, max-datatype-table-size=4. | positive | `—` | [stream_options.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star_generalized/pos_005/stream_options.jelly) | [out.jelly](https://github.com/Jelly-RDF/jelly-protobuf/blob/a91b73f9a793dceeba5ea7237f26ce98c73f887b/test/rdf/to_jelly/triples_rdf_star_generalized/pos_005/out.jelly) | triples_rdf_star_generalized |

