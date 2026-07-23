import sys
import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_contributions(username="GFCOR", output_file="data/contributions.json"):
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    print(f"Fetching contribution calendar for user: {username}...")
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"Error fetching contributions: HTTP {res.status_code}")
        sys.exit(1)
        
    soup = BeautifulSoup(res.text, "html.parser")
    
    # Parse days
    days_data = []
    # Check both td and rect elements
    cells = soup.find_all(["td", "rect"], class_=lambda c: c and "ContributionCalendar-day" in c)
    
    for cell in cells:
        date_str = cell.get("data-date")
        if not date_str:
            continue
            
        level = cell.get("data-level", "0")
        try:
            level = int(level)
        except ValueError:
            level = 0
            
        count = 0
        # Check tooltips or aria-label/id for exact count if available
        # E.g. "12 contributions on January 1, 2025" or "No contributions..."
        cell_id = cell.get("id")
        if cell_id:
            tooltip = soup.find("tool-tip", attrs={"for": cell_id})
            if tooltip:
                text = tooltip.get_text().strip()
                if "No contribution" in text or "0 contribution" in text:
                    count = 0
                else:
                    parts = text.split()
                    if parts and parts[0].isdigit():
                        count = int(parts[0])
                    else:
                        count = level * 3 if level > 0 else 0
        if count == 0 and level > 0:
            count = level * 2
            
        days_data.append({
            "date": date_str,
            "count": count,
            "level": level
        })
        
    # Calculate stats
    total_contributions = sum(d["count"] for d in days_data)
    
    # Calculate total count from header if present
    h2 = soup.find("h2", class_=lambda c: c and "f4" in c)
    if h2:
        h2_text = h2.get_text().strip()
        parts = h2_text.split()
        if parts and parts[0].replace(",", "").isdigit():
            total_contributions = int(parts[0].replace(",", ""))

    # Streaks
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    
    sorted_days = sorted(days_data, key=lambda x: x["date"])
    for d in sorted_days:
        if d["count"] > 0 or d["level"] > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0
            
    # Reverse check for current streak
    for d in reversed(sorted_days):
        if d["count"] > 0 or d["level"] > 0:
            current_streak += 1
        else:
            # allow today/yesterday to be 0 without breaking if recent
            break

    payload = {
        "username": username,
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "days": days_data,
        "updated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        
    print(f"Saved {len(days_data)} days of contributions to {output_file}. Total: {total_contributions}")

if __name__ == "__main__":
    user = sys.argv[1] if len(sys.argv) > 1 else "GFCOR"
    fetch_contributions(user)
