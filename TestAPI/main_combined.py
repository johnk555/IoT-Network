import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
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

class Sensor(Base):
    __tablename__ = "Sensor"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String, index=True)
    model = Column(String, index=True)
    firmware_version = Column(String, index=True)
    manufacturer = Column(String, index=True)

class Measurement(Base):
    __tablename__ = "Measurement"
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey('Sensor.id'))
    temperature = Column(Float, index=True)
    humidity = Column(Float, index=True)
    pressure = Column(Float, index=True)

    sensor = relationship("Sensor")

class CombinedData(BaseModel):
    temperature: float
    humidity: float
    pressure: float
    name: str
    brand: str
    model: str
    firmware_version: str
    manufacturer: str

@app.post("/sensor-combined-data/")
async def create_combined_data(data: CombinedData):
    print(f"Received data: {data}")
    try:
        db = SessionLocal()
        
        # Δημιουργία και αποθήκευση του αισθητήρα
        sensor = Sensor(
            name=data.name,
            brand=data.brand,
            model=data.model,
            firmware_version=data.firmware_version,
            manufacturer=data.manufacturer
        )
        db.add(sensor)
        db.commit()
        db.refresh(sensor)
        print(f"Sensor saved: {sensor.id}")
        
        # Δημιουργία και αποθήκευση της μέτρησης
        measurement = Measurement(
            temperature=data.temperature,
            humidity=data.humidity,
            pressure=data.pressure,
            sensor_id=sensor.id
        )
        db.add(measurement)
        db.commit()
        db.refresh(measurement)
        print(f"Measurement saved: {measurement.id}")
        
        db.close()
        return {"sensor": sensor, "measurement": measurement}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Δημιουργία των πινάκων αν δεν υπάρχουν
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=8000)
