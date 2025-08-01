# Protobuf sources

Below you will find the [Protocol Buffers](https://protobuf.dev/programming-guides/proto3/) definitions for the [Jelly-RDF](serialization.md) and [Jelly-Patch](patch.md) formats, along with the [Jelly gRPC streaming protocol](streaming.md). The original files are hosted on [GitHub](https://github.com/Jelly-RDF/jelly-protobuf) and all releases can be found [here](https://github.com/Jelly-RDF/jelly-protobuf/releases).

Human-readable reference for these definitions can be found [here](reference.md).

The following code is licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

## `rdf.proto`

```protobuf
{% include "./proto/rdf.proto" %}
```

## `patch.proto`

```protobuf
{% include "./proto/patch.proto" %}
```

## `grpc.proto`

```protobuf
{% include "./proto/grpc.proto" %}
```

## See also

- [Jelly Protobuf reference](reference.md)
- [Jelly-RDF specification](serialization.md)
- [Jelly-Patch specification](patch.md)
- [gRPC streaming protocol specification](streaming.md)
