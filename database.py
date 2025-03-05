import os
import psycopg2
from urllib.parse import urlparse

# Use the correct DATABASE_URL from Railway
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:vVMyqWjrqgVhEnwyFifTQxkDtPjQutGb@interchange.proxy.rlwy.net:30451/railway")

# Financial Instruments to Track (Database uses lowercase names)
INSTRUMENTS = {
    "gold": "gold",
    "bitcoin": "bitcoin",
    "ethereum": "ethereum",
    "dow jones": "dow jones",
    "nasdaq": "nasdaq",
    "eur/usd": "eur/usd",
    "gbp/usd": "gbp/usd"
}

def connect_db():
    """Establish connection to PostgreSQL database using DATABASE_URL."""
    try:
        if DATABASE_URL:
            result = urlparse(DATABASE_URL)
            conn = psycopg2.connect(
                dbname=result.path.lstrip('/'),
                user=result.username,
                password=result.password,
                host=result.hostname,
                port=result.port,
                sslmode="require"
            )
            print("✅ Database connection successful")
            return conn
        else:
            raise Exception("DATABASE_URL not found in environment variables")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def fetch_latest_data(table, instrument, date_column, limit=5):
    """Fetch latest data from a specific table for a given instrument."""
    conn = connect_db()
    if not conn:
        return None

    cursor = conn.cursor()

# Ensure "dow-jones" is converted correctly to match database format
if instrument.lower() == "dow-jones":
    instrument_name = "dow jones"  # ✅ Correctly formatted for database
else:
    instrument_name = INSTRUMENTS.get(instrument.lower(), instrument,).lower()  # ✅ Properly get instrument name

print(f"🔍 Fetching {limit} records from table: {table}, for instrument: {instrument_name}")

query = f"""
    SELECT * FROM {table}
    WHERE LOWER(instrument) = %s
    ORDER BY {date_column} DESC
    LIMIT %s
"""
    cursor.execute(query, (instrument_name, limit))
    data = cursor.fetchall()
    print(f"✅ Data fetched from {table} for {instrument_name}: {data}")

    cursor.close()
    conn.close()
    return data if data else None

def fetch_all_data(instrument):
    """Fetch latest data from all tables for a given instrument."""
    instrument_name = INSTRUMENTS.get(instrument.lower(), instrument).lower()
    print(f"Fetching all data for: {instrument_name}")

    return {
        "market_prices": fetch_latest_data("market_prices", instrument_name, "timestamp", limit=1),
        "news_articles": fetch_latest_data("news_articles", instrument_name, "published_at", limit=5),  # Ensure 5 news articles
        "news_risks": fetch_latest_data("news_risks", instrument_name, "timestamp", limit=1),
        "price_predictions": fetch_latest_data("price_predictions", instrument_name, "timestamp", limit=1),
        "trade_recommendations": fetch_latest_data("trade_recommendations", instrument_name, "timestamp", limit=1),
    }

if __name__ == "__main__":
    # Example test: Fetch all data for Nasdaq using lowercase names
    instrument = "nasdaq"
    full_data = fetch_all_data(instrument)
    print("Nasdaq Data:", full_data)
