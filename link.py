import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import joblib

model = joblib.load('student_score_predictor.pkl')  


scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Student Form Responses').worksheet('Form Responses 1')  # your sheet name
data = sheet.get_all_records()
df = pd.DataFrame(data)
if df.empty:
    print("No data found in the Sheet.")
    exit()
latest_entry = df.iloc[-1]

columns_to_use = [
    'Age', 'Gender', 'Study Hours Per Day', 'Social Media Hours', 'Netflix Hours',
    'Part-time Job', 'Attendance Percentage', 'Sleep Hours', 'Diet Quality',
    'Exercise Frequency (days/week)', 'Parental Education Level',
    'Internet Quality', 'Mental Health Rating (out of 10)',
    'Extracurricular Participation'
]

input_data = latest_entry[columns_to_use].to_dict()
input_df = pd.DataFrame([input_data])

predicted_cgpa = model.predict(input_df)[0]

print(f"Predicted Marks: {round(predicted_cgpa, 2)}")
sheet.update_cell(len(df)+1, len(latest_entry)+2, round(predicted_cgpa, 2))  # new column after form fields
print("Prediction updated in Google Sheet!")
