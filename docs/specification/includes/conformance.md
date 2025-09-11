Implementations MAY choose to implement only a subset of the following specification. In this case, they SHOULD clearly specify which parts of the specification they implement. In the rest of this specification, the keywords "MUST", "MUST NOT", etc. refer to full (not partial) implementations.

!!! note "Official Jelly test suite"
    Conformance is established by the results of the [official Jelly tests](https://github.com/Jelly-RDF/jelly-protobuf/tree/main/test).  
    To claim conformance, an implementation MUST pass all applicable tests for the protocol version it implements.  
    Partial implementations MUST pass the respective tests for the parts they implement and MUST state the protocol version.

!!! note

    Implementations may in particular choose to not implement features that are not supported on the target platform (e.g., RDF datasets, RDF-star, generalized RDF terms, etc.).

Implementations MAY also choose to extend Jelly with additional features that SHOULD NOT interfere with the serialization being readable by implementations which follow the specification.