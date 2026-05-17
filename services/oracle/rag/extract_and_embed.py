#!/usr/bin/env python3
"""
Extract PL/SQL source from Oracle ALL_SOURCE, chunk it, embed with
sentence-transformers, and store in code_chunks table.

Usage:
    python extract_and_embed.py               # all objects in PDB
    python extract_and_embed.py --owner SCOTT # only SCOTT's objects
    python extract_and_embed.py --reset       # drop + reload all chunks
"""

import argparse
import sys
import array
import oracledb
from sentence_transformers import SentenceTransformer
from config import (
    ORACLE_HOST, ORACLE_PORT, ORACLE_PDB,
    ORACLE_USER, ORACLE_PASS,
    EMBED_MODEL, CHUNK_SIZE, CHUNK_OVERLAP,
)


def fetch_sources(conn: oracledb.Connection, owner_filter: str) -> list[dict]:
    """Fetch full source text per object from ALL_SOURCE.
    Aggregates lines in Python to avoid LISTAGG's 32KB limit."""
    where = "WHERE type IN ('PACKAGE', 'PACKAGE BODY', 'PROCEDURE', 'FUNCTION', 'TRIGGER', 'TYPE')"
    params: dict = {}
    if owner_filter:
        where += " AND owner = :owner"
        params["owner"] = owner_filter.upper()

    sql = f"""
        SELECT owner, name, type, line, text
        FROM   all_source
        {where}
        ORDER BY owner, type, name, line
    """
    with conn.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()

    # Group lines in Python — no 32KB limit
    sources: dict[tuple, list[str]] = {}
    for owner, name, obj_type, _line, text in rows:
        key = (owner, name, obj_type)
        sources.setdefault(key, []).append(text or "")

    return [
        {"owner": k[0], "name": k[1], "type": k[2], "text": "".join(lines)}
        for k, lines in sources.items()
        if "".join(lines).strip()
    ]


def chunk_text(text: str, size: int, overlap: int) -> list[str]:
    """Split text into overlapping word-boundary chunks."""
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunk = " ".join(words[i : i + size])
        chunks.append(chunk)
        i += size - overlap
    return chunks


def store_chunks(conn: oracledb.Connection, model: SentenceTransformer,
                 sources: list[dict], reset: bool) -> int:
    stored = 0

    with conn.cursor() as cur:
        for src in sources:
            owner, name, obj_type, text = (
                src["owner"], src["name"], src["type"], src["text"]
            )

            if reset:
                cur.execute(
                    "DELETE FROM code_chunks WHERE source_owner=:o AND source_name=:n AND source_type=:t",
                    {"o": owner, "n": name, "t": obj_type},
                )
            else:
                cur.execute(
                    "SELECT COUNT(*) FROM code_chunks WHERE source_owner=:o AND source_name=:n AND source_type=:t",
                    {"o": owner, "n": name, "t": obj_type},
                )
                if cur.fetchone()[0] > 0:
                    continue

            chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
            if not chunks:
                continue

            embeddings = model.encode(chunks, show_progress_bar=False)

            for seq, (chunk, emb) in enumerate(zip(chunks, embeddings)):
                vec = array.array("f", emb.tolist())
                vec_var = cur.var(oracledb.DB_TYPE_VECTOR)
                vec_var.setvalue(0, vec)
                cur.execute(
                    """INSERT INTO code_chunks
                       (source_owner, source_name, source_type, chunk_seq, chunk_text, embedding)
                       VALUES (:owner, :name, :type, :seq, :text, :emb)""",
                    {
                        "owner": owner,
                        "name":  name,
                        "type":  obj_type,
                        "seq":   seq,
                        "text":  chunk,
                        "emb":   vec_var,
                    },
                )
                stored += 1

            conn.commit()
            print(f"  {obj_type:15s} {owner}.{name}: {len(chunks)} chunks")

    return stored


def main():
    parser = argparse.ArgumentParser(description="Embed Oracle PL/SQL into code_chunks")
    parser.add_argument("--owner", default="", help="Filter by schema owner")
    parser.add_argument("--reset", action="store_true", help="Delete existing chunks before reload")
    args = parser.parse_args()

    dsn = f"{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_PDB}"
    print(f"Connecting to {dsn} as {ORACLE_USER}...")
    conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASS, dsn=dsn)

    print(f"Loading embedding model: {EMBED_MODEL}")
    model = SentenceTransformer(EMBED_MODEL)

    print(f"Fetching sources (owner filter: '{args.owner or 'all'}')...")
    sources = fetch_sources(conn, args.owner)
    print(f"Found {len(sources)} objects")

    if not sources:
        print("Nothing to embed.")
        sys.exit(0)

    print("Chunking and embedding...")
    total = store_chunks(conn, model, sources, reset=args.reset)

    conn.close()
    print(f"\nDone. {total} chunks stored in code_chunks.")


if __name__ == "__main__":
    main()
