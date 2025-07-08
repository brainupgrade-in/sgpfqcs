
# Prospect2Sales

Simple Flask+SQLite demo app for managing prospects all the way to sales.

## Features

* Add prospects
* Qualify / Disqualify prospects
* Convert qualified prospects to sales (track amount & outcome)
* Basic dashboard metrics
* Packaged with Docker and runnable locally

## Quick start (local)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask --app app.py init-db
flask run
```

## Docker

```bash
./build_and_run.sh
```

Visit **http://localhost:5000**

---

_Generated on 2025-07-08_


## Data persistence

The SQLite file lives in `/data` inside the container.  
We mount the host `./data` folder, so your database survives container restarts.

```bash
./build_and_run.sh
# or
docker compose up --build
```
