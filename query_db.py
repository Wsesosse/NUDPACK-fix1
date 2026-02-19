import os
import sys

# Add the project root to sys.path so we can import 'server' module
sys.path.append(os.getcwd())

from sqlalchemy import text, inspect
from server.app.db import SessionLocal, engine
from server.app.models import Parcel, CarrierList, User, QueueReservation, QueueSection, DailyCounter

def query_db():
    print("=========================================")
    print("      NUDPACK Database Query Tool       ")
    print("=========================================")
    
    db = SessionLocal()
    inspector = inspect(engine)
    
    try:
        # Show Summary
        print("\n--- Summary ---")
        try:
            with engine.connect() as conn:
                tables = inspector.get_table_names()
                available_tables = []
                for table in tables:
                    if table == "sqlite_sequence": continue
                    count_q = text(f"SELECT COUNT(*) FROM {table}")
                    count = conn.execute(count_q).scalar()
                    print(f"- {table}: {count} rows")
                    available_tables.append(table)
        except Exception as e:
            print(f"Error fetching summary: {e}")

        while True:
            print("\n------------------------------")
            print("Select an option:")
            print("1. View recent Parcels (Last 20)")
            print("2. View Carriers")
            print("3. View Users")
            print("4. View Queue Reservations (Today)")
            print("5. Execute Custom SQL")
            print("q. Quit")
            
            choice = input("Enter choice: ").strip()
            
            if choice == "1":
                parcels = db.query(Parcel).order_by(Parcel.id.desc()).limit(20).all()
                if not parcels:
                    print("No parcels found.")
                else:
                    print(f"Showing last {len(parcels)} parcels:")
                    print(f"{'ID':<5} {'Tracking':<20} {'Status':<15} {'Queue':<10} {'Recipient':<20} {'Unofficial Recipient'}")
                    print("-" * 90)
                    for p in parcels:
                        print(f"{p.id:<5} {p.tracking_number:<20} {p.status:<15} {p.queue_number or '-':<10} {p.recipient_name or '-':<20} {p.unofficial_recipient or '-'}")

            elif choice == "2":
                carriers = db.query(CarrierList).all()
                print(f"{'ID':<5} {'Name'}")
                print("-" * 30)
                for c in carriers:
                    print(f"{c.carrier_id:<5} {c.carrier_name}")

            elif choice == "3":
                users = db.query(User).all()
                print(f"{'ID':<5} {'Name':<20} {'CarrierID'}")
                print("-" * 40)
                for u in users:
                    print(f"{u.id:<5} {u.name:<20} {u.carrier_id}")

            elif choice == "4":
                today = datetime.now().strftime("%Y%m%d") # Basic check, timezone might differ but good enough for query tool
                reservations = db.query(QueueReservation).order_by(QueueReservation.id.desc()).limit(20).all()
                print(f"Showing last 20 reservations:")
                print(f"{'ID':<5} {'Section':<10} {'Status':<10} {'CurrentSeq':<10} {'Date':<10}")
                print("-" * 60)
                for r in reservations:
                    # simplistic check
                    print(f"{r.id:<5} {r.start_seq}-{r.end_seq:<6} {r.status:<10} {r.current_seq:<10} {r.date:<10}")

            elif choice == "5":
                sql = input("SQL Query: ")
                try:
                    with engine.connect() as conn:
                        result = conn.execute(text(sql))
                        try:
                            if result.returns_rows:
                                rows = result.fetchall()
                                if rows:
                                    print(f"Result ({len(rows)} rows):")
                                    print(rows)
                                else:
                                    print("No rows returned.")
                            else:
                                conn.commit() # For update/delete/insert
                                print(f"Executed successfully. Rows affected: {result.rowcount}")
                        except Exception as e:
                             print(f"Executed. Info: {e}")

                except Exception as e:
                    print(f"SQL Error: {e}")

            elif choice.lower() == "q":
                print("Exiting...")
                break
            else:
                print("Invalid choice.")
                
    finally:
        db.close()

if __name__ == "__main__":
    from datetime import datetime
    query_db()
