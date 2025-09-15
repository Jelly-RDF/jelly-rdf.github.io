from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from collections import defaultdict, Counter
from pathlib import Path
from urllib.parse import urlparse, unquote

from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS

OUTPUT_MD = Path("docs/conformance/tests.md")
PROTOBUF_REPO = "https://github.com/Jelly-RDF/jelly-protobuf.git"
BRANCH = "main"
FROM_MANIFEST_REL = Path("test/rdf/from_jelly/manifest.ttl")
TO_MANIFEST_REL   = Path("test/rdf/to_jelly/manifest.ttl")

MF = Namespace("http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#")
EXTS = (".nt", ".nq", ".jelly", ".ttl")

def run(cmd, cwd=None):
    return subprocess.check_output(cmd, cwd=cwd, text=True).strip()

def shallow_clone(repo_url: str, branch: str, dst: Path) -> str:
    run(["git", "init"], cwd=dst)
    run(["git", "remote", "add", "origin", repo_url], cwd=dst)
    run(["git", "fetch", "--depth=1", "origin", branch], cwd=dst)
    run(["git", "checkout", branch], cwd=dst)
    return run(["git", "rev-parse", "HEAD"], cwd=dst)

def rdf_list(g: Graph, head):
    items = []
    node = head
    while node and node != RDF.nil:
        first = g.value(node, RDF.first)
        if first: items.append(first)
        node = g.value(node, RDF.rest)
    return items

def norm_repo_rel(raw_val, manifest_path: Path, repo_root: Path) -> Path | None:
    s = str(raw_val).strip()
    if s.startswith(("http://", "https://")):
        u = urlparse(s); path = unquote(u.path or "")
        parts = [p for p in path.split("/") if p]
        if "tests" in parts:
            i = parts.index("tests")
            rel = Path("test", *parts[i+1:])
            return rel
        if "test" in parts:
            i = parts.index("test")
            rel = Path(*parts[i:])
            return rel
        return None
    if "/" not in s and not s.lower().endswith(EXTS):
        return None
    p = Path(s)
    if not p.is_absolute():
        p = (manifest_path.parent / p).resolve()
    try:
        rel = p.relative_to(repo_root)
    except Exception:
        parts = list(p.parts)
        if "test" in parts:
            rel = Path(*parts[parts.index("test"):])
        else:
            return None
    return rel if rel.parts and rel.parts[0] == "test" else None

def parse_manifest(manifest_path: Path):
    g = Graph(); g.parse(manifest_path, format="turtle")
    repo_root = manifest_path.parents[3]
    entries = []
    for m in g.subjects(RDF.type, MF.Manifest):
        lst = g.value(m, MF.entries)
        if lst: entries.extend(rdf_list(g, lst))

    def collect_paths(node):
        out = set()
        rel = norm_repo_rel(node, manifest_path, repo_root)
        if rel: out.add(rel)
        for _,__,val in g.triples((node, None, None)):
            rel = norm_repo_rel(val, manifest_path, repo_root)
            if rel: out.add(rel)
        return sorted(out)

    tests = []
    for t in entries:
        name    = str(g.value(t, MF.name) or "").strip()
        comment = str(g.value(t, RDFS.comment) or "").strip()

        types = {str(o) for o in g.objects(t, RDF.type)}
        if any("Negative" in x or x.endswith("#NegativeEvaluationTest") for x in types):
            ttype = "negative"
        else:
            ttype = "positive" if any("Positive" in x for x in types) else "positive"

        actions, results = [], []
        for _,__,act in g.triples((t, MF.action, None)):
            actions += collect_paths(act)
        for _,__,res in g.triples((t, MF.result, None)):
            results += collect_paths(res)

        def detect_category(paths):
            for p in paths:
                parts = p.parts
                if "from_jelly" in parts:
                    i = parts.index("from_jelly"); return parts[i+1] if i+1 < len(parts) else "uncategorized"
                if "to_jelly" in parts:
                    i = parts.index("to_jelly");   return parts[i+1] if i+1 < len(parts) else "uncategorized"
            return "uncategorized"

        tests.append(dict(
            name=name, comment=comment, type=ttype,
            actions=actions, results=results,
            category=detect_category(actions or results),
        ))
    return tests

def detect_data(paths):
    exts = {p.suffix.lower() for p in paths}
    if ".nt" in exts: return "triples"
    if ".nq" in exts: return "quads"
    for p in paths:
        if "graphs" in p.parts: return "graphs"
    return "—"

def short_sentence(text: str, limit: int = 160) -> str:
    t = " ".join((text or "").split())
    if not t: return "—"
    p = t.find(". ")
    if 0 < p <= limit: return t[:p+1]
    return t if len(t) <= limit else t[:limit].rstrip() + "…"

def md(s: str) -> str:
    return (s or "").replace("|", r"\|").replace("\n", " ").strip()

def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+","-", (s or "").lower()).strip("-") or "section"

def gh(repo_https: str, sha: str, rel_path: Path) -> str:
    return f"{repo_https.rstrip('.git')}/blob/{sha}/{rel_path.as_posix()}"

def render_tables(cases, repo_https, sha, is_from: bool) -> str:
    out = []
    grouped = defaultdict(lambda: defaultdict(list))
    for c in cases:
        grouped[c["category"]][c["type"]].append(c)

    cats = sorted(grouped.keys())
    out.append("### Jump to category\n\n" + "\n".join(f"- [{md(c)}](#{slug(c)})" for c in cats) + "\n\n")

    counters = {"positive":0, "negative":0}
    for cat in cats:
        pos_n = len(grouped[cat].get("positive", []))
        neg_n = len(grouped[cat].get("negative", []))
        out.append(f"### {md(cat)}\n\n*{pos_n} positive, {neg_n} negative*\n\n")
        for t in ("positive","negative"):
            rows = grouped[cat].get(t, [])
            if not rows: continue
            out.append(f"#### {t.capitalize()}\n\n")
            out.append("| Name | Description | Type | Data | Input(s) | Expected | Category |\n|---|---|---|---|---|---|---|\n")
            for c in sorted(rows, key=lambda r: (r["name"], r["comment"])):
                counters[t]+=1
                sname = f"{'pos' if t=='positive' else 'neg'}_{counters[t]:03d}"
                desc = md(short_sentence(c["comment"] or c["name"], 160))

                data = detect_data(c["results"] or c["actions"]) if is_from else detect_data(c["actions"] or c["results"])

                if is_from:
                    inputs = "—"
                    if c["actions"]:
                        p = c["actions"][0]; inputs = f"[{p.name}]({gh(repo_https, sha, p)})"
                    expected = "—" if not c["results"] else "<br>".join(f"[{p.name}]({gh(repo_https, sha, p)})" for p in c["results"])
                else:
                    inputs = "—" if not c["actions"] else "<br>".join(f"[{p.name}]({gh(repo_https, sha, p)})" for p in c["actions"])
                    expected = "—"
                    if c["results"]:
                        p = c["results"][0]; expected = f"[{p.name}]({gh(repo_https, sha, p)})"

                out.append(f"| {sname} | {desc} | {t} | `{data}` | {inputs} | {expected} | {md(cat)} |\n")
            out.append("\n")
    return "".join(out)

def main():
    tmp = Path(tempfile.mkdtemp(prefix="jellypb-"))
    try:
        sha = shallow_clone(PROTOBUF_REPO, BRANCH, tmp)
        from_tests = parse_manifest(tmp / FROM_MANIFEST_REL)
        to_tests   = parse_manifest(tmp / TO_MANIFEST_REL)

        def count(ts):
            return len(ts), Counter(x["type"] for x in ts)

        n_f, c_f = count(from_tests)
        n_t, c_t = count(to_tests)

        mdout = []
        mdout.append("# Protocol conformance — Tests\n\n")
        mdout.append("<style>table{table-layout:fixed;width:100%;} thead th:nth-child(1){width:110px;} thead th:nth-child(2){width:55%;} td,th{vertical-align:top;}</style>\n\n")
        mdout.append(
            "> ### How to approach these tests\n"
            "> This page lists **Jelly protocol conformance tests**. They are language-agnostic and are used by all Jelly implementations.\n"
            ">\n"
            "> Each test is defined in a manifest and includes: **Name**, **Description**, **Type** (`positive`/`negative`), **Category**, Data (`triples`/`quads`/`graphs`), **Input(s)** and **Expected**.\n"
            ">\n"
            "> **Finding the right tests:** filter by **Category** (e.g., `rdf_star`, `generalized`) and Data.\n"
            ">\n"
            "> **Validate results:**\n"
            "> ```bash\n"
            "> jelly-cli rdf validate --compare-ordered=true <your_output> <expected_output>\n"
            "> ```\n"
            "> *(see jelly-cli: https://github.com/Jelly-RDF/cli)*\n"
            ">\n"
            "> **Run locally (Python):**\n"
            "> ```bash\n"
            "> pytest tests/conformance_tests/test_rdf\n"
            "> ```\n\n"
        )
        mdout.append(f"**Manifests:** [{FROM_MANIFEST_REL}]({PROTOBUF_REPO.rstrip('.git')}/blob/{sha}/{FROM_MANIFEST_REL.as_posix()}) · [{TO_MANIFEST_REL}]({PROTOBUF_REPO.rstrip('.git')}/blob/{sha}/{TO_MANIFEST_REL.as_posix()})\n\n")
        mdout.append("### Summary\n\n")
        mdout.append(f"- **All tests:** {n_f+n_t}\n")
        mdout.append(f"- **From Jelly:** {n_f} (positive: {c_f.get('positive',0)}, negative: {c_f.get('negative',0)})\n")
        mdout.append(f"- **To Jelly:** {n_t} (positive: {c_t.get('positive',0)}, negative: {c_t.get('negative',0)})\n\n")
        mdout.append("## From Jelly (parse)\n\n")
        mdout.append(render_tables(from_tests, PROTOBUF_REPO, sha, is_from=True))
        mdout.append("## To Jelly (serialize)\n\n")
        mdout.append(render_tables(to_tests, PROTOBUF_REPO, sha, is_from=False))

        OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_MD.write_text("".join(mdout), encoding="utf-8")
        print(f"✅ Generated: {OUTPUT_MD}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
