# Jelly protocol specification

**There are two Jelly-based serialization formats: [Jelly-RDF](serialization.md) for RDF data and [Jelly-Patch](patch.md) for RDF patches (diffs).** Additionally, there is the [gRPC RDF streaming protocol](streaming.md) defining an end-to-end mechanism for exchanging RDF data over the network.

The following documents contain the formal specification of these formats and protocols, and are the "ultimate source of truth" for any implementations. **See the [user guide](../user-guide.md) for a friendlier introduction to Jelly.**

See the specification pages for more details:

- Specification documents:
    - [RDF serialization format specification](serialization.md) – for serializing streams of RDF triples, quads, graphs, datasets.
    - [RDF Patch format specification](patch.md) – for serializing streams of changes to RDF data.
    - [gRPC RDF streaming protocol specification](streaming.md) – for exchaning Jelly-RDF over the network.
- Protobuf definitions:
    - [Protobuf reference](reference.md)
    - [Protobuf sources](protobuf-source.md)
- [File extensions and media types](media-type.md)
