Jelly uses conformance test cases as an additional way to verify that implementations correctly follow the specification. Results of these conformance tests ran against different implementations are recorded in a standardized format so they can be automatically aggregated, compared, and published.

## How to report conformance?

Report results using **EARL 1.0** ([Evaluation and Report Language](https://www.w3.org/WAI/standards-guidelines/earl/)), one `earl:Assertion` per test. Run the official Jelly test manifests for the protocol version you implement; iterate each applicable entry and record its outcome.  

### What to include

- **Assertions:** for every applicable test, create a `earl:Assertion` with `earl:test` (the test IRI from the manifest), `earl:subject` (your implementation), `earl:assertedBy`, `earl:mode` (usually `earl:automatic`), and `earl:result/earl:outcome` (allowed outcomes: `earl:passed`, `earl:failed`, `earl:inapplicable`, `earl:cantTell`, `earl:untested`).  
- **Metadata:** describe the implementation with [**DOAP**](https://github.com/ewilderj/doap) (name, version, homepage) and the assertions with [**FOAF**](http://xmlns.com/foaf/spec/).  

### Where to submit / how it’s used

Submit the EARL file (in Turtle format) via pull request [to this directory]({{ git_tree_link('tree/main/docs/conformance/reports') }}). Submitted EARL files are then aggregated into a human-readable table like [this one for Jelly-RDF](rdf-reports.md) and published on the Jelly website.

!!! note "Example EARL report"

    An example, complete, ready-to-submit EARL report template can be found **[here]({{ git_tree_link('tree/main/docs/conformance/reports') }})**. Replace placeholders (names, dates) and add one `earl:Assertion` per Jelly test you executed (use the exact test IRIs from the Jelly manifests).  

### Where to find the test cases

See the [Jelly-RDF test cases](rdf-test-cases.md) page for details on the available tests and how to run them.

## See also

- Jelly-RDF
    - [Test cases](rdf-test-cases.md)
    - [Conformance reports](rdf-reports.md)
