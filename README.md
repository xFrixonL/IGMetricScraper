# IGMetricScraper

IGMetricScraper is an automation and analytics tool designed to extract Instagram profile performance metrics in an ethical, structured way. It uses Playwright for browser navigation, a custom analytics engine, and AI-powered sentiment analysis to calculate engagement, content performance, and community insights for both Posts and Reels.

## Key Features

- **Hybrid extraction**: captures both static posts and Reels data using network interception and modal navigation.
- **Dual operating modes**:
  - **Mode 1 - Deep Analytics**: Comprehensive comparison of Posts vs Reels performance with engagement metrics
  - **Mode 2 - Community Audit**: In-depth sentiment analysis of user comments powered by AI (Groq Llama 3.3)
- **Identity validation**: ensures data belongs only to the target profile, preventing deviation from suggestion algorithms.
- **Separate analytics engine**:
  - Engagement Rate (ER) by content type
  - Conversation Ratio (comments/likes) for Posts and Reels
  - Top performer detection (best post/reel based on reach and interaction)
- **AI-powered sentiment analysis**: Uses Groq API to analyze community sentiment, detect top topics, and understand audience vibe
- **Smart comment extraction**: Captures verified user status, comment engagement, and conversation patterns
- **Persistence**: outputs structured reports in JSON format with optional AI insights

## Prerequisites

- Python 3.8 or higher
- Active Instagram session saved in `session.json`
- Groq API key (for Mode 2 - Community Audit with AI analysis)
  - Get your free API key at [console.groq.com](https://console.groq.com)
  - Store it in a `.env` file as `GROQ_API_KEY=your_key_here`

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

- `main.py`: Main orchestrator for the scraping process with dual-mode selection
- `processor.py`: Network interception and raw data processing logic
- `analytics.py`: Analytics engine for metric calculation and reporting
- `ai_engine.py`: AI-powered sentiment analysis engine using Groq API
- `session_manager.py`: Session persistence helper for login/session state
- `requirements.txt`: Project dependencies

## Usage

1. Generate the Instagram session file first:

```bash
python session_manager.py
```

2. Run the main scraper:

```bash
python main.py
```

3. When prompted, enter the Instagram username and select your analysis mode:

```
Introduce el @usuario: exampleuser

MODOS DISPONIBLES:
1. Deep Analytics (Comparativa Posts vs Reels)
2. Community Audit (Análisis de Sentimiento con IA)

Selecciona modo (1 o 2): 
```

### Mode Details

**Mode 1 - Deep Analytics**: 
- Extracts up to 10 Posts and 10 Reels
- Compares engagement metrics between content types
- Generates detailed engagement rates and conversation ratios
- Outputs performance comparison report

**Mode 2 - Community Audit**:
- Analyzes up to 12 post/reel comments
- Uses Groq AI (Llama 3.3) to detect:
  - Overall sentiment (Positive/Negative/Neutral)
  - Top discussion topics
  - Community vibe and engagement patterns
- Includes verified user detection
- Generates AI-powered community insights report

## Metrics Explained

### Analytics Metrics
- **ER (Engagement Rate)**: Measures audience engagement relative to total followers
- **Conversation Ratio**: Indicates whether content generates discussion versus passive consumption
- **Average Reels Plays**: Reflects real organic reach of the Reels section

### AI Sentiment Analysis Metrics (Mode 2)
- **Sentiment**: Overall community sentiment classification (Positive/Negative/Neutral)
- **Top Topics**: Automatically extracted main discussion themes from comments
- **Community Vibe**: Qualitative assessment of audience attitude and engagement tone
- **Verified Status**: Identifies comments from verified users for credibility assessment

## Configuration

### Environment Setup
Create a `.env` file in the project root directory:

```env
GROQ_API_KEY=your_api_key_here
```

### Chrome Session
1. Run `session_manager.py` to authenticate with Instagram
2. The tool will save your session state in `session.json`
3. Use this saved session for scraping without re-authenticating

## Legal Notice

This tool is intended for educational and research data analysis only. Use it in compliance with the platform's terms of service and local privacy regulations. When using Mode 2, ensure you have appropriate consent for sentiment analysis of public comments.