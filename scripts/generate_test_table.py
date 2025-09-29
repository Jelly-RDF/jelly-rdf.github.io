from __future__ import annotations

import re
import subprocess
from collections import defaultdict, Counter
from pathlib import Path
from urllib.parse import urlparse, unquote

from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
REPO_ROOT = PROJECT_ROOT / "submodules/protobuf"
PROTOBUF_REPO = "https://github.com/Jelly-RDF/jelly-protobuf.git"
JELLY_CLI_REPO = "https://github.com/Jelly-RDF/cli"

FROM_MANIFEST = REPO_ROOT / "test/rdf/from_jelly/manifest.ttl"
TO_MANIFEST = REPO_ROOT / "test/rdf/to_jelly/manifest.ttl"

MF = Namespace("http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#")

ALLOWED_FILE_PATTERNS = (
    r"in\.jelly$", r"out\.jelly$", r"out_\d+\.(nt|nq)$",
    r".*\.(nt|nq|ttl|jelly)$"
)

def sh(cmd, cwd=None) -> str:
    return subprocess.check_output(cmd, cwd=cwd, text=True).strip()

def slug_for_mkdocs(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^a-z0-9_-]", "", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "section"

def md_text(s: str) -> str:
    return (s or "").replace("|", r"\|").replace("\n", " ").strip()

def short(s: str, limit: int = 160) -> str:
    s = (s or "").strip()
    if len(s) <= limit: return s
    cut = s[:limit].rsplit(" ", 1)[0]
    return cut + "…"

def gh_blob_url(repo_https: str, sha: str, rel_path: Path) -> str:
    return f"{repo_https.rstrip('.git')}/blob/{sha}/{rel_path.as_posix()}"

def rdf_list(g: Graph, head):
    out = []
    node = head
    while node and node != RDF.nil:
        first = g.value(node, RDF.first)
        if first is not None: out.append(first)
        node = g.value(node, RDF.rest)
    return out

def _looks_like_file_token(s: str) -> bool:
    return any(re.search(p, s) for p in ALLOWED_FILE_PATTERNS)

def norm_repo_rel(val, manifest_path: Path, repo_root: Path) -> Path | None:
    s = str(val).strip()
    if not s: return None
    if s.startswith(("http://", "https://")):
        u = urlparse(s)
        path = unquote(u.path or "")
        parts = [p for p in path.split("/") if p]
        for n in ("test", "tests"):
            if n in parts:
                i = parts.index(n)
                rel = Path(*parts[i:])
                if rel.parts[0] == "tests": rel = Path("test", *rel.parts[1:])
                return rel
        return None
    if "/" not in s and not _looks_like_file_token(s): return None
    p = Path(s)
    if not p.is_absolute(): p = (manifest_path.parent / p).resolve()
    try: rel = p.relative_to(repo_root)
    except:
        parts = list(p.parts)
        if "test" in parts: rel = Path(*parts[parts.index("test"):])
        else: return None
    return rel if rel.parts and rel.parts[0] == "test" else None

def detect_category(paths: list[Path]) -> str:
    for p in paths:
        for a in ("from_jelly","to_jelly"):
            if a in p.parts:
                i = p.parts.index(a)
                if i+1 < len(p.parts): return p.parts[i+1]
    return "uncategorized"

def parse_manifest(manifest_path: Path, repo_root: Path):
    g = Graph(); g.parse(manifest_path, format="turtle")
    entries = []
    for m in g.subjects(RDF.type, MF.Manifest):
        lst = g.value(m, MF.entries)
        if lst: entries.extend(rdf_list(g, lst))

    def collect(node):
        out=set()
        rel = norm_repo_rel(node, manifest_path, repo_root)
        if rel: out.add(rel)
        for _, __, v in g.triples((node, None, None)):
            rel = norm_repo_rel(v, manifest_path, repo_root)
            if rel: out.add(rel)
        return sorted(out)

    tests = []
    for t in entries:
        name = str(g.value(t, MF.name) or "").strip()
        desc = str(g.value(t, RDFS.comment) or "").strip()
        types = {str(o) for o in g.objects(t, RDF.type)}
        pol = "negative" if any("Negative" in x for x in types) else "positive"
        acts, ress = [], []
        for _, __, a in g.triples((t, MF.action, None)):
            nodes = rdf_list(g, a) if (a, RDF.first, None) in g else [a]
            for n in nodes:
                acts += collect(n)

        for _, __, r in g.triples((t, MF.result, None)):
            nodes = rdf_list(g, r) if (r, RDF.first, None) in g else [r]
            for n in nodes:
                ress += collect(n)
        cat = detect_category(acts or ress)
        path = norm_repo_rel(t, manifest_path, repo_root)
        tests.append(dict(
            iri=str(t),
            raw_name=name,
            description=desc,
            polarity=pol,
            path=path,
            actions=acts,
            results=ress,
            category=cat
        ))
    return tests

TABLE_HEADER = "| Name | Description | Input(s) | Expected output |\n|---|---|---|---|\n"

def files_to_links(paths: list[Path], repo_https: str, sha: str) -> str:
    if not paths: return "—"
    return "<br>".join(f"[{p.name}]({gh_blob_url(repo_https, sha, p)})" for p in paths)

def render_tables(cases: list[dict], repo_https: str, sha: str) -> str:
    out = []
    grouped = defaultdict(lambda: defaultdict(list))
    for c in cases: grouped[c["category"]][c["polarity"]].append(c)
    cats = sorted(grouped.keys())
    out.append("### Jump to category\n\n")
    for cat in cats: out.append(f"- [{md_text(cat)}](#{slug_for_mkdocs(cat)})\n")
    out.append("\n")
    for cat in cats:
        pos = len(grouped[cat].get("positive", []))
        neg = len(grouped[cat].get("negative", []))
        out.append(f"### {md_text(cat)}\n\n*{pos} positive, {neg} negative*\n\n")
        for pol in ("positive", "negative"):
            rows = grouped[cat].get(pol, [])
            if not rows: continue
            out.append(f"#### {pol.capitalize()}\n\n{TABLE_HEADER}")
            for r in sorted(rows, key=lambda x: (x["iri"])):
                desc = md_text(r["raw_name"] + " " + r["description"])
                inputs = files_to_links(r["actions"], repo_https, sha)
                expected = files_to_links(r["results"], repo_https, sha)
                id = files_to_links([r["path"]], repo_https, sha)
                out.append(f"| {id} | {desc} | {inputs} | {expected} |\n")
            out.append("\n")
    return "".join(out)

def generate_test_table():
    try:
        sha = sh(["git","rev-parse","HEAD"],cwd=REPO_ROOT)
    except Exception as e:
        print(f"Warning: Could not get git SHA for protobuf submodule. Error: {e}")
        sha = "main"

    from_tests = parse_manifest(FROM_MANIFEST, REPO_ROOT)
    to_tests = parse_manifest(TO_MANIFEST, REPO_ROOT)

    def stats(ts):
        c=Counter(x["polarity"] for x in ts)
        return len(ts),c.get("positive",0),c.get("negative",0)
    nf,pf,nfneg = stats(from_tests)
    nt,pt,ntneg = stats(to_tests)
    md = []
    md.append(
        "<style>"
        "table{table-layout:fixed;width:100%;}"
        "thead th:nth-child(1){width:120px;}"
        "thead th:nth-child(2){width:9999px;}"
        "thead th:nth-child(3),thead th:nth-child(4),thead th:nth-child(5){width:1%;}"
        "td,th{vertical-align:top;}"
        "</style>\n\n"
    )
    md.append(
        "**Manifests used to generate this page:** "
        f"[from_jelly]({PROTOBUF_REPO.rstrip('.git')}/blob/{sha}/{FROM_MANIFEST.relative_to(REPO_ROOT).as_posix()}) · "
        f"[to_jelly]({PROTOBUF_REPO.rstrip('.git')}/blob/{sha}/{TO_MANIFEST.relative_to(REPO_ROOT).as_posix()})\n\n"
    )
    md.append(f"- **All tests:** {nf+nt}\n")
    md.append(f"- **From Jelly:** {nf} (positive: {pf}, negative: {nfneg})\n")
    md.append(f"- **To Jelly:** {nt} (positive: {pt}, negative: {ntneg})\n\n")
    md.append("## From Jelly (parse)\n\n")
    md.append(render_tables(from_tests, PROTOBUF_REPO, sha))
    md.append("## To Jelly (serialize)\n\n")
    md.append(render_tables(to_tests, PROTOBUF_REPO, sha))

    return "".join(md)