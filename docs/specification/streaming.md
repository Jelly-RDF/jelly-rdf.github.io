# Jelly gRPC streaming protocol specification

**This document is the specification of the Jelly gRPC streaming protocol (publish/subscribe mechanism). It is intended for implementers of Jelly libraries and applications.** If you are looking for a user-friendly introduction to Jelly, see the [Jelly index page](index.md).

This document is accompanied by the [Jelly Protobuf reference](reference.md) and the Protobuf definition itself ([`grpc.proto`](https://github.com/Jelly-RDF/jelly-protobuf/blob/main/grpc.proto)).

The following assumptions are used in this document:

- This document uses the [specification for the Jelly serialization format](serialization.md).
- All strings in the mentioned Protobuf messages are assumed to be UTF-8 encoded.

**Author:** [Piotr Sowiński](https://orcid.org/0000-0002-2543-9461) ([Ostrzyciel](https://github.com/Ostrzyciel))

**Version:** 1.0.0

**Document status**: Draft specification

!!! info

    The key words "MUST", "MUST NOT", "REQUIRED", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

!!! note

    The "Note" blocks in this document are not part of the specification, but rather provide additional information for implementers.

!!! note

    The "Example" blocks in this document are not part of the specification, but rather provide informal examples of the serialization format. The examples use the [Protocol Buffers Text Format Language](https://protobuf.dev/reference/protobuf/textformat-spec/).


## Conformance

Implementations MAY choose to implement only a subset of the following specification. In this case, they SHOULD clearly specify which parts of the specification they implement. In the rest of this specification, the keywords "MUST", "MUST NOT", etc. refer to full (not partial) implementations.

## Versioning

The streaming protocol follows the [Semantic Versioning 2.0](https://semver.org/) scheme. The version of the gRPC streaming protocol is equal to the version of the corresponding serialization format (1:1 equivalence). The version of the protocol is specified in the stream options – see the [serialization specification](serialization.md#versioning) for details.

!!! note
    
    Releases of the protocol are published on [GitHub](https://github.com/Jelly-RDF/jelly-protobuf/releases).

### Backward compatibility

Implementations SHOULD ensure backward compatibility. To achieve backward compatibility, the implementation MUST be able to respond to all RPCs from the previous releases of the protocol with the same MAJOR version. The implementation MAY also be able to respond to RPCs from previous releases of the protocol with a different MAJOR version.

!!! note

    The protocol is designed in such a way that you don't need to worry about backward compatibility. The only thing you need to do is to implement the latest version of the protocol, and you will automatically get backward compatibility with all previous versions (of the same MAJOR).

### Forward compatibility

Forward compatibility is not guaranteed. Implementations MAY be able to respond to RPCs from future releases of the protocol with the same MAJOR version. Implementations MAY also be able to respond to RPCs from future releases of the protocol with a different MAJOR version.

## Actors and implementations

The Jelly gRPC streaming protocol assumes there to be two actors: the server and the client. These actors can both play the role of the producer or the consumer of the stream (see [serialization specification](serialization.md#actors-and-implementations)), depending on the direction of the stream.

Implementations may include only the server, only the client, or both.

## Protocol specification

### Topics

### Subscribing to a stream

TODO

#### Stream options handling

#### Error handling

### Publishing a stream

TODO

#### Stream options handling

#### Error handling

## Implementations

TODO
