# Jelly-SPARQL test cases

This page lists the conformance test cases defined for the [Jelly-SPARQL format](../specification/sparql.md), along with instructions for running them.

!!! warning

    Jelly-SPARQL is an experimental draft, and so is its test suite. Both may change.

Machine-readable definitions of the test cases are available in the [jelly-protobuf repository]({{ git_test_link('sparql') }}).

See also instructions on [reporting conformance](reporting-conformance.md).

## Test categories

Categories indicate supported features: `select_rdf_1_1` (solution sequences with IRIs, blank nodes, and literals), `ask` (boolean results), `select_rdf_1_2_basic` (literals with a base direction, RDF 1.2 Basic), `select_rdf_1_2` (triple terms, RDF 1.2), `punctuated` (streams with a sequence of result sets, the [`PUNCTUATED` stream type](../specification/sparql.md#stream-types)).

Tests in the `select_rdf_1_2_basic` category are marked with `mf:requires jellyt:requirementRdf12Basic`, tests in the `select_rdf_1_2` category with `mf:requires jellyt:requirementRdf12`, and tests in the `punctuated` category with `mf:requires jellyt:requirementPunctuated`. If your implementation does not support a given feature, you should skip the corresponding tests.

## Running tests

- Test cases beginning with `pos_` are positive tests, and those beginning with `neg_` are negative tests.
    - A positive test is expected to succeed. The test case is successful when the implementation returns the expected result specified in `mf:result`.
    - A negative test is expected to fail. The test case is successful when the implementation returns an error. Currently, the test cases do not specify the expected error code.
- There are two types of tests:
    - From Jelly (parse) tests – `jellyt:TestSparqlFromJelly`. The goal of the test is to convert the Jelly-SPARQL input specified in `mf:action` to a SPARQL result.
        - The input (`mf:action`) MUST be an RDF IRI pointing to a `.jellys` file.
        - If the test is positive, the output (`mf:result`) MUST be an RDF IRI pointing to a `.srj` file with the expected result. For a `PUNCTUATED` stream, it MUST instead be an `rdf:List` of `.srj` files, one per result set, in order. The implementation must then read the same number of result sets, and each must be equivalent to the expected one at the same position.
        - This class MUST be combined with either `jellyt:TestPositive` or `jellyt:TestNegative`. When combined with `jellyt:TestPositive`, the test succeeds when the input is read without errors, and the result is equivalent to the expected result specified in `mf:result`.
    - To Jelly (serialize) tests – `jellyt:TestSparqlToJelly`. The goal of the test is to convert the SPARQL result specified in `mf:action` to a Jelly-SPARQL file.
        - The input (`mf:action`) MUST be an `rdf:List` of two or more elements. The first element is a Jelly-SPARQL file with one frame, holding only the stream options to be used by the producer. The remaining elements are `.srj` files with the SPARQL results to be converted: one file, or, for a `PUNCTUATED` stream, one file per result set, in order.
        - If the test is positive, the output (`mf:result`) MUST be an RDF IRI pointing to a `.jellys` file with one valid serialization of the result. If the test is negative, `mf:result` is not set.
        - This class MUST be combined with either `jellyt:TestPositive` or `jellyt:TestNegative`. When combined with `jellyt:TestPositive`, the test succeeds when the first frame of the resulting Jelly-SPARQL file has the expected stream options, and reading the file back gives a result equivalent to the input. Jelly-SPARQL is not byte-level canonical, so the resulting file SHOULD NOT be compared with the file in `mf:result` byte by byte.
- Two SPARQL results are equivalent when both are boolean results with the same value, or when they have the same variables in the same order, the same number of solutions in the same order, and there is a bijection between their blank node labels under which the solutions are pairwise equal. A simple literal and an `xsd:string` literal with the same lexical form are the same term. Links (`head.link`) are not compared.
- The `.srj` files use the [SPARQL 1.2 Query Results JSON Format](https://www.w3.org/TR/sparql12-results-json/): `"its:dir"` for base directions, and `{"type": "triple", ...}` for triple terms.
- The test cases use the delimited variant of Jelly-SPARQL.
- Some positive tests have no [stream trailer](../specification/sparql.md#stream-trailer). The implementation may report such a stream as possibly truncated, but it must not fail these tests because of that.
- Tests of rules that the specification states with SHOULD rather than MUST are marked with the `jellyt:featureShouldLevel` feature (`mf:notable` property). An implementation may fail them and still conform to the specification.

See also [the test manifest vocabulary]({{ git_test_link('vocabulary.ttl') }}) for details on how the test cases are defined in RDF.

## Test summary

{{ conformance_tests('sparql') }}
