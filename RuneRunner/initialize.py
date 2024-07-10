import subprocess
import asyncio
import sys
import os

# Fügen Sie den Projektroot zum Python-Pfad hinzu
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from utils.page_generator import generate_index_page
from utils.vector_db import embed_and_insert_files
from src.data_collection.advanced_crypto_scraper import main as run_scraper

async def run_scrapers():
    await run_scraper()

def initialize():
    # Start Docker containers
    subprocess.run(["docker-compose", "up", "-d"])

    # Run scrapers
    asyncio.run(run_scrapers())

    # Generate index page
    generate_index_page('data/html_pages')

    # Embed and insert files into vector DB
    embed_and_insert_files('data/html_pages')

if __name__ == "__main__":
    initialize()