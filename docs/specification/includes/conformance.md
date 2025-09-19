Implementations MAY choose to implement only a subset of the following specification. In this case, they SHOULD clearly specify which parts of the specification they implement. In the rest of this specification, the keywords "MUST", "MUST NOT", etc. refer to full (not partial) implementations.

!!! note

    Implementations may in particular choose to not implement features that are not supported on the target platform (e.g., RDF datasets, RDF-star, generalized RDF terms, etc.).

Implementations MAY also choose to extend Jelly with additional features that SHOULD NOT interfere with the serialization being readable by implementations which follow the specification.

### Reporting conformance

Report results using **EARL 1.0** ([Evaluation and Report Language](https://www.w3.org/WAI/standards-guidelines/earl/)), one **`earl:Assertion`** per test.  
Run the **official Jelly test manifests** for the protocol version you implement; iterate each applicable entry and record its outcome.  

**What to include:**  
- **Assertions:** for every applicable test, create a **`earl:Assertion`** with **`earl:test`** (the test IRI from the manifest), **`earl:subject`** (your implementation), **`earl:assertedBy`**, **`earl:mode`** (usually **`earl:automatic`**), and **`earl:result/earl:outcome`** (allowed outcomes: **`earl:passed`**, **`earl:failed`**, **`earl:inapplicable`**, **`earl:cantTell`**, **`earl:untested`**).    
- **Metadata:** describe the implementation with **DOAP** (name, version, homepage) and the assertions with **FOAF**.  

#### Where to submit / how it’s used  

Submit the EARL file (in turtle format) via Pull Request [onto this GitHub repository](https://github.com/Jelly-RDF/jelly-rdf.github.io) into the [docs section](https://github.com/Jelly-RDF/jelly-rdf.github.io/tree/main/docs) under specifications' directory. Submitted EARL files are then **aggregated into a human-readable table** on the site.  

!!! note "Example EARL report"
    An example, complete, ready-to-submit **EARL report template** can be found [here](https://github.com/Jelly-RDF/jelly-rdf.github.io/tree/main/docs/specifications). Replace placeholders (names, dates) and add one **`earl:Assertion`** per Jelly test you executed (use the exact test IRIs from the Jelly manifests).   

**Manifests:**  
- Test manifests are RDF lists of tests that provide names, inputs/expecteds, and status; test runners iterate these to produce EARL reports.  
- Manifests for Jelly can be found [here](https://github.com/Jelly-RDF/jelly-protobuf/tree/main/test/rdf).
