from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import sqlite3
import time
from datetime import datetime
import random


app = Flask(__name__)
DB = 'scraper.db'

# DB Instantiation
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS serp_results (
            link_id INTEGER PRIMARY KEY AUTOINCREMENT,
            link_text TEXT,
            link_url TEXT,
            search_term TEXT,
            date_created TEXT
        ) 
              ''')
    
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        query = request.form['query']
        options = Options()
        # options.add_argument("--headless")
        # Mimic human browser
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/113.0.0.0 Safari/537.36")

        options.add_argument("--disable-extensions")
        options.add_argument("--disable-logging")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=options)
        
        driver.get("https://www.google.com/")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        # time.sleep(2)
        time.sleep(random.uniform(1.5, 3.0))
        
        links = driver.find_elements(By.XPATH, "//div[@class='yuRubf']/a")[:8]
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        for link in links:
            text = link.text or link.get_attribute('href')
            href = link.get_attribute('href')        
            
            c.execute('''
                    INSERT INTO serp_results (link_text, link_url, search_term, date_created)
                    VALUES (?, ?, ?, ?)
                      ''', (text, href, query, now))
            results.append((text, href))
        conn.commit()
        conn.close()
        driver.quit()
    return render_template("index.html", results=results)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)