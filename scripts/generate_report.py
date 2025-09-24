from pathlib import Path
from collections import OrderedDict
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, FOAF, DCTERMS

EARL = Namespace("http://www.w3.org/ns/earl#")
DOAP = Namespace("http://usefulinc.com/ns/doap#")


def _load_graph(path: Path) -> Graph:
    g = Graph()
    g.parse(path, format="turtle")
    return g


def _impl_key_label(g: Graph) -> tuple[str, str]:
    name, ver = "", ""
    for subj in g.subjects(RDF.type, DOAP.Project):
        n = g.value(subj, DOAP.name)
        if n:
            name = str(n)
        rel = g.value(subj, DOAP.release)
        if rel:
            rev = g.value(rel, DOAP.revision)
            if rev:
                ver = str(rev)
        break
    if not name:
        name = "Implementation"
    key = (name + (" " + ver if ver else "")).strip()
    return key, key


def _read_assertions(g: Graph) -> dict[str, str]:
    out = {}
    for a in g.subjects(RDF.type, EARL.Assertion):
        test = g.value(a, EARL.test)
        if not isinstance(test, URIRef):
            continue
        res = g.value(a, EARL.result)
        token = ""
        if res:
            oc = g.value(res, EARL.outcome)
            if isinstance(oc, URIRef):
                token = str(oc).split("#")[-1]
        out[str(test)] = token.lower()
    return out


def _short_id(uri: str) -> str:
    parts = uri.rstrip("/").split("/")
    return parts[-1] if parts else uri


def _category_of(uri: str) -> str:
    parts = uri.rstrip("/").split("/")
    return parts[-2] if len(parts) >= 2 else ""


def _cell_html(token: str) -> str:
    token = (token or "").lower()
    if token == "passed":
        return '<td style="background-color:#00b8d41a;text-align:center">PASSED</td>'
    elif token == "failed":
        return '<td style="background-color:#ff17441a;text-align:center">FAILED</td>'
    elif token == "inapplicable":
        return (
            '<td style="background-color:#ff91001a;text-align:center">INAPPLICABLE</td>'
        )
    elif token == "canttell":
        return '<td style="background-color:#ff91001a;text-align:center">CANTTELL</td>'
    elif token == "untested":
        return '<td style="background-color:#ff91001a;text-align:center">UNTESTED</td>'
    return '<td style="text-align:center"></td>'


def _render_matrix_md(
    matrix: "OrderedDict[str, dict[str, str]]",
    impl_labels: "OrderedDict[str, str]",
) -> str:
    md = []
    impl_keys = list(impl_labels.keys())

    md.append("# Report table\n")

    grouped = {}
    for test_uri in matrix.keys():
        type_ = test_uri.split("/")[-3] if "/" in test_uri else "unknown"
        cat = _category_of(test_uri)
        grouped.setdefault(type_, {}).setdefault(cat, []).append(test_uri)

    for type_, cats in grouped.items():
        md.append(f"## {type_}\n")
        for cat, tests in cats.items():
            md.append(f"### {cat}\n")
            header = (
                "<table><thead><tr><th>Test</th>"
                + "".join(f"<th>{impl_labels[k]}</th>" for k in impl_keys)
                + "</tr></thead><tbody>"
            )
            rows = [header]
            totals = {k: {"passed": 0, "total": 0} for k in impl_keys}

            for test_uri in sorted(tests, key=lambda t: _short_id(t)):
                short = _short_id(test_uri)
                link = f'<td><a href="{test_uri}" target="_blank">{short}</a></td>'
                cells = []
                for k in impl_keys:
                    token = matrix[test_uri].get(k, "")
                    if token not in ("inapplicable", "untested", ""):
                        totals[k]["total"] += 1
                    if token == "passed":
                        totals[k]["passed"] += 1
                    cells.append(_cell_html(token))
                rows.append("<tr>" + link + "".join(cells) + "</tr>")

            pct_row = (
                "<tr><td><b>Percentage passed:</b></td>"
                + "".join(
                    f'<td style="text-align:center"><b>{(totals[k]["passed"] / totals[k]["total"] * 100.0 if totals[k]["total"] else 0):.1f}%</b></td>'
                    for k in impl_keys
                )
                + "</tr>"
            )

            rows.append(pct_row)
            rows.append("</tbody></table>\n")
            md.extend(rows)

    return "\n".join(md)


def _render_reports_section_md(
    graphs: dict[Path, Graph], outcomes: dict[str, dict[str, str]]
) -> str:
    lines = ["# Available reports", ""]
    lines.append(
        "This section lists all submitted implementation reports, with metadata from DOAP/FOAF, and their compliance scores."
    )
    lines.append("")
    for path, g in graphs.items():
        impl_name = impl_desc = lang = homepage = rev = ""
        dev_name = dev_home = ""
        for subj in g.subjects(RDF.type, DOAP.Project):
            impl_name = str(g.value(subj, DOAP.name) or "")
            impl_desc = str(g.value(subj, DOAP.description) or "")
            lang = str(g.value(subj, DOAP["programming-language"]) or "")
            homepage = str(g.value(subj, DOAP.homepage) or "")
            rel = g.value(subj, DOAP.release)
            if rel:
                rev = str(g.value(rel, DOAP.revision) or "")
            dev = g.value(subj, DOAP.developer)
            if dev:
                dev_name = str(g.value(dev, FOAF.name) or "")
                dev_home = str(g.value(dev, FOAF.homepage) or "")
            break

        as_name = as_home = ""
        for subj in g.subjects(RDF.type, EARL.Assertor):
            as_name = str(g.value(subj, FOAF.name) or "")
            as_home = str(g.value(subj, FOAF.homepage) or "")
            break

        issued = g.value(None, DCTERMS.issued)
        issued_str = str(issued) if issued else ""

        impl_key = (impl_name + " " + rev).strip()
        outmap = outcomes.get(impl_key, {})
        total = len(
            [o for o in outmap.values() if o not in ("inapplicable", "untested", "")]
        )
        passed = len([o for o in outmap.values() if o == "passed"])
        percent = (passed / total * 100.0) if total else 0.0
        badge = (
            f"![{passed}/{total} {percent:.1f}%](https://img.shields.io/badge/"
            f"{passed}%2F{total}-{percent:.1f}%25-{'brightgreen' if percent >= 99 else 'orange'})"
        )

        lines.append(f"### {impl_name} {rev}")
        if impl_desc:
            lines.append(f"*{impl_desc}*")
        lines.append("")
        if lang:
            lines.append(f"- **Programming Language:** {lang}")
        if homepage:
            lines.append(f"- **Home Page:** [{homepage}]({homepage})")
        if dev_name:
            if dev_home:
                lines.append(f"- **Developer:** [{dev_name}]({dev_home})")
            else:
                lines.append(f"- **Developer:** {dev_name}")
        if as_name:
            if as_home:
                lines.append(f"- **Assertor:** [{as_name}]({as_home})")
            else:
                lines.append(f"- **Assertor:** {as_name}")
        if issued_str:
            lines.append(f"- **Issued:** {issued_str}")
        lines.append(f"- **Test Suite Compliance:** {badge}")
        lines.append(f"- **Report file:** `{path.name}`")
        lines.append("")

    return "\n".join(lines)


def generate_conformance_report() -> str:
    reports_dir = Path("docs/conformance/reports")
    paths = [*reports_dir.glob("*.ttl")]

    impl_labels = OrderedDict()
    per_impl_outcomes = {}
    test_set = set()
    graphs = {}

    for p in paths:
        try:
            g = _load_graph(p)
            graphs[p] = g
        except Exception:
            continue
        key, label = _impl_key_label(g)
        impl_labels.setdefault(key, label)
        outcomes = _read_assertions(g)
        per_impl_outcomes.setdefault(key, {}).update(outcomes)
        test_set.update(outcomes.keys())

    matrix = OrderedDict()
    for t in test_set:
        row = {}
        for ik, outmap in per_impl_outcomes.items():
            if t in outmap:
                row[ik] = outmap[t]
        matrix[t] = row

    md_matrix = _render_matrix_md(matrix, impl_labels)
    md_reports = _render_reports_section_md(graphs, per_impl_outcomes)
    return md_matrix + "\n\n" + md_reports
