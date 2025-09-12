Implementations MAY choose to implement only a subset of the following specification. In this case, they SHOULD clearly specify which parts of the specification they implement. In the rest of this specification, the keywords "MUST", "MUST NOT", etc. refer to full (not partial) implementations.

!!! note

    Implementations may in particular choose to not implement features that are not supported on the target platform (e.g., RDF datasets, RDF-star, generalized RDF terms, etc.).

Implementations MAY also choose to extend Jelly with additional features that SHOULD NOT interfere with the serialization being readable by implementations which follow the specification.

### Reporting conformance

Report results using **EARL 1.0** ([Evaluation and Report Language](https://www.w3.org/WAI/standards-guidelines/earl/)), one **`earl:Assertion` per test**.  
Run the **official Jelly test manifests** for the protocol version you implement; iterate each applicable entry and record an outcome.  

**What to include:**  
- **Assertions:** for every applicable test, create a `earl:Assertion` with `earl:test` (the test IRI from the manifest), `earl:subject` (your implementation), `earl:assertedBy`, `earl:mode` (usually `earl:automatic`), and `earl:result/earl:outcome`. Allowed outcomes: `earl:passed`, `earl:failed`, `earl:inapplicable`, `earl:cantTell`, `earl:untested`.    
- **Metadata:** describe the implementation with **DOAP** (name, version, homepage) and the assertions with **FOAF**.  

**Where to submit / how it’s used:**  
- Submit the EARL file (in turtle format) via Pull Request or mail to the designated reports' location. JSON-LD, N-Triples/N-Quads and others follow this model. Submitted EARL files are then **aggregated into a human-readable table** on the site.  

**Manifests:**  
- Test manifests are RDF lists of tests that provide names, inputs/expecteds, and status; runners iterate these to produce EARL. 
- Manifests for Jelly can be found [here](https://github.com/Jelly-RDF/jelly-protobuf/tree/main/test/rdf).

### Example EARL report

This is a complete, ready-to-submit **EARL report template**. Replace placeholders (names, dates) and add one **`earl:Assertion`** per Jelly test you executed (use the exact test IRIs from the Jelly manifests).  

```turtle
# conformance-report.ttl

@prefix earl: <http://www.w3.org/ns/earl#> .
@prefix doap: <http://usefulinc.com/ns/doap#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix dc:   <http://purl.org/dc/terms/> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

# --- Document metadata ---
<> foaf:primaryTopic <#impl> ;
   dc:issued "2026-01-1T00:00:00Z"^^xsd:dateTime ;
   foaf:maker <#assertor> .

# --- Assertor (you/your org/your bot) ---
<#assertor> a foaf:Person, earl:Assertor ;
  foaf:name "Your Name or Bot Name" ;
  foaf:homepage <https://example.org/your-homepage> .

# --- Test Subject (your implementation) ---
<#impl> a doap:Project, earl:TestSubject, earl:Software ;
  doap:name "Your Jelly implementation" ;
  doap:homepage <https://example.org/your-impl-homepage> ;
  doap:description "Your implemenation description"@en ;
  doap:programming-language "Rust" ;
  doap:developer <#assertor> ;
  doap:release [
    doap:name "Your Jelly implementation 1.0.0" ;
    doap:revision "1.0.0" ;
    dc:created "2026-01-01"^^xsd:date
  ] .

# --- Assertions — one per test from the Jelly manifests you ran. ---
# --- Outcomes values can only include: passed, failed, inapplicable, cantTell, untested. ---

# Example 1
<#a-triples_rdf_1_1_pos_001> a earl:Assertion ;
  earl:assertedBy <#assertor> ;
  earl:subject    <#impl> ;
  earl:test       <https://example.org/jelly/dev/tests/rdf/from_jelly/triples_rdf_1_1/pos_001> ;
  earl:mode       earl:automatic ;
  earl:result [
    a earl:TestResult ;
    dc:date "2026-01-1T0:00:00Z"^^xsd:dateTime ;
    earl:outcome earl:passed
  ] .

# Example 2
<#a-graphs_rdf_1_1_pos_001> a earl:Assertion ;
  earl:assertedBy <#assertor> ;
  earl:subject    <#impl> ;
  earl:test       <https://example.org/jelly/dev/tests/rdf/from_jelly/graphs_rdf_1_1/pos_001> ;
  earl:mode       earl:automatic ;
  earl:result [
    a earl:TestResult ;
    dc:date "2026-01-1T0:00:00Z"^^xsd:dateTime ;
    earl:outcome earl:failed
  ] .

# Example 3
<#a-triples_rdf_1_1_neg_001> a earl:Assertion ;
  earl:assertedBy <#assertor> ;
  earl:subject    <#impl> ;
  earl:test       <https://example.org/jelly/dev/tests/rdf/from_jelly/triples_rdf_1_1/neg_001> ;
  earl:mode       earl:automatic ;
  earl:result [
    a earl:TestResult ;
    dc:date "2026-01-1T0:00:00Z"^^xsd:dateTime ;
    earl:outcome earl:passed  
  ] .

# Example 4
<#a-triples_rdf_star_pos_001> a earl:Assertion ;
  earl:assertedBy <#assertor> ;
  earl:subject    <#impl> ;
  earl:test       <https://example.org/jelly/dev/tests/rdf/from_jelly/triples_rdf_star/pos_001> ;
  earl:mode       earl:automatic ;
  earl:result [
    a earl:TestResult ;
    dc:date "2026-01-1T0:00:00Z"^^xsd:dateTime ;
    earl:outcome earl:inapplicable
  ] .

  # ... Example n-th

```