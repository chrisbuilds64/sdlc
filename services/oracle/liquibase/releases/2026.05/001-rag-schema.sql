--liquibase formatted sql

-- changeset christian:2026.05-001-code-chunks
-- comment: RAG infrastructure — PL/SQL code chunks with vector embeddings (384-dim all-MiniLM-L6-v2)
-- runOnChange: false
CREATE TABLE code_chunks (
    id              NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_owner    VARCHAR2(128)    NOT NULL,
    source_name     VARCHAR2(128)    NOT NULL,
    source_type     VARCHAR2(32)     NOT NULL,
    chunk_seq       NUMBER           NOT NULL,
    chunk_text      CLOB             NOT NULL,
    embedding       VECTOR(384, FLOAT32),
    indexed_at      TIMESTAMP        DEFAULT SYSTIMESTAMP NOT NULL,
    CONSTRAINT uq_chunk UNIQUE (source_owner, source_name, source_type, chunk_seq)
) TABLESPACE sdlc_data;

COMMENT ON TABLE  code_chunks                IS 'PL/SQL source chunks with vector embeddings for RAG similarity search';
COMMENT ON COLUMN code_chunks.source_owner   IS 'Schema owner from ALL_SOURCE';
COMMENT ON COLUMN code_chunks.source_name    IS 'Object name from ALL_SOURCE';
COMMENT ON COLUMN code_chunks.source_type    IS 'PACKAGE, PROCEDURE, FUNCTION, TRIGGER, etc.';
COMMENT ON COLUMN code_chunks.chunk_seq      IS 'Chunk sequence within the object (0-based)';
COMMENT ON COLUMN code_chunks.chunk_text     IS 'Raw text of the chunk (up to ~512 tokens)';
COMMENT ON COLUMN code_chunks.embedding      IS '384-dim float32 vector from all-MiniLM-L6-v2';

-- rollback DROP TABLE code_chunks;

-- changeset christian:2026.05-002-rag-questions-log
-- comment: Query log — track what was asked and which chunks were returned
-- runOnChange: false
CREATE TABLE rag_query_log (
    id              NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    question        VARCHAR2(2000)   NOT NULL,
    top_chunk_ids   VARCHAR2(200),
    llm_model       VARCHAR2(100),
    asked_at        TIMESTAMP        DEFAULT SYSTIMESTAMP NOT NULL
);

-- rollback DROP TABLE rag_query_log;
