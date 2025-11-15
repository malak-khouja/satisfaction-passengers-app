from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel, Field
import joblib
import uvicorn 
import json
import os
import pandas as pd
from enum import Enum
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta

# Charger le modèle, le scaler et l’ordre des colonnes
model = joblib.load(os.path.join("../models", "satisfaction_knn_model.joblib"))
scaler = joblib.load(os.path.join("../models", "scaler.joblib"))
with open(os.path.join("../models", "feature_order.json"), "r") as f:
    feature_order = json.load(f)

# Enums pour champs catégoriels
class TravelClass(str, Enum):
    eco = "Eco"
    eco_plus = "Eco Plus"
    business = "Business"

class TravelType(str, Enum):
    business = "Business travel"
    personal = "Personal Travel"

class CustomerType(str, Enum):
    loyal = "Loyal Customer"
    disloyal = "disloyal Customer"

# Modèle de données attendu dans l’API
class Passenger(BaseModel):
    Age: int
    Class: TravelClass
    Type_of_Travel: TravelType
    Customer_Type: CustomerType
    Flight_Distance: int = Field(..., ge=0)
    Online_boarding: int = Field(..., ge=0, le=5)
    Seat_comfort: int = Field(..., ge=0, le=5)
    Inflight_entertainment: int = Field(..., ge=0, le=5)
    On_board_service: int = Field(..., ge=0, le=5)
    Leg_room_service: int = Field(..., ge=0, le=5)
    Cleanliness: int = Field(..., ge=0, le=5)

# Création de l’app FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGO_DETAILS = "mongodb://localhost:27017" 
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.passenger_satisfaction
passenger_collection = database.get_collection("passengers")

@app.get("/")
async def root():
    return {"message": "FastAPI with MongoDB is working!"}

#crud passenger
@app.post("/add_passenger/")
async def add_passenger(passenger: Passenger):
    passenger_dict = passenger.dict()
    pred = predict(passenger)["predicted_satisfaction"]
    passenger_dict["predicted_satisfaction"] = int(pred)
    passenger_dict["date"] = datetime.utcnow()
    result = await passenger_collection.insert_one(passenger_dict)
    passenger_dict["_id"] = str(result.inserted_id)
    return {"passenger": passenger_dict}

@app.get("/passengers/")
async def get_passengers():
    passengers = []
    async for p in passenger_collection.find():
        p["_id"] = str(p["_id"])
        passengers.append(p)
    return passengers

@app.get("/passengers/{id}")
async def get_passenger(id: str):
    passenger = await passenger_collection.find_one({"_id": ObjectId(id)})
    if passenger:
        passenger["_id"] = str(passenger["_id"])
        return passenger
    raise HTTPException(status_code=404, detail="Passenger not found")

"""
@app.put("/passengers/{id}")
async def update_passenger(id: str, data: Passenger):
    update_result = await passenger_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": data.dict()}
    )
    if update_result.modified_count == 1:
        return {"message": "Passenger updated successfully"}
    raise HTTPException(status_code=404, detail="Passenger not found")

@app.delete("/passengers/{id}")
async def delete_passenger(id: str):
    delete_result = await passenger_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Passenger deleted successfully"}
    raise HTTPException(status_code=404, detail="Passenger not found")
"""

#predict satisfaction
@app.post("/predict")
def predict(data: Passenger):
    try:
        Feature = {
            'Age': data.Age,
            'Class_Business': 1 if data.Class == "Business" else 0,
            'Class_Eco': 1 if data.Class == "Eco" else 0,
            'Class_Eco Plus': 1 if data.Class == "Eco Plus" else 0,
            'Type of Travel_Business travel': 1 if data.Type_of_Travel == "Business travel" else 0,
            'Customer Type_Loyal Customer': 1 if data.Customer_Type == "Loyal Customer" else 0,
            'Flight Distance': data.Flight_Distance,
            'Online boarding': data.Online_boarding,
            'Seat comfort': data.Seat_comfort,
            'Inflight entertainment': data.Inflight_entertainment,
            'On-board service': data.On_board_service,
            'Leg room service': data.Leg_room_service,
            'Cleanliness': data.Cleanliness
        }

        df = pd.DataFrame([Feature])
        df[['Age', 'Flight Distance']] = scaler.transform(df[['Age', 'Flight Distance']])
        df = df[feature_order]
        prediction = model.predict(df)[0]
        return {"predicted_satisfaction": int(prediction)}

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing feature: {e}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Value error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
#predict satisfaction
@app.get("/metrics/overview")
async def metrics_overview():
    # Total passagers
    total = await passenger_collection.count_documents({})
    # % satisfaits
    satisfied = await passenger_collection.count_documents({"predicted_satisfaction": 1})
    satisfied_pct = round(satisfied / total, 4) if total > 0 else 0
    # Moyenne satisfaction dernier mois
    one_month_ago = datetime.utcnow() - timedelta(days=30)
    cursor = passenger_collection.find({"_id": {"$exists": True}, "date": {"$gte": one_month_ago}})
    recent = []
    async for p in cursor:
        if "predicted_satisfaction" in p:
            recent.append(p["predicted_satisfaction"])
    avg_last_month = round(sum(recent)/len(recent), 3) if recent else 0
    # Passagers à risque :
    at_risk = await passenger_collection.count_documents({"predicted_satisfaction": 0})

    return {
        "total": total,
        "satisfied_pct": satisfied_pct,
        "avg_last_month": avg_last_month,
        "at_risk": at_risk
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
