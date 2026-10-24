# Jelly-SPARQL benchmarks

The following results were obtained by benchmarking [Jelly-JVM]({{ jvm_link() }}) 4.0.0 against the SPARQL query results formats built into Apache Jena and Eclipse RDF4J. For RDF serialization, see [Jelly-RDF benchmarks](rdf.md).

The charts are interactive – hover over them for details.

## Benchmark setup

The same datasets, hardware, software, and method were used as in the [Jelly-RDF benchmarks](rdf.md#benchmark-setup). Each of the 13 datasets was turned into a single SPARQL result set with one row per statement. Throughput is given in cells (bound values) per second.

### Tested methods

- [SPARQL Query Results XML Format](https://www.w3.org/TR/rdf-sparql-XMLres/) (SRX) (Apache Jena, Eclipse RDF4J)
- [SPARQL Query Results JSON Format](https://www.w3.org/TR/sparql11-results-json/) (SRJ) (Apache Jena, Eclipse RDF4J)
- [SPARQL Query Results TSV Format](https://www.w3.org/TR/sparql11-results-csv-tsv/) (Apache Jena, Eclipse RDF4J)
    - CSV was not tested, because it does not preserve datatypes or language tags.
- Jena's binary result formats, Protobuf and Thrift (Apache Jena)
- RDF4J Binary query results format (Eclipse RDF4J)
- Jelly-SPARQL (Jelly-JVM 4.0.0, "big" preset)
    ```protobuf
    max_name_table_size = 8192;
    max_prefix_table_size = 1024;
    max_datatype_table_size = 64;
    ```

## Results

### Throughput

--8<-- "snippets/performance/a-overview-sparql.html"

Throughput, geometric mean over 10 datasets. Log scale.
{ .jc-caption }

<div class="jelly-chart-notes" markdown>

- ‡ RDF4J's TSV parser runs on a thread pool, so this uses more than one core

</div>

--8<-- "snippets/performance/a-overview-sparql.data.html"

### Throughput and serialized size

--8<-- "snippets/performance/b-speed-size-sparql.html"

Serialized size (uncompressed) against throughput, geometric mean over 10 datasets. Log scale. Top left is better.
{ .jc-caption }

<div class="jelly-chart-notes" markdown>

- ‡ RDF4J's TSV parser runs on a thread pool, so this uses more than one core

</div>

--8<-- "snippets/performance/b-speed-size-sparql.data.html"

### Throughput per dataset

--8<-- "snippets/performance/c-heatmap-sparql.html"

Throughput on each dataset, in cells/s.
{ .jc-caption }

<div class="jelly-chart-notes" markdown>

- † not lossless on this dataset; left out of averages
- ‡ RDF4J's TSV parser runs on a thread pool, so this uses more than one core
- § the 3 sweeps differ by more than 10%

</div>

--8<-- "snippets/performance/c-heatmap-sparql.data.html"

--8<-- "snippets/performance/d-spread-sparql.html"

Throughput on each dataset (dots) and the geometric mean over 10 datasets (bar). Log scale. Hollow dots: not lossless, left out of the mean.
{ .jc-caption }

<div class="jelly-chart-notes" markdown>

- † not lossless on this dataset; left out of averages
- ‡ RDF4J's TSV parser runs on a thread pool, so this uses more than one core
- § the 3 sweeps differ by more than 10%

</div>

--8<-- "snippets/performance/d-spread-sparql.data.html"

### Serialized size

--8<-- "snippets/performance/f-size-sparql.html"

Serialized size in bytes/row, uncompressed and with zstd, geometric mean over 10 datasets. Log scale.
{ .jc-caption }

--8<-- "snippets/performance/f-size-sparql.data.html"

## See also

- [Jelly-RDF benchmarks](rdf.md)
- [Jelly-SPARQL specification](../specification/sparql.md)
- [Benchmark code](https://github.com/Jelly-RDF/jelly-jvm/tree/main/jmh)
- [RiverBench benchmark suite](https://w3id.org/riverbench/)
- [Jelly-JVM]({{ jvm_link() }}) – the Jelly implementation used in the benchmarks
