# Job Scraper

The Job Scraper is a Python script that scrapes the Pitt CSC Github page for Summer 2024 Tech Internship job listings. It filters the job listings to find only those that are open for application and are eligible for candidates seeking sponsorship. The script then matches these filtered jobs with the user's existing job applications listed in a CSV file. It finally prints out a list of jobs that the user can apply to.

## Requirements

- Python 3.6+
- `requests` library
- `beautifulsoup4` library
- `pandas` library