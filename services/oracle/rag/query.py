#!/usr/bin/env python3
"""
Q&A CLI for Oracle PL/SQL codebase.

Usage:
    python query.py "Was macht das Package PKG_RECHNUNG?"
    python query.py --interactive
"""

import argparse
import array
import sys
import oracledb
import ollama
from sentence_transformers import SentenceTransformer
from config import (
    ORACLE_HOST, ORACLE_PORT, ORACLE_PDB,
    ORACLE_USER, ORACLE_PASS,
    EMBED_MODEL, OLLAMA_HOST, OLLAMA_MODEL, TOP_K,
)

SYSTEM_PROMPT = """You are an expert Oracle PL/SQL analyst helping developers understand
an existing codebase. You are given relevant code fragments retrieved from the database.

Answer the question based on these fragments. Be specific and reference procedure or
package names when relevant. If the fragments don't contain enough information, say so.
Keep your answer concise and practical."""


def embed_question(model: SentenceTransformer, question: str) -> array.array:
    emb = model.encode([question])[0]
    return array.array("f", emb.tolist())


def retrieve_chunks(conn: oracledb.Connection, question_vec: array.array,
                    top_k: int) -> list[dict]:
    sql = """
        SELECT source_owner, source_name, source_type, chunk_seq, chunk_text,
               VECTOR_DISTANCE(embedding, :qvec, COSINE) AS dist
        FROM   code_chunks
        ORDER  BY dist
        FETCH  FIRST :k ROWS ONLY
    """
    with conn.cursor() as cur:
        qvec = cur.var(oracledb.DB_TYPE_VECTOR)
        qvec.setvalue(0, question_vec)
        cur.execute(sql, {"qvec": qvec, "k": top_k})
        rows = cur.fetchall()

    return [
        {
            "owner":  r[0],
            "name":   r[1],
            "type":   r[2],
            "seq":    r[3],
            "text":   r[4],
            "dist":   round(r[5], 4),
        }
        for r in rows
    ]


def build_context(chunks: list[dict]) -> str:
    parts = []
    for c in chunks:
        header = f"--- {c['type']} {c['owner']}.{c['name']} (chunk {c['seq']}, similarity distance: {c['dist']}) ---"
        parts.append(f"{header}\n{c['text']}")
    return "\n\n".join(parts)


def ask_llm(question: str, context: str) -> str:
    client = ollama.Client(host=OLLAMA_HOST)
    response = client.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Code context:\n\n{context}\n\nQuestion: {question}"},
        ],
        stream=False,
    )
    return response.message.content


def answer(conn: oracledb.Connection, embed_model: SentenceTransformer,
           question: str, verbose: bool = False) -> str:
    qvec = embed_question(embed_model, question)
    chunks = retrieve_chunks(conn, qvec, TOP_K)

    if not chunks:
        return "No code chunks found in the database. Run extract_and_embed.py first."

    if verbose:
        print(f"\n[Retrieved {len(chunks)} chunks]")
        for c in chunks:
            print(f"  {c['dist']:.4f}  {c['type']} {c['owner']}.{c['name']} chunk {c['seq']}")

    context = build_context(chunks)
    return ask_llm(question, context)


def main():
    parser = argparse.ArgumentParser(description="Query your Oracle PL/SQL codebase with AI")
    parser.add_argument("question", nargs="?", help="Question to ask")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show retrieved chunks")
    args = parser.parse_args()

    if not args.question and not args.interactive:
        parser.print_help()
        sys.exit(1)

    dsn = f"{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_PDB}"
    conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASS, dsn=dsn)

    print(f"Loading embedding model: {EMBED_MODEL}...")
    embed_model = SentenceTransformer(EMBED_MODEL)
    print(f"LLM: {OLLAMA_MODEL} via {OLLAMA_HOST}\n")

    if args.interactive:
        print("Interactive mode. Type your question (or 'quit' to exit).\n")
        while True:
            try:
                question = input("Question: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nBye.")
                break
            if not question or question.lower() in ("quit", "exit", "q"):
                break
            print("\nSearching and generating answer...\n")
            result = answer(conn, embed_model, question, verbose=args.verbose)
            print(f"Answer:\n{result}\n")
            print("-" * 60)
    else:
        print(f"Question: {args.question}\n")
        print("Searching and generating answer...\n")
        result = answer(conn, embed_model, args.question, verbose=args.verbose)
        print(f"Answer:\n{result}")

    conn.close()


if __name__ == "__main__":
    main()
