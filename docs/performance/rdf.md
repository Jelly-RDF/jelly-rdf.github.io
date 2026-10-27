# Jelly-RDF benchmarks

The following results were obtained by benchmarking [Jelly-JVM]({{ jvm_link() }}) 4.0.0 against the RDF serialization formats built into Apache Jena and Eclipse RDF4J, and [pyjelly]({{ python_link() }}) 0.9.0 against the formats built into RDFLib. For SPARQL query results, see [Jelly-SPARQL benchmarks](sparql.md).

The benchmarks were performed on flat streams of RDF triples or quads.

The charts are interactive – hover over them for details.

**Jump to:**

- **[Jelly-JVM](#jelly-jvm)** – Apache Jena and Eclipse RDF4J
- **[pyjelly](#pyjelly)** – RDFLib

## Jelly-JVM

### Benchmark setup

All benchmarks were performed on the first 100,000 statements of each dataset in [RiverBench](https://w3id.org/riverbench/v/dev) (development version, October 2026), except `yago-annotated-facts`, which uses RDF-star. Out of the 13 used datasets, 3 include RDF quads (`assist-iot-weather-graphs`, `citypulse-traffic-graphs`, `nanopubs`).

- Each method/dataset combination was run in 3 separate JVM forks (sweeps), each with 5 × 1 s warmup and 5 × 1 s measurement. The result for a dataset is the median of the 3 sweeps.
- Serialization: the data was preloaded into memory and serialized to a null output stream.
- Deserialization: the data was deserialized from a byte array input stream in memory. The deserializer was emitting only a stream of triples/quads, without any further processing.
- All parsers and writers were configured to skip optional work that can be turned off in the library: IRI, language tag, and datatype validation, blank node relabeling, and pretty-printing. Writers that use prefixes were given the prefixes of the dataset.
- Averages are geometric means over the datasets.

Hardware: NVIDIA DGX Spark (GB10 Grace Blackwell Superchip with 10 Cortex-X925 and 10 Cortex-A725 cores, 128 GB unified memory). The benchmarks were pinned to 5 Cortex-X925 cores (3.9 GHz) and are single-threaded. The disk was not used during the benchmarks (all data was in memory).

Software: Linux kernel 6.17, GraalVM CE 25.4 (Java 25.0.4), Apache Jena 6.2.0, Eclipse RDF4J 6.1.0, [Jelly-JVM]({{ jvm_link() }}) 4.0.0.

#### Tested methods

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

### Results

#### Throughput

--8<-- "snippets/performance/a-overview-rdf.html"

Throughput, geometric mean over 13 datasets (10 for RDF/JSON and RDF/XML, which don't support quads). Log scale.
{ .jc-caption }

<div class="jelly-chart-notes" markdown>

- \* buffering writer: deduplicates statements (write throughput still counts every input statement)
- ° RDF4J's writer is given an OutputStream and writes it one character at a time. With a BufferedWriter it could be 1.28–1.56× faster

</div>

--8<-- "snippets/performance/a-overview-rdf.data.html"

#### Throughput and serialized size

--8<-- "snippets/performance/b-speed-size-rdf-triples.html"

Serialized size (uncompressed) against throughput, geometric mean over 10 datasets. Log scale. Top left is better.
{ .jc-caption }

<div class="jelly-chart-notes" markdown>

- \* buffering writer: deduplicates statements (write throughput still counts every input statement)
- ° RDF4J's writer is given an OutputStream and writes it one character at a time. With a BufferedWriter it could be 1.28–1.56× faster

</div>

--8<-- "snippets/performance/b-speed-size-rdf-triples.data.html"

#### Throughput per dataset

--8<-- "snippets/performance/c-heatmap-rdf.html"

Throughput on each dataset, in statements/s. The last 3 datasets contain quads.
{ .jc-caption }

<div class="jelly-chart-notes" markdown>

- \* buffering writer: deduplicates statements (write throughput still counts every input statement)
- § the 3 sweeps differ by more than 10%
- ° RDF4J's writer is given an OutputStream and writes it one character at a time. With a BufferedWriter it could be 1.28–1.56× faster

</div>

--8<-- "snippets/performance/c-heatmap-rdf.data.html"

--8<-- "snippets/performance/d-spread-rdf-triples.html"

Throughput on each dataset (dots) and the geometric mean over 10 datasets (bar). Log scale.
{ .jc-caption }

<div class="jelly-chart-notes" markdown>

- \* buffering writer: deduplicates statements (write throughput still counts every input statement)
- § the 3 sweeps differ by more than 10%
- ° RDF4J's writer is given an OutputStream and writes it one character at a time. With a BufferedWriter it could be 1.28–1.56× faster

</div>

--8<-- "snippets/performance/d-spread-rdf-triples.data.html"

#### Serialized size

--8<-- "snippets/performance/f-size-rdf-triples.html"

Serialized size in bytes/statement, uncompressed and with zstd, geometric mean over 10 datasets. Log scale.
{ .jc-caption }

<div class="jelly-chart-notes" markdown>

- \* buffering writer: deduplicates statements (write throughput still counts every input statement)

</div>

--8<-- "snippets/performance/f-size-rdf-triples.data.html"

## pyjelly

### Benchmark setup

The same 13 datasets (first 100,000 statements of each) and the same hardware were used as for [Jelly-JVM](#benchmark-setup).

- Each method/dataset combination was run in 3 separate Python processes (sweeps), each with 1 × 1 s warmup and 5 × 1 s measurement. The result for a dataset is the median of the 3 sweeps.
- Serialization: the data was preloaded into memory as a list of RDFLib terms and serialized to a null output stream. RDFLib can write Turtle, RDF/XML, and JSON-LD only from a whole `Graph` or `Dataset`, so for these formats the graph was built beforehand, and only `serialize` was measured.
- Deserialization: the data was parsed from bytes in memory. Only the parsed statements were counted in the throughput numbers.
- Writers were given the prefixes of the dataset.
- Averages are geometric means over the datasets.

Hardware: the same NVIDIA DGX Spark, pinned to 5 Cortex-X925 cores. The benchmarks are single-threaded.

Software: Linux kernel 6.17, CPython 3.15.1, RDFLib 7.6.0, protobuf 7.36.2 (upb backend), [pyjelly]({{ python_link() }}) 0.9.0 (compiled with mypyc).

#### Tested methods

- W3C N-Triples / N-Quads (RDFLib's serializer, run line by line over the list of statements)
- W3C Turtle / TriG (RDFLib)
- W3C RDF/XML (RDFLib) – triples only. RDFLib can't parse its own RDF/XML for 4 of the datasets, so there are results for 6 datasets.
- W3C JSON-LD (RDFLib)
- Jelly (pyjelly 0.9.0, Jelly-RDF 1.2, "big" preset), with pyjelly's streaming API (`flat_stream_to_file` and `parse_jelly_flat`)
    ```protobuf
    max_name_table_size = 4000;
    max_prefix_table_size = 150;
    max_datatype_table_size = 32;
    ```
- Jelly (Graph API) – the same, through RDFLib's plugin API (`Graph.serialize(format="jelly")` and `Graph.parse(format="jelly")`)

RDFLib changes some literals when parsing them (e.g., `"73"^^xsd:float` is parsed as `"73.0"`), so N-Triples, Turtle, RDF/XML, and JSON-LD don't round-trip exactly on 7 of the 13 datasets. These results are still included. Jelly round-trips exactly on all datasets.

### Results

#### Throughput

--8<-- "snippets/performance/py-a-overview-rdf.html"

Throughput, geometric mean over 13 datasets (6 for RDF/XML). Log scale.
{ .jc-caption }

<div class="jelly-chart-notes" markdown>

- \* writes from an RDFLib `Graph`, which deduplicates statements (throughput counts only the statements written)

</div>

--8<-- "snippets/performance/py-a-overview-rdf.data.html"

#### Throughput and serialized size

--8<-- "snippets/performance/py-b-speed-size-rdf-triples.html"

Serialized size (uncompressed) against throughput, geometric mean over 10 datasets (6 for RDF/XML). Log scale. Top left is better.
{ .jc-caption }

<div class="jelly-chart-notes" markdown>

- \* writes from an RDFLib `Graph`, which deduplicates statements (throughput counts only the statements written)

</div>

--8<-- "snippets/performance/py-b-speed-size-rdf-triples.data.html"

#### Throughput per dataset

--8<-- "snippets/performance/py-c-heatmap-rdf.html"

Throughput on each dataset, in statements/s. The last 3 datasets contain quads.
{ .jc-caption }

<div class="jelly-chart-notes" markdown>

- \* writes from an RDFLib `Graph`, which deduplicates statements (throughput counts only the statements written)

</div>

--8<-- "snippets/performance/py-c-heatmap-rdf.data.html"

--8<-- "snippets/performance/py-d-spread-rdf-triples.html"

Throughput on each dataset (dots) and the geometric mean over 10 datasets (bar; 6 for RDF/XML). Log scale.
{ .jc-caption }

<div class="jelly-chart-notes" markdown>

- \* writes from an RDFLib `Graph`, which deduplicates statements (throughput counts only the statements written)

</div>

--8<-- "snippets/performance/py-d-spread-rdf-triples.data.html"

#### Serialized size

--8<-- "snippets/performance/py-f-size-rdf-triples.html"

Serialized size in bytes/statement, uncompressed and with zstd, geometric mean over 10 datasets (6 for RDF/XML). Log scale.
{ .jc-caption }

<div class="jelly-chart-notes" markdown>

- \* writes from an RDFLib `Graph`, which deduplicates statements (throughput counts only the statements written)

</div>

--8<-- "snippets/performance/py-f-size-rdf-triples.data.html"

## See also

- [Jelly-SPARQL benchmarks](sparql.md)
- [Jelly-JVM benchmark code](https://github.com/Jelly-RDF/jelly-jvm/tree/main/jmh)
- [RiverBench benchmark suite](https://w3id.org/riverbench/)
- [Jelly-JVM]({{ jvm_link() }}) – the Jelly implementation used in the benchmarks
- [User guide](../user-guide.md)
- [pyjelly benchmark code](https://github.com/Jelly-RDF/pyjelly/tree/main/benchmarks)
- [pyjelly]({{ python_link() }}) – the Jelly implementation for Python
