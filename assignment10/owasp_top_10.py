import re
import time
import csv
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://owasp.org/www-project-top-ten/"

def main():
    #headless so no browser window pops up
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1200,900")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                              options=options)
    
    try:
        
        #wait to avoid overloading server
        driver.get(URL)
        time.sleep(1.5)  

        #grab all links on the page, then filter to ones like "A01:2021-..."
        a_tags = driver.find_elements(By.TAG_NAME, "a")
        results = []
        seen_titles = set()

        #regex for "Axx:YYYY-" pattern
        pat = re.compile(r"^A\d{2}:\d{4}-")  

        #selenium returns a list of WebElement objects
        for a in a_tags:
            text = (a.text or "").strip() #grab text
            href = a.get_attribute("href") or "" #grab href url
            if not text or not href:
                continue
            if pat.match(text):
                #dedupe by title in case it appears more than once
                if text not in seen_titles:
                    seen_titles.add(text)
                    results.append({"Title": text, "URL": href})

        #sort by A-number for cleanliness
        def sort_key(row):
            
            #pull the 2-digit number after 'A'
            m = re.match(r"A(\d{2}):", row["Title"])
            return int(m.group(1)) if m else 999
        results.sort(key=sort_key)

        #print to confirm results
        for r in results:
            print(f"{r['Title']} -> {r['URL']}")

        #navigate to assignment10
        out_dir = Path(__file__).parent 
        csv_path = out_dir / "owasp_top_10.csv"
        
        #write to csv
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["Title", "URL"])
            w.writeheader()
            w.writerows(results)
            
        #confirmation
        print(f"\nSaved {len(results)} rows to {csv_path}")

    #selenium cleanup
    finally:
        driver.quit()

#boilerplate
if __name__ == "__main__":
    main()
