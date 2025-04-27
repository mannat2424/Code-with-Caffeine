import joblib
import pandas as pd
label_encoders = joblib.load('C:/Users/abhis/OneDrive/Desktop/cs/hackowasp project/model/label_encoders.pkl')
model = joblib.load('C:/Users/abhis/OneDrive/Desktop/cs/hackowasp project/model/student_score_predictor.pkl')

cols = ['gender','part_time_job', 'diet_quality', 
        'internet_quality', 'parental_education_level',
        'extracurricular_participation']

def preprocess_input(user_input_dict):
    df = pd.DataFrame([user_input_dict])
    for col in cols:
        if col in df:
            le = label_encoders[col]
            df[col] = le.transform(df[col])
    return df.values.tolist()[0]

def predict_exam_score(user_input_dict):
    input_features = preprocess_input(user_input_dict)
    prediction = model.predict([input_features])
    return prediction[0]


improvement_suggestions = {
    'study_hours_per_day': {
        'condition': lambda x: x < 3,
        'suggestion': "Try to study at least 3 hours a day."
    },
    'social_media_hours': {
        'condition': lambda x: x > 3,
        'suggestion': "Reduce time on social media to under 3 hours daily."
    },
    'netflix_hours': {
        'condition': lambda x: x > 2,
        'suggestion': "Limit Netflix or streaming to under 2 hours daily."
    },
    'sleep_hours': {
        'condition': lambda x: x < 6,
        'suggestion': "Make sure you're getting at least 6 hours of sleep."
    },
    'exercise_frequency': {
        'condition': lambda x: x < 2,
        'suggestion': "Try to exercise at least twice a week."
    },
    'attendance_percentage': {
        'condition': lambda x: x < 75,
        'suggestion': "Increase your class attendance to at least 75%."
    },
    'mental_health_rating': {
        'condition': lambda x: x < 5,
        'suggestion': "Focus on improving your mental health. Consider stress-relief activities."
    },
    'part_time_job': {
        'condition': lambda x: x.strip().lower() == 'yes',
        'suggestion': "Reconsider part-time job hours to make more time for studies."
    },
    'diet_quality': {
        'condition': lambda x: x.strip().lower() == 'poor',
        'suggestion': "Work on improving your diet eat more nutritious meals."
    },
    'internet_quality': {
        'condition': lambda x: x.strip().lower() == 'poor',
        'suggestion': "Upgrade your internet if possible for smoother study sessions."
    },
    'extracurricular_participation': {
        'condition': lambda x: x.strip().lower() == 'no',
        'suggestion': "Join extracurricular activities to boost confidence and discipline."
    }
}


def suggest_improvements(student_input, predicted_score, desired_score=90):
    try:
        desired_score = float(desired_score)
        predicted_score = float(predicted_score)
        suggestions = []
        
        if predicted_score >= desired_score:
            return ["You're already meeting your goal! Maintain these habits."]
        
        # Convert all string inputs to lowercase for consistent comparison
        normalized_input = {k: v.lower() if isinstance(v, str) else v 
                          for k, v in student_input.items()}
        
        for habit, rule in improvement_suggestions.items():
            if habit in normalized_input:
                if rule['condition'](normalized_input[habit]):
                    suggestions.append(rule['suggestion'])
        
        if not suggestions:
            suggestions.append("Your habits are good! Small tweaks could help reach your goal.")
            
        return suggestions
    
    except Exception as e:
        return [f" Suggestion generation error: {str(e)}"]