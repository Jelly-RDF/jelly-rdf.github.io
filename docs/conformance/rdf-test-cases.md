# Jelly-RDF test cases

This page lists the conformance test cases defined for the [Jelly-RDF 1.2 format](../specification/serialization.md) (version tag 3, the column layout), along with instructions for running them.

Machine-readable definitions of the test cases are available in the [jelly-protobuf repository]({{ git_test_link('rdf/v1_2') }}).

!!! info "Jelly-RDF 1.0 and 1.1 streams"

    A consumer of Jelly-RDF 1.2 must also be able to read streams with version tags 1 and 2 (Jelly-RDF 1.0 and 1.1). These are tested by a separate test suite, listed on the [Jelly-RDF 1.1 test cases](rdf-1-1-test-cases.md) page. Its "to Jelly" tests apply only to producers that write Jelly-RDF 1.1.

See also instructions on [reporting conformance](reporting-conformance.md) and the [page listing conformance reports of implementations](rdf-reports.md) page.

## Test categories

Categories indicate supported features:

| Category                | Physical type | RDF terms                                           | `mf:requires` |
| ----------------------- | ------------- | --------------------------------------------------- | ------------- |
| `triples_rdf_1_1`       | `TRIPLES`     | IRIs, blank nodes, literals                         | `jellyt:requirementPhysicalTypeTriples` |
| `quads_rdf_1_1`         | `QUADS`       | IRIs, blank nodes, literals                         | `jellyt:requirementPhysicalTypeQuads` |
| `triples_rdf_1_2_basic` | `TRIPLES`     | also literals with a [base direction](../specification/serialization.md#base-direction) | also `jellyt:requirementRdf12Basic` |
| `quads_rdf_1_2_basic`   | `QUADS`       | also literals with a base direction                 | also `jellyt:requirementRdf12Basic` |
| `triples_rdf_1_2`       | `TRIPLES`     | also [triple terms](../specification/serialization.md#triple-terms) | also `jellyt:requirementRdf12` |
| `quads_rdf_1_2`         | `QUADS`       | also triple terms                                   | also `jellyt:requirementRdf12` |
| `messages`              | either        | IRIs, blank nodes, literals                         | `jellyt:requirementMessages`, and the requirement of the physical type |

The tests in the `messages` category use streams of [RDF Messages](../specification/serialization.md#stream-types) (stream type `MESSAGES`), which implementations are not required to support. Most tests of the rules shared by all streams (stream options, lookups, columns) are in the `triples_rdf_1_1` category.

If your implementation does not support a given feature, you should skip the corresponding tests.

## Running tests

- Test cases beginning with `pos_` are positive tests, and those beginning with `neg_` are negative tests.
    - A positive test is expected to succeed. The test case is successful when the implementation returns the expected result specified in `mf:result`.
    - A negative test is expected to fail. The test case is successful when the implementation returns an error. Currently, the test cases do not specify the expected error code.
- There are two types of tests:
    - From Jelly (parse) tests – `jellyt:TestRdf12FromJelly`. The goal of the test is to convert the Jelly-RDF input specified in `mf:action` to RDF.
        - The input (`mf:action`) MUST be an RDF IRI pointing to a `.jelly` file.
        - If the test is positive, the output (`mf:result`) depends on the stream type. For a `FLAT` stream, it MUST be an RDF IRI pointing to one N-Triples or N-Quads file with all statements of the stream. For a stream of RDF Messages, it MUST be an `rdf:List` of N-Triples or N-Quads files, one per message, in order. The file of an empty message is empty.
        - This class MUST be combined with either `jellyt:TestPositive` or `jellyt:TestNegative`. When combined with `jellyt:TestPositive`, the test succeeds when the input is read without errors, and its statements are equivalent to the expected ones (see below). For a stream of RDF Messages, the implementation must read the same number of messages, and each must be equivalent to the expected file at the same position.
    - To Jelly (serialize) tests – `jellyt:TestRdf12ToJelly`. The goal of the test is to convert the RDF input specified in `mf:action` to a Jelly-RDF file.
        - The input (`mf:action`) MUST be an `rdf:List` of two or more elements. The first element is a Jelly-RDF file with one frame, containing only the stream options to be used by the producer. The remaining elements are N-Triples or N-Quads files with the statements to be converted: one file for a `FLAT` stream, or one file per message, in order, for a stream of RDF Messages.
        - If the test is positive, the output (`mf:result`) MUST be an RDF IRI pointing to a `.jelly` file with one valid serialization of the input. If the test is negative, `mf:result` is not set.
        - This class MUST be combined with either `jellyt:TestPositive` or `jellyt:TestNegative`. When combined with `jellyt:TestPositive`, the test succeeds when the resulting file is a valid Jelly-RDF 1.2 stream, its first non-empty frame has the expected stream options, and reading it back gives statements equivalent to the input. If the input has no statements, an output without any non-empty frame (for example, an empty file) is also correct.
- Two lists of statements are equivalent when they have the same statements in the same order, and there is a bijection between their blank node labels under which the statements are pairwise equal (ordered RDF dataset isomorphism). A simple literal and an `xsd:string` literal with the same lexical form are the same term.
- Blank node labels are scoped as in the [specification](../specification/serialization.md#blank-nodes): a `FLAT` stream, and its N-Triples or N-Quads file, is one scope. In a stream of RDF Messages, each message, and its file, is its own scope.
- The N-Triples and N-Quads files use the [RDF 1.2 syntax](https://www.w3.org/TR/rdf12-n-triples/).
- The test cases use the delimited variant of Jelly-RDF. If a non-delimited file is used, the test is marked with the `jellyt:featureNonDelimited` feature (`mf:notable` property).
- Tests of rules that the specification states with SHOULD rather than MUST are marked with the `jellyt:featureShouldLevel` feature (`mf:notable` property). An implementation may fail them and still conform to the specification.

See also [the test manifest vocabulary]({{ git_test_link('test-manifest.yaml') }}) for details on how the test cases are defined in RDF. The vocabulary is a [LinkML](https://linkml.io) schema, and it is also published in RDFS and SHACL with every [release of jelly-protobuf](https://github.com/Jelly-RDF/jelly-protobuf/releases).

## Test summary

{{ conformance_tests('rdf/v1_2') }}
