# Jelly-RDF conformance reports

This page lists conformance testing results for Jelly-RDF implementations. Details on the tests themselves are provided on the [conformance tests](rdf-test-cases.md) page, and guidance on producing reports can be found on the [reporting conformance](reporting-conformance.md) page.

The information presented here includes:

- The [**report table**](#report-table), which provides a comparative overview of test outcomes across all submitted implementations.  
- The [**available reports**](#available-reports) section, which lists implementation metadata (name, version, developer, assertor, and issue date) together with compliance statistics.

Note that implementations are not required to cover all features of Jelly-RDF. In particular, you will find that many implementations do not support:

- The GRAPHS physical type for serialization (to Jelly). The GRAPHS type is considered legacy, and using the QUADS type is recommended instead.
- Generalized RDF (e.g., triples with literals in subject position). Many RDF libraries do not support this feature.
- RDF-star (i.e., quoted triples). Some RDF libraries do not support this feature.

In general, all implementations should at least pass the following test categories for parsing (from Jelly): `graphs_rdf_1_1`, `triples_rdf_1_1`, and `quads_rdf_1_1`.

{{ conformance_report() }}
