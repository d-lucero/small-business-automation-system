import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "client_intake_data.csv"
DATABASE_FILE = BASE_DIR / "client_intake.db"
REPORT_FILE = BASE_DIR / "reports" / "weekly_summary_report.csv"

def load_data():
    return pd.read_csv(DATA_FILE)

def clean_data(df):
    df["first_name"] = df["first_name"].str.title()
    df["last_name"] = df["last_name"].str.title()
    df["email"] = df["email"].str.lower()
    df["service_needed"] = df["service_needed"].str.title()
    df["county"] = df["county"].str.title()
    df["status"] = df["status"].str.title()
    df["intake_date"] = pd.to_datetime(df["intake_date"])
    return df

def save_to_database(df):
    conn = sqlite3.connect(DATABASE_FILE)
    df.to_sql("client_intake", conn, if_exists="replace", index=False)
    conn.close()

def generate_report(df):
    report = df.groupby(["service_needed", "status"]).size().reset_index(name="client_count")
    report.to_csv(REPORT_FILE, index=False)
    return report

def main():
    df = load_data()
    df = clean_data(df)
    save_to_database(df)
    report = generate_report(df)

    print("Automation completed successfully.")
    print(f"Database created: {DATABASE_FILE}")
    print(f"Report created: {REPORT_FILE}")
    print(report)

if __name__ == "__main__":
    main()
