import logging
import argparse
import platform
import time
import os
import re
import random
import sqlite3
from datetime import datetime
from typing import List
from dataclasses import dataclass, asdict
from playwright.sync_api import sync_playwright, Page
import pandas as pd
from colorama import init, Fore, Style
from tqdm import tqdm
from fake_useragent import UserAgent

# ============================================================
# Project: Advanced Neshan Maps Scraper
# Author: @EhsanShahbazi
# Date: 2025-01-10
# Description:
# This script scrapes place information from Neshan Maps
# based on a search query and exports the results in
# multiple formats such as CSV, JSON, Parquet, or SQLite.
# ============================================================

# Initialize colorama for colored terminal output
init(autoreset=True)

@dataclass
class Place:
    # Data model for storing scraped place information
    name: str = ""
    category: str = ""
    address: str = ""
    phone_number: str = ""
    website: str = ""
    opening_hours_today: str = ""
    rating: str = ""
    reviews_count: str = ""

class ColorLogFormatter(logging.Formatter):
    # Custom colored formatter for logging output
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        # Apply color based on log level
        log_color = self.COLORS.get(record.levelno, Fore.WHITE)
        format_str = f"{Fore.LIGHTBLACK_EX}%(asctime)s{Style.RESET_ALL} - {log_color}%(levelname)s{Style.RESET_ALL} - %(message)s"
        formatter = logging.Formatter(format_str, datefmt="%H:%M:%S")
        return formatter.format(record)

def setup_logging(level: str):
    # Configure root logger and apply custom colored formatter
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper()))
    handler = logging.StreamHandler()
    handler.setFormatter(ColorLogFormatter())
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(handler)

def print_banner():
    """Print a colorful ASCII banner for Neshan"""
    banner_lines = [
        r"███╗   ██╗███████╗███████╗██╗  ██╗ █████╗ ███╗   ██╗",
        r"████╗  ██║██╔════╝██╔════╝██║  ██║██╔══██╗████╗  ██║",
        r"██╔██╗ ██║█████╗  ███████╗███████║███████║██╔██╗ ██║",
        r"██║╚██╗██║██╔══╝  ╚════██║██╔══██║██╔══██║██║╚██╗██║",
        r"██║ ╚████║███████╗███████║██║  ██║██║  ██║██║ ╚████║",
        r"╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝"
    ]
    
    # Color gradient for banner lines
    colors = [
        Fore.RED + Style.BRIGHT,
        Fore.YELLOW + Style.BRIGHT,
        Fore.GREEN + Style.BRIGHT,
        Fore.CYAN + Style.BRIGHT,
        Fore.BLUE + Style.BRIGHT,
        Fore.MAGENTA + Style.BRIGHT
    ]
    
    print("\n")
    for line, color in zip(banner_lines, colors):
        print(f"  {color}{line}{Style.RESET_ALL}")
    print("\n" + "=" * 54 + "\n")

def get_delay(mode: str) -> float:
    # Return a random delay value based on selected delay mode
    delays = {
        "low": (0.5, 1.5),
        "medium": (1.5, 3.5),
        "high": (3.5, 6.0)
    }
    min_d, max_d = delays.get(mode, delays["medium"])
    return random.uniform(min_d, max_d)

def extract_place(page: Page) -> Place:
    # Extract detailed information for a single place from the details page
    place = Place()
    place.url = page.url

    try:
        # Extract place name and category
        place.name = page.locator("h1.ZzIY7hD").inner_text().strip()
        place.category = page.locator("span.qpxuHlU").inner_text().strip()
    except:
        pass

    try:
        # Extract rating and number of reviews
        rating_info = page.locator(".qZI77s3").first
        if rating_info.count() > 0:
            text = rating_info.inner_text()
            match = re.search(r"(\d+/?\d*)\s*\((\d+)\)", text)
            if match:
                place.rating = match.group(1)
                place.reviews_count = match.group(2)
    except:
        pass

    try:
        # Extract address, phone number, and website from info buttons
        info_buttons = page.locator("button.wE_mwzL").all()
        for btn in info_buttons:
            text = btn.inner_text().replace('\u200e', '').strip()
            img_el = btn.locator("img")
            img_src = img_el.first.get_attribute("src") if img_el.count() > 0 else ""

            if "pin.png" in img_src:
                place.address = text
            elif "call.png" in img_src or "شماره تماس" in text:
                place.phone_number = text.replace("شماره تماس:", "").strip()
            elif "world.png" in img_src:
                link_el = btn.locator("a")
                href = link_el.first.get_attribute("href") if link_el.count() > 0 else ""
                if "وب‌سایت" in text or "وب سایت" in text:
                    place.website = href
            elif any(word in text for word in ["کوچه", "،", "خیابان", "بلوار", "میدان"]):
                place.address = text
    except Exception as e:
        logging.debug(f"Error parsing contact elements: {e}")

    try:
        # Extract today's opening hours
        hours_el = page.locator("div.GiQOShA")
        if hours_el.count() > 0:
            place.opening_hours_today = hours_el.inner_text().replace("ساعت کاری:", "").replace('\u200e', '').strip()
    except:
        pass

    return place

def scrape_places(search_for: str, total: int, headless: bool, delay_mode: str) -> List[Place]:
    # Main scraping function that searches Neshan and collects place data
    places: List[Place] = []
    ua = UserAgent()
    
    with sync_playwright() as p:
        browser_args = {"headless": headless}
        
        # Use installed Chrome on Windows if available
        if platform.system() == "Windows":
            path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            if os.path.exists(path):
                browser_args["executable_path"] = path
        
        browser = p.chromium.launch(**browser_args)
        context = browser.new_context(user_agent=ua.random)
        page = context.new_page()
        
        try:
            logging.info(f"Navigating to Neshan to search: {Fore.CYAN}{search_for}")
            page.goto("https://neshan.org/maps", wait_until="commit")
            
            # Interact with the search input and submit the query
            page.wait_for_selector("input.f5AeHfr")
            page.click("input.f5AeHfr")
            page.fill("input.AZLBjuP", search_for)
            page.keyboard.press("Enter")
            
            result_selector = ".nrFZBE4"
            page.wait_for_selector(result_selector, timeout=20000)
            
            # Scroll until enough listings are loaded or no more new results appear
            logging.info(f"Scrolling to find {total} listings...")
            last_count = 0
            while True:
                current_count = page.locator(result_selector).count()
                if current_count >= total or current_count == last_count:
                    break
                page.mouse.wheel(0, 4000)
                time.sleep(get_delay(delay_mode))
                last_count = current_count

            listings = page.locator(result_selector).all()[:total]
            actual_total = len(listings)
            
            # Show progress bar while scraping results
            pbar = tqdm(
                total=actual_total,
                desc=f"{Fore.MAGENTA}Scraping{Style.RESET_ALL}",
                bar_format="{l_bar}{bar:30}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
            )
            
            for idx, listing in enumerate(listings):
                try:
                    # Open the listing details page
                    listing.locator("h2").click(force=True)
                    page.wait_for_selector("h1.ZzIY7hD", timeout=10000)
                    time.sleep(get_delay(delay_mode))
                    
                    # Extract data from the opened listing
                    data = extract_place(page)
                    if data.name:
                        places.append(data)
                        logging.debug(f"Extracted: {data.name}")
                    
                    # Return to the search results page
                    page.go_back(wait_until="commit")
                    page.wait_for_selector(result_selector)
                except Exception as e:
                    logging.warning(f"Error on item {idx+1}: {e}")
                    page.goto("https://neshan.org/maps")
                
                pbar.update(1)
            pbar.close()

        finally:
            # Ensure browser is always closed
            browser.close()
            
    return places

def save_data(places: List[Place], base_name: str, fmt: str):
    # Save scraped data to the selected file format
    if not places:
        logging.warning("No data to save!")
        return
        
    df = pd.DataFrame([asdict(p) for p in places])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base_name}_{timestamp}.{fmt}"
    
    try:
        if fmt == 'csv':
            df.to_csv(filename, index=False, encoding='utf-8-sig')
        elif fmt == 'json':
            df.to_json(filename, orient='records', force_ascii=False, indent=4)
        elif fmt == 'parquet':
            df.to_parquet(filename, index=False)
        elif fmt == 'sqlite':
            filename = f"{base_name}_{timestamp}.db"
            conn = sqlite3.connect(filename)
            df.to_sql('places', conn, if_exists='replace', index=False)
            conn.close()
            
        logging.info(f"Data successfully saved to {Fore.YELLOW}{filename}")
    except Exception as e:
        logging.error(f"Failed to save data: {e}")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Advanced Neshan Maps Scraper")
    parser.add_argument("-s", "--search", type=str, default="cafe tehran", help="Search query")
    parser.add_argument("-t", "--total", type=int, default=5, help="Total items to scrape")
    parser.add_argument("-o", "--output", type=str, default="neshan_export", help="Base name for output file")
    parser.add_argument("-f", "--format", type=str, choices=['csv', 'json', 'parquet', 'sqlite'], default='csv', help="Output format")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--delay", type=str, choices=['low', 'medium', 'high'], default='medium', help="Delay profile to avoid blocking")
    parser.add_argument("--log", type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='INFO', help="Logging level")
    
    args = parser.parse_args()

    # Set up logging
    setup_logging(args.log)
    
    # Print the project banner
    print_banner()
    
    logging.info(f"{Fore.GREEN}Starting Scraper...{Style.RESET_ALL} Options: Format={args.format}, Headless={args.headless}, Delay={args.delay}")

    # Run scraping and save results
    results = scrape_places(args.search, args.total, args.headless, args.delay)
    save_data(results, args.output, args.format)

if __name__ == "__main__":
    main()
