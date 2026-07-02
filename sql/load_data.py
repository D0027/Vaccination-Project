"""
Loads the cleaned CSVs (exported from the Kaggle notebook) into the
vaccination_db MySQL database.

Usage:
    1. Put the 5 cleaned CSVs in data/cleaned/  (already done if you
       downloaded them from Kaggle's /kaggle/working/cleaned_data/)
    2. Copy .env.example -> .env and fill in your MySQL credentials
    3. Run:  python sql/load_data.py
"""
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("MYSQL_USER", "root")
PWD = os.getenv("MYSQL_PASSWORD", "")
HOST = os.getenv("MYSQL_HOST", "localhost")
PORT = os.getenv("MYSQL_PORT", "3306")
DB = os.getenv("MYSQL_DB", "vaccination_db")

engine = create_engine(f"mysql+pymysql://{USER}:{PWD}@{HOST}:{PORT}/{DB}")

CLEANED = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned")

FILES = {
    "coverage_data": "coverage_data_cleaned.csv",
    "incidence_rate": "incidence_rate_cleaned.csv",
    "reported_cases": "reported_cases_cleaned.csv",
    "vaccine_introduction": "vaccine_introduction_cleaned.csv",
    "vaccine_schedule": "vaccine_schedule_cleaned.csv",
}

def build_countries_table():
    """Derives the countries reference table from whichever source has iso/region."""
    intro = pd.read_csv(os.path.join(CLEANED, FILES["vaccine_introduction"]))
    cols = {c.lower(): c for c in intro.columns}
    iso_col = next(c for c in intro.columns if "iso" in c.lower())
    name_col = next(c for c in intro.columns if "country" in c.lower() and "name" in c.lower())
    region_col = next(c for c in intro.columns if "who" in c.lower() or "region" in c.lower())
    countries = intro[[iso_col, name_col, region_col]].drop_duplicates()
    countries.columns = ["iso_3_code", "country_name", "who_region"]
    countries.dropna(subset=["iso_3_code"], inplace=True)
    return countries

def main():
    print(f"Connecting to MySQL: {HOST}:{PORT}/{DB} as {USER}")

    countries = build_countries_table()
    countries.to_sql("countries", engine, if_exists="append", index=False,
                      method="multi", chunksize=1000)
    print(f"  countries              loaded ({len(countries):,} rows)")

    for table, fname in FILES.items():
        path = os.path.join(CLEANED, fname)
        if not os.path.exists(path):
            print(f"  ⚠️  Skipped {table} — {fname} not found in data/cleaned/")
            continue
        df = pd.read_csv(path)
        df.to_sql(table, engine, if_exists="append", index=False,
                   method="multi", chunksize=2000)
        print(f"  {table:<22} loaded ({len(df):,} rows)")

    print("\n✅ Done. Now run sql/views.sql in MySQL Workbench (or via CLI) to build the analytical views.")

if __name__ == "__main__":
    main()
