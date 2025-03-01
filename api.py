from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

# Fetch DATABASE_URL from Railway environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

@app.get("/test-db")
def test_db():
    """Test database connection and fetch actual Nasdaq data."""
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM market_prices WHERE instrument = 'nasdaq' LIMIT 5;")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"status": "Success", "data": data}
    except Exception as e:
        return {"status": "Failed", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
