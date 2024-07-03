# Jelly gRPC streaming protocol specification

**This document is the specification of the Jelly gRPC streaming protocol (publish/subscribe mechanism). It is intended for implementers of Jelly libraries and applications.** If you are looking for a user-friendly introduction to Jelly, see the [Jelly index page](index.md).

This document is accompanied by the [Jelly Protobuf reference](reference.md) and the Protobuf definition itself ([`grpc.proto`]({{ git_proto_link('grpc.proto') }})).

The following assumptions are used in this document:

- This document uses the [specification for the Jelly serialization format](serialization.md).
- All strings in the mentioned Protobuf messages are assumed to be UTF-8 encoded.
- Standard gRPC status codes are used, as defined in [gRPC documentation](https://grpc.github.io/grpc/core/md_doc_statuscodes.html).

**Author:** [Piotr Sowiński](https://orcid.org/0000-0002-2543-9461) ([Ostrzyciel](https://github.com/Ostrzyciel))

**Version:** {{ proto_version() }}

**Document status**: {{ specification_status() }} specification

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

The protocol specifies a simple publish/subscribe mechanism topics identified with UTF-8 strings. The client can subscribe to a topic and receive messages published to that topic by the server. The client can also publish messages to a topic.

The described protocol is implemented as a gRPC service `RdfStreamService` ([reference](reference.md#rdfstreamservice)).

!!! note

    The protocol does not specify what happens to the messages on the server – this is NOT a broker or message queue specification. The protocol is meant to enable point-to-point communication, but can also be used to implement a broker or a similar service (see [Usage notes](#usage-notes) below).

    You can also ignore the topics and use the protocol as a simple streaming protocol.

### Topics

Topics are identified with UTF-8 strings. The topic string MUST be valid UTF-8. There are no further restrictions on the topic string.

!!! note

    The topic can be whatever you like – it can also be empty. It is up the user to decide what to use the topics for, or if to use them at all.

### Subscribing to a stream

The client subscribes to a stream from the server with the `SubscribeRdf` RPC ([reference](reference.md#rdfstreamservice)). The RPC is initiated with an `RdfStreamSubscribe` message ([reference](reference.md#rdfstreamsubscribe)) from the client. The message includes two OPTIONAL fields:

- `topic` (1) – the topic to subscribe to. The default is an empty string.
- `options` (2) – the stream options ([`RdfStreamOptions`](reference.md#rdfstreamoptions)). The default is an empty message.

The server MUST respond with either a stream of [`RdfStreamFrame`](reference.md#rdfstreamframe) messages or an error.

#### Stream options handling

The client MAY request specific options for the stream it subscribes to. In that case, the client MUST include the `options` field in the `RdfStreamSubscribe` message. The server SHOULD respond with a stream that uses options that are compatible with the options requested by the client. If the server cannot respond with a stream that uses options that are compatible with the options requested by the client, the server MUST respond with the `INVALID_ARGUMENT` error.

The following rules are used to determine if the options are compatible. All rules MUST be satisfied for the options to be compatible.

| Option | Client request | Server response |
| --- | --- | --- |
| `stream_name` | `x` | MAY be `x` |
| `physical_type` | `x` | MUST be `x` |
| `generalized_statements` | `x` | MUST be `x` or false |
| `use_repeat` | `x` | MUST be `x` or false |
| `rdf_star` | `x` | MUST be `x` or false |
| `max_name_table_size` | `x` | MUST be <= `x` |
| `max_prefix_table_size` | `x` | MUST be <= `x` |
| `max_datatype_table_size` | `x` | MUST be <= `x` |
| `logical_type` | `x` | MAY be `x` |
| `version` | `x` | MUST be <= `x` |

!!! note

    The server should implement some limits for the stream options it supports, for example the maximum size of the name table. Otherwise, a client may request a name table that takes up all the server's memory.

Logical stream type handling is entirely dependent on the server implementation:

1. The server MAY respect the client's request in the `logical_type` field in the stream options and respond with the same type.
2. The server MAY respect the client's request in the `logical_type` field in the stream options and respond with a subtype of the requested type.
3. The server MAY ignore the `logical_type` field in the client request and respond with its own type or with no type at all.
4. The server MAY respond with an `INVALID_ARGUMENT` error if the client requests a type that the server does not support with the specified physical stream type.

!!! note

    How you implement this behavior depends on your use case, possibly combining the above options. For example, you may want to allow the client to request a specific logical type, but only if it is compatible with the physical type. Or, if your server supports stream type conversion, you may want to allow the client to request a specific logical type and let the server handle the conversion.

### Publishing a stream

The client publishes a stream to the server with the `PublishRdf` RPC ([reference](reference.md#rdfstreamservice)). The RPC is initiated with a stream of [`RdfStreamFrame`](reference.md#rdfstreamframe) messages from the client. The stream MUST include at least one message. The first frame MUST include a row with the stream options as the first row. After the stream successfully completes, the server MUST respond with the `RdfStreamReceived` message ([reference](reference.md#rdfstreamreceived)).

If the server cannot handle the stream with the specified options, the server MUST respond with the `INVALID_ARGUMENT` error.

## Usage notes

*This section is not part of the specification.*

The protocol is deliberately very general and unrestrictive. The pub/sub mechanism can be used in a number of ways, possibly extending the existing base protocol. The following are some examples of how the protocol can be used:

- Server publishing a number of streams, each with a different topic.
- RDF stream broker or message queue – the server acts as a "hub" aggregating RDF data sent to a topic by clients, and then forwarding it to other clients.
- Microservice chains – one service can process an RDF stream, forward it to another service, etc.

These use cases can be implemented with the protocol as-is, or by extending the protocol with additional messages and/or RPCs. In either case, the protocol provides a base layer for compatibility between different implementations.

## Implementations

*This section is not part of the specification.*

The following implementations of the Jelly gRPC streaming protocol specification are available:

- [Jelly-JVM (Scala) implementation]({{ jvm_link() }})
    - Specification version: {{ proto_version() }}
    - Partial (boilerplate) implementation based on [Apache Pekko gRPC](https://pekko.apache.org/docs/pekko-grpc/current/). Requires the end user to implement their own code for handling the streams.
