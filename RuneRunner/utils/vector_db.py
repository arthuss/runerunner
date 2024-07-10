import os
import logging
import psycopg2
from psycopg2.extras import execute_values
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect_to_db():
    return psycopg2.connect(
        dbname="vectordb",
        user="user",
        password="password",
        host="postgres",
        port="5432"
    )

def create_table_if_not_exists(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS document_vectors (
            id SERIAL PRIMARY KEY,
            filename TEXT,
            embedding vector(384)
        )
        """)
    conn.commit()

def insert_vectors(conn, vectors):
    with conn.cursor() as cur:
        execute_values(cur, """
        INSERT INTO document_vectors (filename, embedding)
        VALUES %s
        """, vectors)
    conn.commit()

def embed_and_insert_files(base_dir):
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        conn = connect_to_db()
        create_table_if_not_exists(conn)

        vectors = []
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith('.html'):
                    filename = os.path.join(root, file)
                    logger.info(f"Processing file: {filename}")
                    with open(filename, 'r', encoding='utf-8') as f:
                        content = f.read()
                    embedding = model.encode(content)
                    vectors.append((filename, embedding.tolist()))

        logger.info(f"Inserting {len(vectors)} vectors into database")
        insert_vectors(conn, vectors)
        conn.close()
        logger.info("Embedding and insertion complete")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    embed_and_insert_files('data/html_pages')