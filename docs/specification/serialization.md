# Jelly serialization format

TODO: intro, reference to RDF 1.1 and RDF-star

!!! info

    The key words "MUST", "MUST NOT", "REQUIRED", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

## Format specification

TODO: overall structure, stream frames and rows, mention lookup tables, multiple types

### Stream options

TODO

### Stream types

TODO

### Prefix, name, and datatype lookups

TODO

### RDF statements

### RDF terms

#### IRIs

#### Blank nodes

#### Literals

#### Quoted triples (RDF-star)

#### Repeated terms

### RDF graph nodes

## Delimited variant

!!! note

    Protobuf messages [are not delimited](https://protobuf.dev/programming-guides/techniques/#streaming), so if you write multiple messages to the same file / socket / byte stream, you need to add some kind of delimiter between them. Jelly uses the convention already implemented in some protobuf libraries of prepending a varint before the message, to specify the length of the message. 

A byte stream (or file) in the delimited variant MUST consist of a series of delimited `RdfStreamFrame` messages. A delimited message is a message that has a varint prepended before it, specifying the length of the message.

Implementing the delimited variant is OPTIONAL.

### Implementations

The delimiting convention is implemented in:

- C++: [delimited_message_util.cc](https://github.com/protocolbuffers/protobuf/blob/main/src/google/protobuf/util/delimited_message_util.cc)
- Java / Scala: [writeDelimitedTo](https://developers.google.com/protocol-buffers/docs/reference/java/com/google/protobuf/MessageLite#writeDelimitedTo-java.io.OutputStream-) and [parseDelimitedFrom](https://developers.google.com/protocol-buffers/docs/reference/java/com/google/protobuf/Parser#parseDelimitedFrom-java.io.InputStream-)

The JVM (Scala) implementation of Jelly also supports the delimited variant – [see the documentation](../jvm/reactive.md#byte-streams).
