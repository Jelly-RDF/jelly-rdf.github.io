# Jelly-SPARQL conformance reports

This page lists conformance testing results for Jelly-SPARQL implementations. Details on the tests themselves are provided on the [conformance tests](sparql-test-cases.md) page, and guidance on producing reports can be found on the [reporting conformance](reporting-conformance.md) page.

The information presented here includes:

- The [**report table**](#report-table), which provides a comparative overview of test outcomes across all submitted implementations.
- The [**available reports**](#available-reports) section, which lists implementation metadata (name, version, developer, assertor, and issue date) together with compliance statistics.

Note that implementations are not required to cover all features of Jelly-SPARQL. The `select_rdf_1_2_basic`, `select_rdf_1_2`, and `punctuated` test categories cover optional features. Tests of rules stated with SHOULD are included in the percentages, although an implementation may fail them and still conform to the specification.

{{ conformance_report('sparql') }}
