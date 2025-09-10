Implementations MAY choose to implement only a subset of the following specification. In this case, they SHOULD clearly specify which parts of the specification they implement. In the rest of this specification, the keywords "MUST", "MUST NOT", etc. refer to full (not partial) implementations.

!!! note "**The official Jelly conformance tests determine conformance**"
    Conformance is checked and determined by running the official Jelly [conformance tests](https://github.com/Jelly-RDF/jelly-protobuf/tree/main/test).  
    An implementation may claim conformance only if, for its implemented protocol version, it MUST pass all applicable tests.  
    Claims of partial conformance **MUST** state exactly which test groups were passed and the protocol version.

!!! note

    Implementations may in particular choose to not implement features that are not supported on the target platform (e.g., RDF datasets, RDF-star, generalized RDF terms, etc.).

Implementations MAY also choose to extend Jelly with additional features that SHOULD NOT interfere with the serialization being readable by implementations which follow the specification.