# 🔍 DuckDuckGo SERP Scraper (Flask + Selenium + SQLite)

Simple SERP Flask web application designed to:

✅ Perform search queries on [DuckDuckGo](https://duckduckgo.com)  
✅ Scrape the top 8 search result links  
✅ Store the links in a SQLite database  
✅ View a full archive of all scraped results  
✅ Export search results as a CSV file  
✅ Interact with the scraper via AJAX for seamless user experience

---

## 🛠️ Tech Stack

- **Flask** (Web framework)
- **Selenium** (Web automation)
- **DuckDuckGo** (Target search engine)
- **SQLite** (Lightweight database)
- **AJAX** (Asynchronous form submission)
- **HTML + JS** (Frontend)

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/mayerz6/ETLDevBench.git
cd serp_flask
```

### 2. Create a Virtual Environment (Optional)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### Required packages:

✅ Flask
✅ Selenium
✅ Werkzeug
✅ Tabulate (optional for CLI tools)

📌 Don't forget to install ChromeDriver and place it in your system PATH.

### 4. 🚀 Run the Application
```bash
python app.py
```
### 5.Access it in your browser:
``` bash
http://127.0.0.1:5000/
```