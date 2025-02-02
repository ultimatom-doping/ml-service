import pandas as pd
from app.services.question_service import get_all_questions
import datetime
import requests

# Puan hesaplama fonksiyonu
def calculate_score(row):
    if row["result"] == 'incorrect':
        score = (8 - row["difficulty_cluster"]) * (-0.25)
    elif row["result"] == 'skipped':
        score = (8 - row["difficulty_cluster"]) * (0)
    elif row["result"] == 'correct':
        score = row["difficulty_cluster"] * 1

    # score = score / (2**row['attempt']) if score > 0 else score * (2**row['attempt'])
    score = score * (row['confidence'] if row['confidence'] > 0 else 0)
    
    return score

def success_evaluator_for_all(questions_ml, questions_be):
    df2 = pd.DataFrame(questions_be)
    df = pd.DataFrame(questions_ml)

    df_merged = df2.merge(df[["question_id", "difficulty_cluster", "confidence", "subject_id"]], on="question_id", how="left")

    # Yeni sütun olarak puanı ekleme
    df_merged["score"] = df_merged.apply(calculate_score, axis=1)
    
    # Öğrencinin ortalama puanını hesaplama
    # Pass a list of columns to the second groupby
    student_scores = (
        df_merged
        .groupby(["student_id", "subject_id", "difficulty_cluster"])["score"]
        .mean()
        .reset_index()
        .groupby(["student_id", "subject_id"])["score"]  # ✅ Provide columns in a list
        .sum()
        .reset_index()
    )

    return student_scores

async def trigger_job():
    """
    1. Computes timestamp for 24 hours ago (UTC).
    2. Makes GET request to /api/students/questions?since=...
    3. Uses the returned JSON to do something, e.g., call success_evaluator_for_all.
    """
    # 1. Compute 'since' time (24 hours prior to now, in UTC)
    since_time = datetime.datetime.utcnow() - datetime.timedelta(hours=24)
    since_str = since_time.isoformat()  # e.g. "2025-01-11T00:25:23.641597"

    # 2. Make the GET request
    url = "http://host.docker.internal:8000/api/students/questions"
    try:
        response = requests.get(url, params={"since": since_str})
        response.raise_for_status()  # will raise an error if the status code isn't 200
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return

    # 3. Parse the returned JSON
    data = response.json()  # This should be a list of dicts
    
    # For demonstration, we'll assume:
    #    "questions_ml" is the data we just received
    #    "questions_be" is the same data or different data from somewhere else
    # If you only have one data source, you can adapt as needed.
    
    questions_be = data  # or a separate endpoint; just using the same for example
    
    questions_ml = await get_all_questions()
    
    # 4. Evaluate
    scores_df = success_evaluator_for_all(questions_ml, questions_be)
    
    # Optionally, return it if you need the DataFrame
    return scores_df    