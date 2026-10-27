# Jelly-RDF 1.1 vs 1.2

Jelly-RDF 1.2 features a new column layout for stream frames, which improves throughput and reduces serialized size (see the [changes from Jelly-RDF 1.1](../specification/serialization.md#changes-from-jelly-rdf-11)). The first versions to support it are Jelly-JVM 4.0.0 and pyjelly 0.9.0. Both also include other performance improvements in the implementation itself that made Jelly-RDF 1.1 faster as well. This page compares Jelly-RDF 1.2 with Jelly-RDF 1.1, and also shows the performance improvements coming from the implementations.

The charts are interactive – hover over them for details.

**Jump to:**

- **[Jelly-JVM](#jelly-jvm)** – Apache Jena and Eclipse RDF4J
- **[pyjelly](#pyjelly)** – RDFLib

## Jelly-JVM

### Benchmark setup

The same datasets, hardware, software, and method were used as in the [Jelly-RDF benchmarks](rdf.md#benchmark-setup), with the "big" preset. Three versions were compared:

- **3.7 (Jelly-RDF 1.1)** – Jelly-JVM 3.7.3, Jelly-RDF 1.1, frame size 256
- **4.0 (Jelly-RDF 1.1)** – Jelly-JVM 4.0.0 writing Jelly-RDF 1.1, frame size 1024
- **4.0 (Jelly-RDF 1.2)** – Jelly-JVM 4.0.0, Jelly-RDF 1.2, frame size 1024

Each of the three versions was run 6 times for every dataset. The result for a dataset is the median of the 6 runs.

### Results

#### Throughput

--8<-- "snippets/performance/e-versions.html"

Step-by-step throughput improvements: the code changes in Jelly-JVM 4.0.0 (still with Jelly-RDF 1.1), and the Jelly-RDF 1.2 format. Teal: geometric mean over 13 datasets, gray: each dataset.
{ .jc-caption }

--8<-- "snippets/performance/e-versions.data.html"

--8<-- "snippets/performance/k-speed-variants.html"

Throughput on each of the 13 datasets (median of 6 runs). Log scale.
{ .jc-caption }

--8<-- "snippets/performance/k-speed-variants.data.html"

#### Serialized size

--8<-- "snippets/performance/i-size-summary.html"

Serialized size, geometric mean over 13 datasets.
{ .jc-caption }

--8<-- "snippets/performance/i-size-summary.data.html"

!!! question "Why are Jelly-RDF 1.1 files smaller on Jelly-JVM 4.0?"

    Jelly-JVM 4.0 changed the prefix and name ID assignment algorithm to favor allocating long runs of consecutive IDs, instead of spreading them randomly. This reduces the number of "noisy" IDs which helps with zstd compression, and also allows us to skip writing some prefix and name IDs thanks to delta compression. Such better-compressed files can still be read by existing Jelly-RDF 1.1 readers.

--8<-- "snippets/performance/j-size-variants.html"

Serialized size on each of the 13 datasets, uncompressed and with zstd. Sorted by how much smaller Jelly-RDF 1.2 is. Log scale.
{ .jc-caption }

--8<-- "snippets/performance/j-size-variants.data.html"

#### Throughput and serialized size

--8<-- "snippets/performance/l-speed-size-variants.html"

Size (uncompressed) against throughput on each of the 13 datasets. Each line connects a dataset's results for 3.7 (Jelly-RDF 1.1) and 4.0 (Jelly-RDF 1.2). Up and to the left is better. Log scales.
{ .jc-caption }

--8<-- "snippets/performance/l-speed-size-variants.data.html"

## pyjelly

### Benchmark setup

The same datasets, hardware, software, and method were used as in the [pyjelly Jelly-RDF benchmarks](rdf.md#pyjelly), with pyjelly's streaming API and the "big" preset. Three versions were compared:

- **0.8 (Jelly-RDF 1.0)** – pyjelly 0.8.2, Jelly-RDF 1.0, frame size 250 (its defaults)
- **0.9 (Jelly-RDF 1.1)** – pyjelly 0.9.0 writing Jelly-RDF 1.1, frame size 1024
- **0.9 (Jelly-RDF 1.2)** – pyjelly 0.9.0, Jelly-RDF 1.2, frame size 1024

Each of the three versions was run 6 times for every dataset. The result for a dataset is the median of the 6 runs.

### Results

#### Throughput

--8<-- "snippets/performance/py-e-versions.html"

Step-by-step throughput improvements: the code changes in pyjelly 0.9.0 (with Jelly-RDF 1.1), and the Jelly-RDF 1.2 format. Teal: geometric mean over 13 datasets, gray: each dataset.
{ .jc-caption }

--8<-- "snippets/performance/py-e-versions.data.html"

--8<-- "snippets/performance/py-k-speed-variants.html"

Throughput on each of the 13 datasets (median of 6 runs). Log scale.
{ .jc-caption }

--8<-- "snippets/performance/py-k-speed-variants.data.html"

#### Serialized size

--8<-- "snippets/performance/py-i-size-summary.html"

Serialized size, geometric mean over 13 datasets.
{ .jc-caption }

--8<-- "snippets/performance/py-i-size-summary.data.html"

--8<-- "snippets/performance/py-j-size-variants.html"

Serialized size on each of the 13 datasets, uncompressed and with zstd. Sorted by how much smaller Jelly-RDF 1.2 is. Log scale.
{ .jc-caption }

--8<-- "snippets/performance/py-j-size-variants.data.html"

#### Throughput and serialized size

--8<-- "snippets/performance/py-l-speed-size-variants.html"

Size (uncompressed) against throughput on each of the 13 datasets. Each line connects a dataset's results for 0.8 (Jelly-RDF 1.0) and 0.9 (Jelly-RDF 1.2). Up and to the left is better. Log scales.
{ .jc-caption }

--8<-- "snippets/performance/py-l-speed-size-variants.data.html"

## See also

- [Jelly-RDF benchmarks](rdf.md)
- [Jelly-RDF 1.2 specification](../specification/serialization.md)
- [Jelly-JVM benchmark code](https://github.com/Jelly-RDF/jelly-jvm/tree/main/jmh)
- [pyjelly benchmark code](https://github.com/Jelly-RDF/pyjelly/tree/main/benchmarks)
