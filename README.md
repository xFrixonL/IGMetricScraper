# IGMetricScraper

IGMetricScraper is an automation and analytics tool designed to extract Instagram profile performance metrics in an ethical, structured way. It uses Playwright for browser navigation and a custom analytics engine to calculate engagement and content performance for both Posts and Reels.

## Key Features

- Hybrid extraction: captures both static posts and Reels data using network interception and modal navigation.
- Identity validation: ensures data belongs only to the target profile, preventing deviation from suggestion algorithms.
- Separate analytics engine:
  - Engagement Rate (ER) by content type
  - Conversation Ratio (comments/likes) for Posts and Reels
  - Top performer detection (best post/reel based on reach and interaction)
- Persistence: outputs structured reports in JSON format

## Prerequisites

- Python 3.8 or higher
- Active Instagram session saved in `session.json`

## Installation

```bash
git clone https://github.com/tu-usuario/IGMetricScraper.git
cd IGMetricScraper

python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt
playwright install chromium
```

## Project Structure

- `main.py`: Main orchestrator for the scraping process
- `processor.py`: Network interception and raw data processing logic
- `analytics.py`: Analytics engine for metric calculation and reporting
- `session_manager.py`: Session persistence helper for login/session state
- `requirements.txt`: Project dependencies

## Usage

1. Generate the Instagram session file first:

```bash
python session_manager.py
```

2. Then run the main scraper:

```bash
python main.py
```

`main.py` currently targets the username configured in the script. Adjust the `scrape_profile("username")` call as needed.

## Metrics Explained

- ER (Engagement Rate): measures audience engagement relative to total followers
- Conversation Ratio: indicates whether content generates discussion versus passive consumption
- Average Reels Plays: reflects real organic reach of the Reels section

## Legal Notice

This tool is intended for educational and research data analysis only. Use it in compliance with the platform’s terms of service and local privacy regulations.
```# IGMetricScraper

IGMetricScraper is an automation and analytics tool designed to extract Instagram profile performance metrics in an ethical, structured way. It uses Playwright for browser navigation and a custom analytics engine to calculate engagement and content performance for both Posts and Reels.

## Key Features

- Hybrid extraction: captures both static posts and Reels data using network interception and modal navigation.
- Identity validation: ensures data belongs only to the target profile, preventing deviation from suggestion algorithms.
- Separate analytics engine:
  - Engagement Rate (ER) by content type
  - Conversation Ratio (comments/likes) for Posts and Reels
  - Top performer detection (best post/reel based on reach and interaction)
- Persistence: outputs structured reports in JSON format

## Prerequisites

- Python 3.8 or higher
- Active Instagram session saved in `session.json`

## Installation

```bash
git clone https://github.com/tu-usuario/IGMetricScraper.git
cd IGMetricScraper

python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt
playwright install chromium
```

## Project Structure

- `main.py`: Main orchestrator for the scraping process
- `processor.py`: Network interception and raw data processing logic
- `analytics.py`: Analytics engine for metric calculation and reporting
- `session_manager.py`: Session persistence helper for login/session state
- `requirements.txt`: Project dependencies

## Usage

1. Generate the Instagram session file first:

```bash
python session_manager.py
```

2. Then run the main scraper:

```bash
python main.py
```

`main.py` currently targets the username configured in the script. Adjust the `scrape_profile("username")` call as needed.

## Metrics Explained

- ER (Engagement Rate): measures audience engagement relative to total followers
- Conversation Ratio: indicates whether content generates discussion versus passive consumption
- Average Reels Plays: reflects real organic reach of the Reels section

## Legal Notice

This tool is intended for educational and research data analysis only. Use it in compliance with the platform’s terms of service and local privacy regulations.