import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

# Database connection settings
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-73854IF\\SQLEXPRESS;"
    "DATABASE=Register;"
    "Trusted_Connection=yes"
)
DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

class Measurement(Base):
    __tablename__ = "Measurement"
    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, index=True)
    humidity = Column(Float, index=True)
    pressure = Column(Float, index=True)

class SensorData(BaseModel):
    temperature: float
    humidity: float
    pressure: float

@app.post("/sensor-data/")
async def create_sensor_data(data: SensorData):
    print(f"Received data: {data}")
    try:
        db = SessionLocal()
        measurement = Measurement(
            temperature=data.temperature,
            humidity=data.humidity,
            pressure=data.pressure
        )
        db.add(measurement)
        db.commit()
        db.refresh(measurement)
        db.close()
        return measurement
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Create the table if it doesn't exist
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=8000)
