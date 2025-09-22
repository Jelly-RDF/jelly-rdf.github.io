from pathlib import Path
from collections import OrderedDict
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, FOAF, DCTERMS

EARL = Namespace("http://www.w3.org/ns/earl#")
DOAP = Namespace("http://usefulinc.com/ns/doap#")


def _load_graph(path: Path) -> Graph:
    g = Graph()
    g.parse(path.as_posix(), format="turtle")
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
        out[str(test)] = token
    return out


def _short_id(uri: str) -> str:
    parts = uri.rstrip("/").split("/")
    return parts[-1] if parts else uri


def _category_of(uri: str) -> str:
    parts = uri.rstrip("/").split("/")
    return parts[-2] if len(parts) >= 2 else ""


def _format_outcome(token: str) -> str:
    token = (token or "").lower()
    if token == "passed":
        return '<span style="color:green;font-weight:bold">PASS</span>'
    elif token == "failed":
        return '<span style="color:red;font-weight:bold">FAILED</span>'
    elif token == "inapplicable":
        return "INAPPLICABLE"
    elif token == "cantTell":
        return "CANTTELL"
    elif token == "untested":
        return "UNTESTED"
    return ""


def _format_outcome(token: str) -> str:
    token = (token or "").lower()
    if token == "passed":
        return '<div align="center"><span style="color:green;font-weight:bold">PASS</span></div>'
    elif token == "failed":
        return '<div align="center"><span style="color:red;font-weight:bold">FAILED</span></div>'
    elif token == "inapplicable":
        return '<div align="center">INAPPLICABLE</div>'
    elif token == "cantTell":
        return '<div align="center">CANTTELL</div>'
    elif token == "untested":
        return '<div align="center">UNTESTED</div>'
    return '<div align="center"></div>'


def _render_matrix_md(
    matrix: "OrderedDict[str, dict[str, str]]",
    impl_labels: "OrderedDict[str, str]",
) -> str:
    impl_keys = list(impl_labels.keys())

    header = "| Test | Category | " + " | ".join(impl_labels.values()) + " |"
    sep = "|" + "---|" * (2 + len(impl_keys))

    # Compute pass percentages for summary row
    def percent_for(k: str):
        total = len(
            [
                o
                for o in matrix.values()
                if k in o and o[k] not in ("inapplicable", "untested")
            ]
        )
        passed = len([o for o in matrix.values() if k in o and o[k] == "passed"])
        pct = (passed / total * 100.0) if total else 0.0
        return f'<div align="center"><b>{pct:.1f}% PASS</b></div>'

    rows = []
    for test_uri, impl_map in matrix.items():
        cat = _category_of(test_uri)
        link = f"[{_short_id(test_uri)}]({test_uri})"
        cells = []
        for k in impl_keys:
            token = impl_map.get(k, "")
            cells.append(_format_outcome(token))
        rows.append("| " + " | ".join([link, cat] + cells) + " |")

    summary = (
        "| **Percentage passed:** |  | "
        + " | ".join(percent_for(k) for k in impl_keys)
        + " |"
    )

    md = []
    md.append(header)
    md.append(sep)
    md.extend(rows)
    md.append(summary)
    return "\n".join(md)


def _render_reports_section_md(
    graphs: dict[Path, Graph], outcomes: dict[str, dict[str, str]]
) -> str:
    lines = ["## Available Reports", ""]
    for path, g in graphs.items():
        # Implementation information
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

        # Assertor information
        as_name = as_home = ""
        for subj in g.subjects(RDF.type, EARL.Assertor):
            as_name = str(g.value(subj, FOAF.name) or "")
            as_home = str(g.value(subj, FOAF.homepage) or "")
            break

        # Report date information
        issued = g.value(None, DCTERMS.issued)
        issued_str = str(issued) if issued else ""

        # Compliance information
        impl_key = (impl_name + " " + rev).strip()
        outmap = outcomes.get(impl_key, {})
        total = len(
            [o for o in outmap.values() if o not in ("inapplicable", "untested")]
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

    def _sort_key(u: str):
        sid = _short_id(u)
        sid = sid.zfill(8) if sid.isdigit() else sid
        return (_category_of(u), sid)

    tests_sorted = sorted(test_set, key=_sort_key)

    matrix = OrderedDict()
    for t in tests_sorted:
        row = {}
        for ik, outmap in per_impl_outcomes.items():
            if t in outmap:
                row[ik] = outmap[t]
        matrix[t] = row

    matrix_md = _render_matrix_md(matrix, impl_labels)
    reports_md = _render_reports_section_md(graphs, per_impl_outcomes)

    return "## Turtle tests\n\n" + matrix_md + "\n\n" + reports_md
