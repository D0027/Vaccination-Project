# 💉 Vaccination Data Analysis and Visualization

End-to-end project: WHO vaccination data → Python cleaning/EDA → MySQL (`vaccination_db`) → Power BI dashboard → Streamlit app.

## Folder structure

```
vaccination-project/
├── data/
│   ├── raw/                 ← put the 5 original WHO CSVs here
│   └── cleaned/              ← cleaned CSVs exported from the notebook go here
├── notebooks/
│   └── vaccination_analysis.ipynb   ← full cleaning + EDA + 30 questions
├── sql/
│   ├── schema.sql            ← CREATE TABLE statements (6 tables)
│   ├── views.sql             ← 6 analytical views (feed Power BI + Streamlit)
│   └── load_data.py          ← loads cleaned CSVs into MySQL
├── powerbi/
│   └── vaccination_dashboard.pbix   ← your 9-page Power BI report
├── streamlit_app/
│   ├── app.py                ← the Streamlit dashboard
│   ├── db.py                 ← MySQL connection helper
│   ├── requirements.txt
│   └── .env.example          ← copy to .env, fill in MySQL credentials
├── docs/
│   ├── Project_Documentation.docx   ← full write-up (process/challenges/insights)
│   └── Project_Brief.docx           ← original requirements doc
└── images/                   ← dashboard screenshots (optional, for docs)
```

## 1. About your MySQL database (`vaccination_db`)

You already built this in MySQL Workbench — nothing to redo. This folder just gives it a
portable, version-controlled home so the whole project (not just the dashboard) is
reproducible on any machine, including for Streamlit to connect to it.

**Two options, pick whichever fits:**

**Option A — Keep using your existing local DB (fastest).**
Nothing to do. Just point `.env` at it (see step 2 below) and both Streamlit and any
fresh MySQL Workbench session will read the same `vaccination_db`.

**Option B — Make it portable / back it up into this repo.**
Export a full dump from your existing database so it's included in the project folder
and can be restored on any machine:
```bash
mysqldump -u root -p vaccination_db > sql/vaccination_db_dump.sql
```
To restore it elsewhere later:
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS vaccination_db"
mysql -u root -p vaccination_db < sql/vaccination_db_dump.sql
```
`schema.sql` + `views.sql` are also included separately in case you ever need to
rebuild the structure from scratch (e.g. on a new machine) and repopulate from the
cleaned CSVs using `sql/load_data.py`.

## 2. Set up credentials

```bash
cp .env.example .env
# then edit .env with your MySQL Workbench username/password
```

## 3. Run the Streamlit app

```bash
cd streamlit_app
pip install -r requirements.txt
cp .env.example .env      # if not already done at root
streamlit run app.py
```

Opens at `http://localhost:8501`. If MySQL isn't reachable, the app automatically
falls back to demo data with a banner — so it always renders, even before you've
connected your DB.

## 4. Power BI

Open `powerbi/vaccination_dashboard.pbix` in Power BI Desktop. It's already wired to
`vaccination_db` — if you moved databases/machines, update the data source under
**Home → Transform Data → Data Source Settings**.

## 5. Notebook

`notebooks/vaccination_analysis.ipynb` — the full Python pipeline: load → clean → EDA
→ all 30 analytical questions → export cleaned CSVs to `data/cleaned/`.

## 6. Documentation

`docs/Project_Documentation.docx` — the full write-up: problem statement, cleaning
process, DB design, dashboard walkthrough (with screenshots), key insights, challenges,
and deliverables checklist.
