import sqlite3
from tabulate import tabulate

DB = 'scraper.db'

def view_results():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM serp_results ORDER BY link_id DESC")
    rows = c.fetchall()
    conn.close()
    
    
    if rows:
        print(tabulate(rows, headers=["ID", "Link Text", "URL", "Search Term", "Date Created"]))
    else:
        print("No results found.")

if __name__ == "__main__":
    view_results()