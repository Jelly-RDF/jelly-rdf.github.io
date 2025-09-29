# Jelly-RDF test cases

This page lists the conformance test cases defined for the Jelly-RDF format, along with instructions for running them.

Machine-readable definitions of the test cases are available in the [jelly-protobuf repository]({{ git_test_link('rdf') }}).

See also instructions on [reporting conformance](reporting-conformance.md) and the [page listing conformance reports of implementations](rdf-reports.md) page.

## Test categories

Categories indicate supported features: `rdf_star` (RDF-star), `generalized` (generalized RDF), `graphs` (the GRAPHS physical type), `quads` (QUADS physical type), `triples` (TRIPLES physical type).

If your implementation does not support a given feature, you should skip the corresponding tests.

## Running tests

- Test cases beginning with `pos_` are positive tests, and those beginning with `neg_` are negative tests.
    - A positive test is expected to succeed. The test case is successful when the implementation returns the expected result specified in `mf:result`.
    - A negative test is expected to fail. The test case is successful when the implementation returns an error. Currently, the test cases do not specify the expected error code, but this will be added in the future.
- There are two types of tests:
    - From Jelly (parse) tests – `jellyt:TestRdfToJelly`. The goal of the test is to convert the Jelly-RDF input specified in mf:action to an RDF file or a series of RDF files.
        - The input (`mf:action`) MUST be an RDF IRI pointing to a .jelly file.
        - If the test is positive, the output (`mf:result`) MUST be an `rdf:List` of RDF IRIs with the expected output files. The output files are either in N-Triples or N-Quads format.
        - This class MUST be combined with either `jellyt:TestPositive` or `jellyt:TestNegative`. When combined with `jellyt:TestPositive`, the test succeeds when the resulting RDF file is syntactically valid and is equivalent to the expected RDF file specified in `mf:result`, when compared using the ordered RDF dataset isomorphism algorithm. In case the test includes multiple frames (multiple output files), the equivalence must be checked for each frame separately.
    - To Jelly (serialize) tests – `jellyt:TestJellyToRdf`. The goal of the test is to convert the RDF input specified in mf:action to a Jelly-RDF file.
        - The input (mf:action) MUST be an `rdf:List`. The first element of the list is a Jelly-RDF file containing the stream options to be used by the producer. The subsequent elements are the RDF files to be converted to Jelly-RDF. The input files are either in N-Triples or N-Quads format.
        - If the test is positive, the output (`mf:result`) MUST be an RDF IRI pointing to a .jelly file  with the expected Jelly-RDF file. If the test is negative, `mf:result` is not set.
        - This class MUST be combined with either `jellyt:TestPositive` or `jellyt:TestNegative`. When combined with `jellyt:TestPositive`, the test succeeds when the resulting Jelly-RDF file has the expected stream options, is syntactically valid, and is equivalent to the expected Jelly-RDF file specified in `mf:result`, when compared using the ordered RDF dataset isomorphism algorithm. This can be done with the [jelly-cli tool](https://github.com/Jelly-RDF/cli): `jelly-cli rdf validate --compare-to-rdf-file=<output> --compare-ordered=true --compare-frame-indices=<frame-index-to-compare> --options-file=<options-file> <implementation-output>`
- Generally, the test cases use the delimited form of Jelly-RDF. If non-delimited files are used, the test is marked with the `jellyt:featureNonDelimited` feature (`mf:notable` property).
- Blank node identifiers in the input files should be considered to all come from the same blank node pool, i.e. blank nodes should be considered equal if they have the same identifier.

See also [the test manifest vocabulary]({{ git_test_link('vocabulary.ttl') }}) for details on how the test cases are defined in RDF.

## Test summary

{{ conformance_tests() }}
