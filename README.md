<!-- BANNER START -->
<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=32&duration=2800&pause=2000&color=A020F0&center=true&vCenter=true&width=600&lines=Neshan+Maps+Scraper;Extract+Places+Like+a+Pro" alt="Typing SVG" />
</p>

<p align="center">
  <b>📍 A powerful, colourful, and stealthy scraper for Neshan Maps</b><br>
  <i>Search for businesses, extract detailed info, and export to CSV, JSON, SQLite & more.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License"/>
  <img src="https://img.shields.io/badge/Playwright-Powered-orange?logo=playwright" alt="Playwright"/>
</p>

<pre align="center">
███╗   ██╗███████╗███████╗██╗  ██╗ █████╗ ███╗   ██╗
████╗  ██║██╔════╝██╔════╝██║  ██║██╔══██╗████╗  ██║
██╔██╗ ██║█████╗  ███████╗███████║███████║██╔██╗ ██║
██║╚██╗██║██╔══╝  ╚════██║██╔══██║██╔══██║██║╚██╗██║
██║ ╚████║███████╗███████║██║  ██║██║  ██║██║ ╚████║
╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
</pre>

---

## ✨ Features

- 🔍 **Search any query** on [Neshan Maps](https://neshan.org/maps) (restaurants, shops, services...)
- 📋 **Extract rich data**: name, category, address, phone, website, opening hours, rating, reviews
- 🎨 **Beautiful coloured console output** with progress bars
- 🥷 **Anti-detection** measures: random user-agents, configurable delays, stealthy scrolling
- 📁 **Multiple export formats** – CSV, JSON, Parquet, SQLite
- ⚙️ **Fully configurable** via CLI arguments

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/neshan-scraper.git
cd neshan-scraper

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers (Chromium)
playwright install chromium
```

> **Note:** On Windows, the script automatically tries to use your installed Chrome if available – no Playwright browser download needed in that case.

---

## 🖥️ Usage

Run the scraper with a simple command:

```bash
python neshan_scraper.py -s "فست فود تهران" -t 20 -f csv
```

This will search for "fast food in Tehran", scrape **20** listings, and save them to a timestamped CSV file.

### ⚡ All Options

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--search` | `-s` | Search query (UTF-8 supported) | `فست فود تهران` |
| `--total` | `-t` | Number of places to scrape | `5` |
| `--output` | `-o` | Base name for the export file | `neshan_export` |
| `--format` | `-f` | Output format: `csv`, `json`, `parquet`, `sqlite` | `csv` |
| `--headless` | | Run browser in background (no GUI) | `False` |
| `--delay` | | Delay profile: `low`, `medium`, `high` | `medium` |
| `--log` | | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR` | `INFO` |

---

## 📸 Terminal Preview

This is how the scraper looks in action:
```bash
(venv) ➜  neshan-scraper python neshan.py -s "cafe tehran" -t 10 -f csv --delay medium

  ███╗   ██╗███████╗███████╗██╗  ██╗ █████╗ ███╗   ██╗
  ████╗  ██║██╔════╝██╔════╝██║  ██║██╔══██╗████╗  ██║
  ██╔██╗ ██║█████╗  ███████╗███████║███████║██╔██╗ ██║
  ██║╚██╗██║██╔══╝  ╚════██║██╔══██║██╔══██║██║╚██╗██║
  ██║ ╚████║███████╗███████║██║  ██║██║  ██║██║ ╚████║
  ╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝

======================================================

14:08:21 - INFO - Starting Scraper... Options: Format=csv, Headless=False, Delay=medium
14:08:22 - INFO - Navigating to Neshan to search: cafe tehran
14:08:24 - INFO - Scrolling to find 10 listings...
Scraping: 100%|██████████████████████████████| 10/10 [00:26<00:00]
14:08:50 - INFO - Data successfully saved to neshan_export_20260527_140850.csv
```

## 📦 Example Output (CSV)

| name | category | address | phone_number | website | opening_hours_today | rating | reviews_count |
|------|----------|---------|--------------|---------|---------------------|--------|---------------|
| برگرلند | فست فود | تهران، خیابان ولیعصر... | ۰۲۱-۸۸۸۸۸۸۸۸ | https://... | ۱۱:۰۰ - ۲۳:۰۰ | 4.5 | (124) |

---

## ⚠️ Disclaimer

This tool is intended for **educational purposes** and **personal research** only.  
Please respect the website’s `robots.txt` and terms of service. Do not overload the server with aggressive scraping.

---

## 🤝 Contributing & Support

If you need more features, find a bug, or have an idea to make this tool better:
- 🚩 **Open an Issue** to report bugs or request features.
- 🍴 **Fork the repo** and submit a **Pull Request**.
- 🌟 **Star the project** if it helped you!

I'm more than happy to collaborate and see this project grow!

---

## 📄 License

MIT ©EhsanShahbazi

---

<p align="center">
  Made with ❤️ and lots of ☕
</p>
