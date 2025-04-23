import requests
import os
from dotenv import load_dotenv
from utils.files import download_file, PLAYBOOK_FOLDER

load_dotenv() 

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def google_search(query: str):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "q": query
    }
    response = requests.post(url, headers=headers, json=data)
    results = response.json()

    links = []
    for item in results.get("organic", []):
        links.append(f"🔗 {item.get('title')}\n{item.get('link')}\n{item.get('snippet')}\n")
        title = item['title']
        link = item['link']

        if link.lower().endswith(('.pdf', '.docx', '.pptx')): 
            filename = f"{title[:30].replace(' ', '_')}_{link.split('/')[-1]}"
            save_path = os.path.join(PLAYBOOK_FOLDER, filename)
            download_file(link, save_path)
        else:
            print(f"Skipping non-file link: {link}")
    return "\n\n".join(links[:5]) or "No relevant results found."
