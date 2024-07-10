# src/data_collection/advanced_crypto_scraper.py
import aiohttp
import asyncio
import logging
from bs4 import BeautifulSoup
from datetime import datetime
import os
import json
import sys

# Fügen Sie den Projektroot zum Python-Pfad hinzu
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from utils.config import Config
from utils.logger import setup_logger
from src.data_collection.data_storage import DataStorage



class CryptoScraper:
    def __init__(self, config):
        self.config = config
        self.session = None
        self.logger = logging.getLogger(__name__)
        self.data_storage = DataStorage()

    async def fetch_page(self, url):
        if not self.session:
            self.session = aiohttp.ClientSession()
        try:
            async with self.session.get(url) as response:
                return await response.text()
        except Exception as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None

    async def scrape_btc_data(self, url):
        html = await self.fetch_page(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            # Implementieren Sie hier die spezifische Parsing-Logik für BTC-Daten
            # Dies ist ein Beispiel und sollte an die tatsächliche Struktur der Ziel-Website angepasst werden
            price = soup.find('div', {'class': 'price'}).text.strip() if soup.find('div', {'class': 'price'}) else "N/A"
            volume = soup.find('div', {'class': 'volume'}).text.strip() if soup.find('div', {'class': 'volume'}) else "N/A"
            market_cap = soup.find('div', {'class': 'market-cap'}).text.strip() if soup.find('div', {'class': 'market-cap'}) else "N/A"
            return {
                'type': 'btc',
                'price': price,
                'volume': volume,
                'market_cap': market_cap,
                'timestamp': datetime.now().isoformat()
            }
        return None

    async def scrape_runes_data(self, url):
        html = await self.fetch_page(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            # Implementieren Sie hier die spezifische Parsing-Logik für Runes-Daten
            # Dies ist ein Platzhalter und sollte an die tatsächliche Datenstruktur angepasst werden
            rune_data = soup.find('div', {'id': 'rune-data'}).text.strip() if soup.find('div', {'id': 'rune-data'}) else "N/A"
            return {
                'type': 'runes',
                'data': rune_data,
                'timestamp': datetime.now().isoformat()
            }
        return None

    async def scrape_ordinals_data(self, url):
        html = await self.fetch_page(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            # Implementieren Sie hier die spezifische Parsing-Logik für Ordinals-Daten
            # Dies ist ein Platzhalter und sollte an die tatsächliche Datenstruktur angepasst werden
            ordinals_data = soup.find('div', {'id': 'ordinals-data'}).text.strip() if soup.find('div', {'id': 'ordinals-data'}) else "N/A"
            return {
                'type': 'ordinals',
                'data': ordinals_data,
                'timestamp': datetime.now().isoformat()
            }
        return None

    async def run(self):
        tasks = []
        for url in self.config.SCRAPING_URLS:
            if 'bitcoin' in url:
                tasks.append(self.scrape_btc_data(url))
            elif 'runes' in url:
                tasks.append(self.scrape_runes_data(url))
            elif 'ordinals' in url:
                tasks.append(self.scrape_ordinals_data(url))
        
        results = await asyncio.gather(*tasks)
        return [r for r in results if r]

    async def close(self):
        if self.session:
            await self.session.close()

def save_results(results, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f"scraped_data_{timestamp}.json")
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    return filename

async def main():
    config = Config()
    setup_logger()
    logger = logging.getLogger(__name__)

    scraper = CryptoScraper(config)
    try:
        results = await scraper.run()
        if results:
            filename = save_results(results, config.DATA_RAW_DIR)
            logger.info(f"Scraped data saved to {filename}")
            
            # Hier können Sie die Daten weiter verarbeiten oder in die Datenbank speichern
            data_storage = DataStorage()
            for result in results:
                data_storage.store_scraped_data(result)
            
            logger.info("Data processing and storage complete")
        else:
            logger.warning("No data was scraped")
    except Exception as e:
        logger.error(f"An error occurred during scraping: {e}")
    finally:
        await scraper.close()

if __name__ == "__main__":
    asyncio.run(main())