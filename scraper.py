import json
import requests
from feedgen.feed import FeedGenerator

def fetch_ungm_tenders():
    api_url = "https://ungm.org"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    payload = {
        "page": 1,
        "displayedItemsCount": 20,
        "sortField": "DatePublished",
        "sortDescending": True
    }
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get('data', [])
    except Exception as e:
        print(f"Error fetching data from UNGM: {e}")
        return []

def generate_rss():
    tenders = fetch_ungm_tenders()
    fg = FeedGenerator()
    fg.title("UNGM Procurement Opportunities Feed")
    fg.link(href="https://www.ungm.org/public/notice", rel="alternate")
    fg.description("Automated tracking of live UNGM Request for Proposals (RFP) and tenders.")
    
    for item in tenders:
        title = item.get("Title", "Untitled Tender")
        notice_id = item.get("Id", "")
        link = f"https://www.ungm.org/Public/Notice/{notice_id}" if notice_id else "https://www.ungm.org/public/notice"
        agency = item.get("AgencyName", "Unknown Agency")
        deadline = item.get("DeadlineStr", "No Deadline Specified")
        countries = item.get("BeneficiaryCountriesStr", "Global")
        
        description = f"Agency: {agency} | Deadline: {deadline} | Beneficiary: {countries}"
        
        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=link)
        fe.description(description)
        fe.id(str(notice_id))

    fg.rss_file("ungm_feed.xml", pretty=True)
    print("Success: ungm_feed.xml generated successfully!")

if __name__ == "__main__":
    generate_rss()
