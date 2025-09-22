To ensure interoperability between different Jelly implementations, it is important to verify that each system correctly follows the specification. Conformance testing provides a consistent way to demonstrate which features are implemented and how well they align with the standard. Results are recorded in a standardized format so they can be automatically aggregated, compared, and published.

!!! note
    Implementations may extend Jelly with additional features, provided these extensions do not prevent the serialization from being readable by implementations that follow the requirements.

## How to report conformance?

Report results using **EARL 1.0** ([Evaluation and Report Language](https://www.w3.org/WAI/standards-guidelines/earl/)), one **`earl:Assertion`** per test.  
Run the official Jelly test manifests for the protocol version you implement; iterate each applicable entry and record its outcome.  

**What to include:**

- **Assertions:** for every applicable test, create a **`earl:Assertion`** with **`earl:test`** (the test IRI from the manifest), **`earl:subject`** (your implementation), **`earl:assertedBy`**, **`earl:mode`** (usually **`earl:automatic`**), and **`earl:result/earl:outcome`** (allowed outcomes: **`earl:passed`**, **`earl:failed`**, **`earl:inapplicable`**, **`earl:cantTell`**, **`earl:untested`**).  
- **Metadata:** describe the implementation with [**DOAP**](https://github.com/ewilderj/doap) (name, version, homepage) and the assertions with [**FOAF**](http://xmlns.com/foaf/spec/).  

### Where to submit / how it’s used

Submit the EARL file (in Turtle format) via pull request [to this directory]({{ git_tree_link('tree/main/docs/conformance/reports') }}). Submitted EARL files are then aggregated into a human-readable table on the site.  

!!! note "Example EARL report"
    An example, complete, ready-to-submit EARL report template can be found [here]({{ git_tree_link('tree/main/docs/conformance/reports') }}). Replace placeholders (names, dates) and add one **`earl:Assertion`** per Jelly test you executed (use the exact test IRIs from the Jelly manifests).  

**Manifests:**

- Test manifests are RDF lists of tests that provide names, inputs/expecteds, and status; test runners iterate these to produce EARL reports.  
- Manifests for Jelly can be found [here]({{ git_test_link('/rdf') }}).
