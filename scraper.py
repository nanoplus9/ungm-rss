import json
import requests
from feedgen.feed import FeedGenerator

def fetch_ungm_tenders():
    # Target official public API endpoint directly
    api_url = "https://ungm.org"
    
    # Advanced headers to bypass bot protection
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://www.ungm.org",
        "Referer": "https://www.ungm.org/public/notice"
    }
    
    # Requesting the first 25 most recent active notices
    payload = {
        "page": 1,
        "displayedItemsCount": 25,
        "sortField": "DatePublished",
        "sortDescending": True
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        tenders = data.get('data', [])
        print(f"Successfully fetched {len(tenders)} tenders from UNGM.")
        return tenders
    except Exception as e:
        print(f"Error fetching data from UNGM: {e}")
        return []

def generate_rss():
    tenders = fetch_ungm_tenders()
    
    fg = FeedGenerator()
    fg.title("UNGM Procurement Opportunities Feed")
    fg.link(href="https://www.ungm.org/public/notice", rel="alternate")
    fg.description("Automated tracking of live UNGM Request for Proposals (RFP) and tenders.")
    
    if not tenders:
        # Fallback entry if data fetch fails
        fe = fg.add_entry()
        fe.title("Feed Temporarily Empty")
        fe.link(href="https://www.ungm.org/public/notice")
        fe.description("No active data returned from the UNGM portal during this cycle.")
        fe.id("fallback")
    
    for item in tenders:
        title = item.get("Title", "Untitled Tender")
        notice_id = item.get("Id", "")
        link = f"https://ungm.org{notice_id}" if notice_id else "https://www.ungm.org/public/notice"
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
    print("Success: ungm_feed.xml has been refreshed!")

if __name__ == "__main__":
    generate_rss()
