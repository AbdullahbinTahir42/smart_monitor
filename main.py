import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv

# 1. Load Keys
load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# 2. Connect to Supabase
supabase: Client = create_client(url, key)

app = FastAPI()

# 3. Data Schema
class ReadingSchema(BaseModel):
    voltage: float
    current: float
    power: float
    temperature: float
    humidity: float
    source: str

@app.get("/")
def home():
    return {"message": "VoltSense API is connected to Supabase!"}

# POST: Save Data
@app.post("/readings/")
def create_reading(reading: ReadingSchema):
    # Prepare data dictionary
    data = {
        "voltage": reading.voltage,
        "current": reading.current,
        "power": reading.power,
        "temperature": reading.temperature,
        "humidity": reading.humidity,
        "source": reading.source
    }
    
    # Insert into Supabase 'sensor_readings' table
    try:
        response = supabase.table("sensor_readings").insert(data).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# GET: Fetch Data
@app.get("/readings/")
def get_readings():
    # Fetch last 10 readings
    response = supabase.table("sensor_readings").select("*").order("timestamp", desc=True).limit(10).execute()
    return response.data