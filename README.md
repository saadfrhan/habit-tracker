# habit tracker

minimal cli and web habit tracker uses 
- sqlite3 for data persistence, 
- matplotlib for graphs, 
- flask for web,
- docker for containerization

## setup

### init setup

```bash
git clone https://github.com/saadfrhan/habit-tracker-cli
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt      
```

### web

```bash
gunicorn web:app
```

### docker compose

```bash
docker compose up -d
```

visit [localhost:8000](localhost:8000) for the demo
visit [localhost:3000](localhost:3000) for the sqlite browser for `habits.db`

### docker

```bash
docker buildx build -t habit-tracker-image .
docker run --name habit-tracker-container -p 8000:8000 -v $(pwd)/data:/app/data habit-tracker-image
```

now visit [localhost:8000](http://localhost:8000).

### cli

```bash
# add a new entry
python habit.py add <text>               
# list all entries
python habit.py list                     
# search by keyword (case insensitive)
python habit.py search <keyword>         
# search by exact date
python habit.py search-date <YYYY-MM-DD> 
# show count per day
python habit.py stats-daily              
# show count per month
python habit.py stats-monthly            
# export all entries to CSV
python habit.py export-csv               
# generates a PNG bar chart of daily counts
python habit.py chart-daily              
# prompts for today's entry, updates DB, CSV and chart
python habit.py daily-update       
```
