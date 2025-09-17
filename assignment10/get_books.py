from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import json
import time
import os

URL = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"

#headless to prevent browser window pop ups
opts = webdriver.ChromeOptions()
opts.add_argument("--headless=new")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opts)

try:
    #open the page
    driver.get(URL)

    #wait for any result item to exist
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "li.cp-search-result-item"))
    )

    #find results
    items = driver.find_elements(By.CSS_SELECTOR, "li.cp-search-result-item")
    #print(len(items))  #<- for debugging

    results = []

    #main loop, loop through each <li> result item
    for li in items:
        #extract each title (title text sits in <h2 class="cp-title"><a><span class="title-content">…</span>)
        t = ""
        try:
            t = li.find_element(By.CSS_SELECTOR, "h2.cp-title a .title-content").text.strip()
        except:
            try:
                t = li.find_element(By.CSS_SELECTOR, "h2.cp-title a").text.strip()
            except:
                t = ""

        #extract authors
        a_elems = li.find_elements(By.CSS_SELECTOR, "a.author-link")
        authors = "; ".join([a.text.strip() for a in a_elems if a.text.strip()])

        #extract format & year (inside div.cp-format-info; prefer the primary span)
        fy = ""
        try:
            fy = li.find_element(By.CSS_SELECTOR, ".cp-format-info .display-info-primary").text.strip()
        except:
            try:
                fy = li.find_element(By.CSS_SELECTOR, ".cp-format-info").text.strip()
            except:
                fy = ""

        #save results
        results.append({"Title": t, "Author": authors, "Format-Year": fy})
        
        #courtesy pause to avoid overwhelming server
        time.sleep(0.05)  

    #create and print table
    df = pd.DataFrame(results)
    print(df)

    #JSON to inspect
    #with open("books_page1.json", "w", encoding="utf-8") as f:
    #    json.dump(results, f, ensure_ascii=False, indent=2)


finally:
    driver.quit()


#TASK 4

#save DataFrame to CSV
csv_path = os.path.join("assignment10", "get_books.csv")
df.to_csv(csv_path, index=False, encoding="utf-8")
print(f"CSV written to {csv_path}")

#save results list to JSON
json_path = os.path.join("assignment10", "get_books.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"JSON written to {json_path}")
