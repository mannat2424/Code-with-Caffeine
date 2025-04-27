from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# Initialize FastAPI app
app = FastAPI()

# Load your trained model
model = joblib.load('model/student_score_predictor.pkl')

# Define what input the model expects
class StudentData(BaseModel):
    age: int
    gender: str
    study_hours_per_day: float
    social_media_hours: float
    netflix_hours: float
    part_time_job: str
    attendance_percentage: float
    sleep_hours: float
    diet_quality: str
    exercise_frequency: int
    parental_education_level: str
    internet_quality: str
    mental_health_rating: int
    extracurricular_participation: str
    exam_score: float = None

@app.post("/predict")
def predict(data: StudentData):
    # Convert input to DataFrame
    input_data = pd.DataFrame([data.dict()])
    
    # Make prediction
    prediction = model.predict(input_data)[0]
    
    # Respond
    return {
        "predicted_cgpa": round(prediction, 2),
        "advice": generate_advice(input_data)
    }

def generate_advice(data):
    advice = []
    if data['attendance_percentage'][0] < 75:
        advice.append("Improve attendance to boost performance.")
    if data['study_hours_per_day'][0] < 3:
        advice.append("Increase study time daily.")
    if data['social_media_hours'][0] > 3:
        advice.append("Reduce social media usage.")
    if data['sleep_hours'][0] < 6:
        advice.append("Improve sleep schedule for better focus.")
    return advice