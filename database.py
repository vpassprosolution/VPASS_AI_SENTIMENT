import psycopg2

# PostgreSQL Database Configuration
DB_CONFIG = {
    "dbname": "news_db",
    "user": "postgres",
    "password": "Didie555363!",
    "host": "localhost",
    "port": "5432"
}

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
    """Establish connection to PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def fetch_latest_data(table, instrument, date_column, limit=1):
    """Fetch latest data from a specific table for a given instrument."""
    conn = connect_db()
    if not conn:
        return None

    cursor = conn.cursor()
    instrument_name = INSTRUMENTS.get(instrument.lower(), instrument).lower()

    # Debug: Print the actual query and instrument being used
    print(f"Fetching data from table: {table}, for instrument: {instrument_name}")

    query = f"""
        SELECT * FROM {table}
        WHERE LOWER(instrument) = %s
        ORDER BY {date_column} DESC
        LIMIT %s
    """
    cursor.execute(query, (instrument_name, limit))
    data = cursor.fetchall()

    # Debug: Print the fetched data
    print(f"Data fetched from {table} for {instrument_name}: {data}")

    cursor.close()
    conn.close()
    return data if data else None

def fetch_all_data(instrument):
    """Fetch latest data from all 5 tables for a given instrument."""
    instrument_name = INSTRUMENTS.get(instrument.lower(), instrument).lower()
    print(f"Fetching all data for: {instrument_name}")

    return {
        "market_prices": fetch_latest_data("market_prices", instrument_name, "timestamp", limit=1),
        "news_articles": fetch_latest_data("news_articles", instrument_name, "published_at", limit=3),
        "news_risks": fetch_latest_data("news_risks", instrument_name, "timestamp", limit=1),
        "price_predictions": fetch_latest_data("price_predictions", instrument_name, "timestamp", limit=1),
        "trade_recommendations": fetch_latest_data("trade_recommendations", instrument_name, "timestamp", limit=1),
    }

if __name__ == "__main__":
    # Example test: Fetch all data for Nasdaq using lowercase names
    instrument = "nasdaq"
    full_data = fetch_all_data(instrument)
    print("Nasdaq Data:", full_data)
