# Jelly-RDF benchmarks

The following results were obtained by benchmarking [Jelly-JVM]({{ jvm_link() }}) 4.0.0 against the RDF serialization formats built into Apache Jena and Eclipse RDF4J. For SPARQL query results, see [Jelly-SPARQL benchmarks](sparql.md).

The benchmarks were performed on flat streams of RDF triples or quads.

The charts are interactive – hover over them for details.

## Benchmark setup

All benchmarks were performed on the first 100,000 statements of each dataset in [RiverBench](https://w3id.org/riverbench/v/dev) (development version, October 2026), except `yago-annotated-facts`, which uses RDF-star. Out of the 13 used datasets, 3 include RDF quads (`assist-iot-weather-graphs`, `citypulse-traffic-graphs`, `nanopubs`).

- Each method/dataset combination was run in 3 separate JVM forks (sweeps), each with 5 × 1 s warmup and 5 × 1 s measurement. The result for a dataset is the median of the 3 sweeps.
- Serialization: the data was preloaded into memory and serialized to a null output stream.
- Deserialization: the data was deserialized from a byte array input stream in memory. The deserializer was emitting only a stream of triples/quads, without any further processing.
- All parsers and writers were configured to skip optional work that can be turned off in the library: IRI, language tag, and datatype validation, blank node relabeling, and pretty-printing. Writers that use prefixes were given the prefixes of the dataset.
- Averages are geometric means over the datasets.

Hardware: NVIDIA DGX Spark (GB10 Grace Blackwell Superchip with 10 Cortex-X925 and 10 Cortex-A725 cores, 128 GB unified memory). The benchmarks were pinned to 5 Cortex-X925 cores (3.9 GHz) and are single-threaded. The disk was not used during the benchmarks (all data was in memory).

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

!!! tip "How much faster is Jelly-RDF 1.2 than 1.1?"
    
    See the [dedicated Jelly-RDF 1.1 vs 1.2 comparison](rdf-1-1-vs-1-2.md) for details on the performance improvements.

## Results

### Throughput

--8<-- "snippets/performance/a-overview-rdf.html"

Throughput, geometric mean over 13 datasets (10 for RDF/JSON and RDF/XML, which don't support quads). Log scale.
{ .jc-caption }

<div class="jelly-chart-notes" markdown>

- \* buffering writer: drops duplicate statements (write throughput still counts every input statement)
- ° RDF4J's writer is given an OutputStream and writes it one character at a time. With a BufferedWriter it could be 1.28–1.56× faster

</div>

--8<-- "snippets/performance/a-overview-rdf.data.html"

### Throughput and serialized size

--8<-- "snippets/performance/b-speed-size-rdf-triples.html"

Serialized size (uncompressed) against throughput, geometric mean over 10 datasets. Log scale. Top left is better.
{ .jc-caption }

<div class="jelly-chart-notes" markdown>

- \* buffering writer: drops duplicate statements (write throughput still counts every input statement)
- ° RDF4J's writer is given an OutputStream and writes it one character at a time. With a BufferedWriter it could be 1.28–1.56× faster

</div>

--8<-- "snippets/performance/b-speed-size-rdf-triples.data.html"

### Throughput per dataset

--8<-- "snippets/performance/c-heatmap-rdf.html"

Throughput on each dataset, in statements/s. The last 3 datasets contain quads.
{ .jc-caption }

<div class="jelly-chart-notes" markdown>

- \* buffering writer: drops duplicate statements (write throughput still counts every input statement)
- § the 3 sweeps differ by more than 10%
- ° RDF4J's writer is given an OutputStream and writes it one character at a time. With a BufferedWriter it could be 1.28–1.56× faster

</div>

--8<-- "snippets/performance/c-heatmap-rdf.data.html"

--8<-- "snippets/performance/d-spread-rdf-triples.html"

Throughput on each dataset (dots) and the geometric mean over 10 datasets (bar). Log scale.
{ .jc-caption }

<div class="jelly-chart-notes" markdown>

- \* buffering writer: drops duplicate statements (write throughput still counts every input statement)
- § the 3 sweeps differ by more than 10%
- ° RDF4J's writer is given an OutputStream and writes it one character at a time. With a BufferedWriter it could be 1.28–1.56× faster

</div>

--8<-- "snippets/performance/d-spread-rdf-triples.data.html"

### Serialized size

--8<-- "snippets/performance/f-size-rdf-triples.html"

Serialized size in bytes/statement, uncompressed and with zstd, geometric mean over 10 datasets. Log scale.
{ .jc-caption }

<div class="jelly-chart-notes" markdown>

- \* buffering writer: drops duplicate statements (write throughput still counts every input statement)

</div>

--8<-- "snippets/performance/f-size-rdf-triples.data.html"

## See also

- [Jelly-SPARQL benchmarks](sparql.md)
- [Benchmark code](https://github.com/Jelly-RDF/jelly-jvm/tree/main/jmh)
- [RiverBench benchmark suite](https://w3id.org/riverbench/)
- [Jelly-JVM]({{ jvm_link() }}) – the Jelly implementation used in the benchmarks
- [User guide](../user-guide.md)
