# Jelly protocol specification

**The Jelly protocol consists of two parts: the [gRPC streaming protocol](streaming.md) and the [serialization format](serialization.md).** The serialization format is the basis for Jelly, specifying how to turn RDF data into bytes and back. The gRPC streaming protocol defines a publish/subscribe mechanism for exchanging RDF data between a client and a server, using gRPC.

**See the [user guide](../user-guide.md) for a friendly introduction to Jelly.**

See the specification pages for more details:

- [Serialization format](serialization.md)
- [gRPC streaming protocol](streaming.md)
- [File extension and media type](media-type.md)
