from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import sqlite3
import time
from datetime import datetime

app = Flask(__name__)
DB = '../scraper.db'

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
        # options.add_argument("--headless")  # Or leave this out if debugging
        options.add_argument("user-agent=Mozilla/5.0")
        driver = webdriver.Chrome(options=options)

        try:
            driver.get("https://duckduckgo.com")
            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            time.sleep(2)

            links = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='result-title-a']")[:8]

            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            conn = sqlite3.connect(DB)
            c = conn.cursor()

            for link in links:
                text = link.text
                href = link.get_attribute('href')

                c.execute('''
                    INSERT INTO serp_results (link_text, link_url, search_term, date_created)
                    VALUES (?, ?, ?, ?)
                ''', (text, href, query, now))

                results.append((text, href))

            conn.commit()
            conn.close()
        finally:
            driver.quit()

    return render_template("index.html", results=results)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
