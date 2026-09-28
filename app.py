from fastapi import FastAPI


import pickle
import numpy as np

from fastapi import FastAPI, Request, Form

from pydantic import BaseModel,Field, field_validator, model_validator, ConfigDict, computed_field


app = FastAPI(
    title="California House Price Prediction",
    description="House price prediction using Machine Learning",
    version="1.0"
)


# Load model and scaler
regmodel = pickle.load(open("regmodel.pkl", "rb"))
scalar = pickle.load(open("scailing.pkl", "rb"))


class HouseData(BaseModel):

    MedInc: float = Field(..., gt=0)
    HouseAge: float = Field(..., ge=0, le=100)
    AveRooms: float = Field(..., gt=0)
    AveBedrms: float = Field(..., gt=0)
    Population: float = Field(..., ge=0)
    AveOccup: float = Field(..., gt=0)
    Latitude: float = Field(..., ge=-90, le=90)
    Longitude: float = Field(..., ge=-180, le=180)



  ##field validator
    @field_validator("MedInc", "AveRooms", "AveBedrms", "AveOccup")
    @classmethod
    def validat_positive_value(cls,value):
      if not np.isfinite(value):
        raise ValueError("Value must be positive")
      return value
    
    
    ##model validator
    @model_validator(mode="after")
    def validate_rooms(self):
      if self.AveBedrms > self.AveRooms:
        raise ValueError("Average bedrooms can not exceed average rooms")
      return self
    
    @computed_field
    @property
    def cordinates(self) ->str:
      return f"{self.Latitude},{self.Longitude}"
    
@app.get("/")
def home():
  return{
    "message":"California House Price PRediction API is runung"
  }
  
@app.post("/predict")
def predict(data:HouseData):
  input_data = np.array([[
        data.MedInc,
        data.HouseAge,
        data.AveRooms,
        data.AveBedrms,
        data.Population,
        data.AveOccup,
        data.Latitude,
        data.Longitude
    ]])
     
  scaled_data = scalar.transform(input_data)

  prediction = regmodel.predict(scaled_data)[0]

  return {
        "prediction": float(prediction),
        "coordinates": data.cordinates
    }