
# IMDb Top 10000 Movies Web Scraping

This project is a Python script for scraping the top 10,000 movies from IMDb. The script extracts movie details such as name, year, rating, metascore, gross income, votes, runtime, genre, certificate, description, directors, and stars. The data is scraped from IMDb's website using web scraping techniques.

## Implementation Details

- **Web Scraping**: Implemented web scraping using the `requests` library to fetch HTML content and `BeautifulSoup` library for parsing the HTML and extracting relevant data.
- **Data Cleaning**: Removed inconsistent values and handled possible errors during scraping to ensure the scraped data is consistent and reliable.
- **Data Utilization**: The cleaned data can be utilized for various purposes including data analysis, natural language processing (NLP), and other research applications.

## Prerequisites

Make sure you have the following Python libraries installed:

- `requests`
- `BeautifulSoup`
- `numpy`

You can install them using pip:

```
pip install requests BeautifulSoup numpy
```

## How to Use

1. Clone the repository:

```
git clone <repository-url>
```

2. Run the Python script:

```
python scraper.py
```

The script will start scraping the IMDb website and save the data in appropriate data structures.

## Files

- **`scraper.py`**: Python script for web scraping IMDb's top 10,000 movies.
- **`data.csv`**: CSV file containing scraped movie data.
- **`README.md`**: Documentation file you are currently reading.

## Notes

- The scraping script is designed to handle possible connection errors and missing data gracefully.
- The data is saved in CSV format for easy import and analysis.
