# LinkedIn AI Job Scraper

An intelligent job scraping tool that combines LinkedIn job listings with OpenAI's GPT-4 for smart filtering based on custom criteria.

## Features

- Scrapes LinkedIn job postings based on keywords
- Filters jobs using GPT-4 based on custom criteria
- Supports multiple job level filtering
- Exports results to CSV
- Prevents duplicate job exploration
- User-friendly web interface

## Prerequisites

- Python 3.8+
- OpenAI API key
- Internet connection

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/linkedin-ai-job-scraper.git
cd linkedin-ai-job-scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

## Usage

1. Access the web interface at `http://localhost:5000`
2. Enter your OpenAI API key
3. Add keywords (up to 10) for job search
4. Select desired job levels
5. Define search criteria for AI filtering
6. Submit to start the search
7. Download results as CSV if needed

## Security Note

The application stores the OpenAI API key in memory only and does not persist it.

## License

MIT License

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss proposed changes.