# Jelly-RDF benchmarks

The following results were obtained by benchmarking [Jelly-JVM]({{ jvm_link() }}) 4.0.0 against the RDF serialization formats built into Apache Jena and Eclipse RDF4J. For SPARQL query results, see [Jelly-SPARQL benchmarks](sparql.md).

The benchmarks were performed on flat RDF streams – streams of RDF triples or quads. This is the "classic" serialization – equivalent to, for example, N-Triples or N-Quads.

The charts are interactive – hover over them for details. The data behind each chart is listed below it.

## Benchmark setup

All benchmarks were performed on the first 100,000 statements of each dataset in [RiverBench](https://w3id.org/riverbench/v/dev) (development version, October 2026), except `yago-annotated-facts`, which uses RDF-star. Out of the 13 used datasets, 3 include RDF quads (`assist-iot-weather-graphs`, `citypulse-traffic-graphs`, `nanopubs`).

- Each method/dataset combination was run in 3 separate JVM forks, each with 5 × 1 s warmup and 5 × 1 s measurement. The result for a dataset is the median of the 3 forks.
- Serialization: the data was preloaded into memory and serialized to a null output stream.
- Deserialization: the data was deserialized from a byte array in memory. The deserializer was emitting only a stream of triples/quads, without any further processing.
- All parsers and writers were configured to skip optional work that can be turned off in the library: IRI, language tag, and datatype validation, blank node relabeling, and pretty-printing. Writers that use prefixes were given the prefixes of the dataset.
- Averages are geometric means over the datasets.

Hardware: NVIDIA DGX Spark (GB10 Grace Blackwell Superchip with 10 Cortex-X925 and 10 Cortex-A725 cores; 128 GB unified memory). The benchmarks were pinned to 5 Cortex-X925 cores (3.9 GHz) and are single-threaded. The disk was not used during the benchmarks (all data was in memory).

Software: Linux kernel 6.17, GraalVM CE 25.4 (Java 25.0.4), Apache Jena 6.2.0, Eclipse RDF4J 6.1.0, [Jelly-JVM]({{ jvm_link() }}) 4.0.0.

### Tested methods

- W3C N-Triples / N-Quads (Apache Jena, Eclipse RDF4J)
- W3C Turtle / TriG (Apache Jena `TURTLE_BLOCKS` and `TRIG_BLOCKS`, Eclipse RDF4J without pretty-printing)
- W3C RDF/XML (Apache Jena `RDFXML_PLAIN`, Eclipse RDF4J) – triples only
- W3C JSON-LD (Apache Jena `JSONLD11_FLAT`, Eclipse RDF4J)
- W3C RDF/JSON (Apache Jena, Eclipse RDF4J) – triples only
- [Jena's RDF binary](https://jena.apache.org/documentation/io/rdf-binary.html) Protobuf and Thrift formats (Apache Jena, `RDF_PROTO` and `RDF_THRIFT`)
- [RDF4J Binary RDF Format](https://rdf4j.org/documentation/reference/rdf4j-binary/) (Eclipse RDF4J, `BINARY`)
- Jelly (Jelly-JVM 4.0.0, Jelly-RDF 1.2, "big" preset)
    ```protobuf
    max_name_table_size = 4000;
    max_prefix_table_size = 150;
    max_datatype_table_size = 32;
    ```

## Results

### Throughput

--8<-- "snippets/performance/a-overview-rdf.html"

### Throughput and serialized size

--8<-- "snippets/performance/b-speed-size-rdf-triples.html"

### Throughput per dataset

--8<-- "snippets/performance/c-heatmap-rdf.html"

--8<-- "snippets/performance/d-spread-rdf-triples.html"

### Serialized size

--8<-- "snippets/performance/f-size-rdf-triples.html"

## See also

- [Jelly-SPARQL benchmarks](sparql.md)
- [Benchmark code](https://github.com/Jelly-RDF/jelly-jvm/tree/main/jmh)
- [RiverBench benchmark suite](https://w3id.org/riverbench/)
- [Jelly-JVM]({{ jvm_link() }}) – the Jelly implementation used in the benchmarks
- [User guide](../user-guide.md)
