import os
from dotenv import load_dotenv

import requests
from bs4 import BeautifulSoup
import pandas as pd

load_dotenv()

jobs = [] # List of all jobs in Summer 2024 Tech Internships by Pitt CSC
filtered_jobs = [] # List of all jobs in Summer 2024 Tech Internships by Pitt CSC that I can apply to
apply_jobs = [] # List of all jobs to apply to

# Scraping the site for jobs
def web_crawler(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) == 3:
                        name = cells[0].text.strip()
                        location = cells[1].text.strip()
                        notes = cells[2].text.split("  ")
                        jobs.append({
                            "Name": name,
                            "Location": location,
                            "Notes": notes
                        })
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    starting_url = "https://github.com/pittcsc/Summer2024-Internships"
    web_crawler(starting_url)

    # Filtering the jobs
    for job in jobs:
        name = job["Name"]
        location = job["Location"]
        notes = job["Notes"]

        if notes[0] == "🔒 Closed 🔒":
            continue
        
        notes_lower = [note.lower() for note in notes]
        filtered_notes = []

        for note in notes_lower:
            
            if "no sponsorship" in note or "closed" in note or "citizen" in note:
                continue
            filtered_notes.append(note)

        if len(filtered_notes) == 0:
            continue
        else:
            filtered_jobs.append({
                "Name": name,
                "Location" : location,
                "Notes": filtered_notes
            })

    # # Printing the jobs after filter
    # for job in filtered_jobs:
    #     name = job["Name"]
    #     location = job["Location"]
    #     notes = job["Notes"]

    #     print(f"Name: {name}\nLocation: {location}\nNotes: {notes}\n")

    # Reading the csv file
    file_path = os.getenv("FILE_PATH")
    df = pd.read_csv(file_path, encoding='utf-8')
    
    # for index, row in df.iterrows():
    #     print(row.to_dict())

    # Matching filtered jobs and applied jobs
    df["Position"] = df["Position"].str.lower()
    for job in filtered_jobs:
        name = job["Name"]
        location = job["Location"]
        notes = job["Notes"]

        for job_name in notes:
            match = df[(df["Company"] == name) & (df["Position"] == job_name)]

            if match.empty:
                apply_jobs.append({
                    "Name": name,
                    "Location": location, 
                    "Notes": job_name
                })
            else:
                continue
        
    # Printing all the jobs to apply
    print("\n")
    for job in apply_jobs:
        name = job["Name"]
        location = job["Location"]
        notes = job["Notes"]

        print(f"Name: {name}\nLocation: {location}\nNotes: {notes}\n")