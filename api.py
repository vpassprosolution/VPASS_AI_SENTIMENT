from fastapi import FastAPI
from storyline_generator import generate_storyline

app = FastAPI()

@app.get("/storyline/{instrument}")
def get_storyline(instrument: str):
    """API endpoint to fetch the financial storyline for a given instrument."""
    storyline = generate_storyline(instrument.lower())
    return {"instrument": instrument, "storyline": storyline}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
 
