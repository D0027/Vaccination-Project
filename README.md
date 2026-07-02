<div align="center">

# 💉 Vaccination Data Analysis & Visualization

**A full-stack global public health analytics platform** — from raw WHO/UNICEF datasets to a live interactive dashboard, spanning Python, SQL, Power BI, and Streamlit.

[![Live App](https://img.shields.io/badge/🔴_LIVE_DEMO-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://vaccination-project-027.streamlit.app/)

<p>
<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/MySQL-vaccination__db-4479A1?style=flat-square&logo=mysql&logoColor=white" />
<img src="https://img.shields.io/badge/Power_BI-9_pages-F2C811?style=flat-square&logo=powerbi&logoColor=black" />
<img src="https://img.shields.io/badge/Pandas-EDA-150458?style=flat-square&logo=pandas&logoColor=white" />
<img src="https://img.shields.io/badge/Plotly-Charts-3F4F75?style=flat-square&logo=plotly&logoColor=white" />
<img src="https://img.shields.io/badge/License-MIT-2BD9A0?style=flat-square" />
</p>

**[🚀 View Live Dashboard](https://vaccination-project-027.streamlit.app/)**

</div>

---

## 📌 Overview

This project analyzes global vaccination coverage, disease incidence, and immunization trends across all six WHO regions, using official WHO/UNICEF datasets. It covers the complete data lifecycle, end to end:

<div align="center">

`5 raw WHO CSVs` → `Python cleaning & EDA (30 analytical questions)` → `Normalized MySQL schema (6 tables · 6 views)` → `Power BI dashboard (9 pages)` → `Streamlit web app`

</div>

The Streamlit app connects live to MySQL and automatically falls back to demo data if the database isn't reachable — so it always renders cleanly, both locally and in production.

---

## 📖 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Folder Structure](#-folder-structure)
- [Getting Started](#-getting-started)
  - [1. Database Setup](#1-database-setup)
  - [2. Configure Credentials](#2-configure-credentials)
  - [3. Run the Streamlit App](#3-run-the-streamlit-app)
  - [4. Power BI Report](#4-power-bi-report)
  - [5. Jupyter Notebook](#5-jupyter-notebook)
- [Documentation](#-documentation)
- [License](#-license)

---

## ✨ Features

- 🌍 **Global choropleth map** — coverage by country, with in-map labels and region-level filtering
- 📈 **Coverage vs. Incidence analysis** — quadrant scatter plot to flag high-priority intervention zones
- 🔎 **Country Explorer** — antigen-level breakdown and year-over-year coverage trend per country
- ⚠️ **Risk & Gaps view** — single-dose-round vaccines flagged as reinforcement candidates
- 🦠 **Disease trend tracking** — historical case counts across major vaccine-preventable diseases
- 🎯 **2030 Measles Target tracker** — live gauge showing progress against the WHO 95% target
- 🗂️ **Raw data explorer** — browse and export any base table directly from MySQL
- 📊 **9-page Power BI report** — executive-level static dashboard for offline/stakeholder use
- 🔄 **Graceful demo-data fallback** — app never breaks, even without a live DB connection

---

## 🛠 Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| **Data Source** | WHO / UNICEF datasets | Raw global vaccination & disease data |
| **Cleaning & EDA** | Python (pandas, numpy) | Data cleaning + 30 analytical questions |
| **Database** | MySQL | Normalized schema — 6 tables, 6 analytical views |
| **BI Layer** | Power BI | 9-page executive dashboard |
| **Web App** | Streamlit + Plotly | Live interactive dashboard, deployed on Streamlit Community Cloud |

---

## 🏗 Architecture

```
┌──────────────┐    ┌───────────────────┐    ┌──────────────────┐
│  5 WHO CSVs  │ →  │ Python Cleaning &  │ →  │  MySQL Database   │
│  (raw data)  │    │  EDA (Notebook)    │    │  vaccination_db   │
└──────────────┘    └───────────────────┘    │  6 tables·6 views │
                                              └─────────┬─────────┘
                                                         │
                                   ┌─────────────────────┴─────────────────────┐
                                   ▼                                           ▼
                          ┌────────────────┐                         ┌────────────────┐
                          │   Power BI      │                         │   Streamlit App │
                          │  9-page report  │                         │  (live web app) │
                          └────────────────┘                         └────────────────┘
```

---

## 📁 Folder Structure

```
vaccination-project/
├── data/
│   ├── raw/                 ← the 5 original WHO CSVs
│   └── cleaned/              ← cleaned CSVs exported from the notebook
├── notebooks/
│   └── vaccination_analysis.ipynb   ← full cleaning + EDA + 30 questions
├── sql/
│   ├── schema.sql            ← CREATE TABLE statements (6 tables)
│   ├── views.sql             ← 6 analytical views (feed Power BI + Streamlit)
│   └── load_data.py          ← loads cleaned CSVs into MySQL
├── powerbi/
│   └── vaccination_dashboard.pbix   ← 9-page Power BI report
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

---

## 🚀 Getting Started

### 1. Database Setup

The MySQL database (`vaccination_db`) is already built in MySQL Workbench — nothing to redo. This repo just gives it a portable, version-controlled home so the whole project is reproducible on any machine.

**Option A — Use your existing local DB (fastest)**
Nothing to do. Just point `.env` at it (see step 2) and both Streamlit and any fresh MySQL Workbench session will read the same `vaccination_db`.

**Option B — Make it portable / back it up into this repo**

```bash
mysqldump -u root -p vaccination_db > sql/vaccination_db_dump.sql
```

To restore it on another machine:

```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS vaccination_db"
mysql -u root -p vaccination_db < sql/vaccination_db_dump.sql
```

`schema.sql` + `views.sql` are also included separately if you ever need to rebuild the structure from scratch and repopulate it using `sql/load_data.py`.

### 2. Configure Credentials

```bash
cp .env.example .env
# edit .env with your MySQL Workbench username/password
```

### 3. Run the Streamlit App

```bash
cd streamlit_app
pip install -r requirements.txt
cp .env.example .env      # if not already done at root
streamlit run app.py
```

App opens at `http://localhost:8501`. If MySQL isn't reachable, it automatically falls back to demo data with a banner — so it always renders.

> **Just want to explore it without setup?** → **[Open the live app](https://vaccination-project-027.streamlit.app/)**

### 4. Power BI Report

Open `powerbi/vaccination_dashboard.pbix` in Power BI Desktop. It's already wired to `vaccination_db` — if you've moved databases or machines, update the source under **Home → Transform Data → Data Source Settings**.

### 5. Jupyter Notebook

`notebooks/vaccination_analysis.ipynb` — the full Python pipeline: load → clean → EDA → all 30 analytical questions → export cleaned CSVs to `data/cleaned/`.

---

## 📄 Documentation

`docs/Project_Documentation.docx` contains the complete write-up:

- Problem statement
- Data cleaning process
- Database design decisions
- Dashboard walkthrough with screenshots
- Key insights & findings
- Challenges encountered
- Deliverables checklist

---

## 📜 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

<div align="center">

---

Built with 🐍 Python · 🐬 MySQL · 📊 Power BI · ⚡ Streamlit

**[🔴 Live Demo](https://vaccination-project-027.streamlit.app/)**

</div>
