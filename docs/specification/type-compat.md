## RDF 1.1 interpretations

| RDF 1.1 type / Physical type | `TRIPLES` | `QUADS` | `GRAPHS` |
|:--|:-:|:-:|:-:|
| RDF graph | Continuous | ✘ | ✘ |
| RDF dataset | ✘ | Continuous | Continuous |

## RDF-STaX interpretations

| RDF STaX type / Physical type | `TRIPLES` | `QUADS` | `GRAPHS` |
|:--|:-:|:-:|:-:|
| Graph stream | Framed | ✘ | ✘ |
| Subject graph stream | Framed | ✘ | ✘ |
| Dataset stream | ✘ | Framed | Framed |
| Named graph stream | ✘ | Framed | Framed |
| Timestamped named graph stream | ✘ | Framed | Framed |
| Flat triple stream | Continuous | ✘ | ✘ |
| Flat quad stream | ✘ | Continuous | Continuous |


- triplesAsGraphStream
    - triplesToGrouped
- triplesAsFlatTripleStream
    - triplesToFlat
- quadsAsDatasetStream
    - quadsToGrouped
- quadsAsFlatQuadStream
    - quadsToFlat
- graphsAsGraphStream
- graphsAsDatasetStream
    - graphsAsQuadsToGrouped
- graphsAsFlatQuadStream
    - graphsAsQuadsToFlat


aaaa

- Quad – InterpretableAs.FlatQuadStream
    - QUADS (flatten frames)
    - GRAPHS (flatten frames and graphs)
- Seq[Quad] – InterpretableAs.DatasetStreamOfQuads
    - QUADS (by frames)
    - GRAPHS (by frames, flatten graphs)
- (Node, Seq[Triple]) – InterpretableAs.DatasetStream
    - GRAPHS (by graphs)
- Seq[(Node, Seq[Triple])] – InterpretableAs.DatasetStream
    - GRAPHS (by frames and graphs)
