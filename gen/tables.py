"""Render CSV rows to GitHub-flavored Markdown tables (searchable, and
sortable client-side via tablesort added in mkdocs.yml)."""


def _esc(v):
    return (str(v) if v is not None else "").replace("|", "\\|").replace("\n", " ").strip()


def md_table(rows, columns=None, headers=None):
    """rows: list of dicts. columns: ordered keys to show (default: all keys of row 0).
    headers: optional display names aligned with columns."""
    if not rows:
        return "_No rows._\n"
    if columns is None:
        columns = list(rows[0].keys())
    if headers is None:
        headers = columns
    out = ["| " + " | ".join(_esc(h) for h in headers) + " |",
           "| " + " | ".join("---" for _ in columns) + " |"]
    for r in rows:
        out.append("| " + " | ".join(_esc(r.get(c, "")) for c in columns) + " |")
    return "\n".join(out) + "\n"
