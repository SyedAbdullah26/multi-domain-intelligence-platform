# Week 8 Implementation (Streamlit-ready)
from pathlib import Path
from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user
from app.data.incidents import insert_incident, get_all_incidents
import pandas as pd
import traceback


# 1. DIRECTORIES

DATA_DIR = Path("DATA")
DATA_DIR.mkdir(exist_ok=True)


# 2. CSV - DATAFRAME MAPPERS 


def map_cyber_incidents(df):
    """Convert messy CSV into cyber_incidents-compatible DataFrame."""
    mapped_rows = []
    
    for _, row in df.iterrows():
        mapped_rows.append({
            "date_reported": row.get("Date", "2024-01-01"),
            "incident_type": row.get("Type", "Unknown"),
            "severity": "Medium",       # default value
            "status": "Open",           # default value
            "description": f"{row.get('Title', '')} - {row.get('Description', '')}",
            "reported_by": "System"
        })
    
    return pd.DataFrame(mapped_rows)


def map_datasets_metadata(df):
    """Map dataset metadata CSV → table format."""
    mapped_rows = []
    
    for _, row in df.iterrows():
        mapped_rows.append({
            "dataset_name": row.get("dataset_name", "Unknown Dataset"),
            "source": row.get("source_organization", "Unknown"),
            "record_count": 0,
            "last_updated": row.get("last_updated", "2024-01-01"),
            "description": row.get("description", "No description")
        })
    
    return pd.DataFrame(mapped_rows)


def map_it_tickets(df):
    """Map IT tickets into consistent table format."""
    mapped_rows = []
    
    for i, row in df.iterrows():
        mapped_rows.append({
            "ticket_id": f"TICKET_{i + 1000}",
            "date_created": "2024-01-01",
            "priority": row.get("Category", "Medium"),
            "status": "Open",
            "description": row.get("Customer Input", "No description"),
            "assigned_to": "Unassigned"
        })
    
    return pd.DataFrame(mapped_rows)


# Mapper dictionary for easier extension
MAPPERS = {
    "cyber_incidents": map_cyber_incidents,
    "datasets_metadata": map_datasets_metadata,
    "it_tickets": map_it_tickets,
}

# 3. LOAD ALL CSV FILES

def load_all_csv_data(conn):
    """Loads all CSVs into the database with flexible mapping functions."""
    
    csv_files = {
        "cyber_incidents.csv": "cyber_incidents",
        "datasets_metadata.csv": "datasets_metadata",
        "it_tickets.csv": "it_tickets",
    }

    total_rows = 0
    
    for file_name, table_name in csv_files.items():
        csv_path = DATA_DIR / file_name
        
        if not csv_path.exists():
            print(f"⚠️ CSV missing: {file_name}")
            continue
        
        try:
            print(f"\n📥 Loading {file_name} ...")
            df_raw = pd.read_csv(csv_path)

            print(f"🔎 Raw columns: {list(df_raw.columns)}")

            # Use the mapper to convert CSV → database-ready DF
            df_mapped = MAPPERS[table_name](df_raw)

            # Save to SQL
            df_mapped.to_sql(table_name, conn, if_exists="replace", index=False)

            total_rows += len(df_mapped)
            print(f" Loaded {len(df_mapped)} rows into {table_name}")

        except Exception as e:
            print(f" Error loading {file_name}: {e}")
            traceback.print_exc()

    return total_rows

# 4. FULL DATABASE SETUP


def setup_database_complete():
    print("\n" + "="*70)
    print(" STARTING COMPLETE DATABASE SETUP")
    print("="*70)

    conn = connect_database()

    # Create all tables
    create_all_tables(conn)

    # Load CSV data
    total = load_all_csv_data(conn)
    print(f"\n TOTAL ROWS IMPORTED FROM CSV: {total}")

    # Summary
    cursor = conn.cursor()
    tables = ["users", "cyber_incidents", "datasets_metadata", "it_tickets"]

    print("\n TABLE SUMMARY:")
    for t in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {t}")
        print(f"  • {t}: {cursor.fetchone()[0]} rows")

    conn.close()
    print("\n DATABASE SETUP COMPLETE!")
    print("="*70)


# 5. DEMO OPERATIONS (kept separate so Streamlit can call them later)


def demo_operations():
    """Demonstration only—will not run in Streamlit app."""
    print("\n--- USER AUTH TEST ---")
    print(register_user("alice", "SecurePass123!", "analyst"))
    print(login_user("alice", "SecurePass123!"))

    print("\n--- INSERT INCIDENT TEST ---")
    incident_id = insert_incident(
        "2024-11-05", "Phishing", "High", "Open", "Test incident", "alice"
    )
    
    print(f"✔ Created Incident #{incident_id}")

    df = get_all_incidents()
    print(f"Total incidents in DB: {len(df)}")

# 6. MAIN ENTRY

def main():
    setup_database_complete()
    demo_operations()


if __name__ == "__main__":
    main()
