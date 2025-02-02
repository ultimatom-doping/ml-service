import pandas as pd
from app.services.question_service import get_all_questions
import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_SERVICE_URL = os.getenv("BACKEND_SERVICE_URL")

def calculate_score(row):
    if row["result"] == 'incorrect':
        score = (8 - row["difficulty_cluster"]) * (-0.25)
    elif row["result"] == 'skipped':
        score = (8 - row["difficulty_cluster"]) * (0)
    elif row["result"] == 'correct':
        score = row["difficulty_cluster"] * 1

    score = score * (row['confidence'] if row['confidence'] > 0 else 0)
    
    return score

def update_function(prev_score, new_score):
    lr = 0.1
    updated_score = prev_score*lr + new_score(1-lr)
    return updated_score

def success_evaluator_for_all(questions_ml, questions_be):
    df2 = pd.DataFrame(questions_be)
    df = pd.DataFrame(questions_ml)

    df_merged = df2.merge(df[["question_id", "difficulty_cluster", "confidence", "subject_id"]], on="question_id", how="left")

    df_merged["score"] = df_merged.apply(calculate_score, axis=1)

    student_scores = (
        df_merged
        .groupby(["student_id", "subject_id", "difficulty_cluster"])["score"]
        .mean()
        .reset_index()
        .groupby(["student_id", "subject_id"])["score"]
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
    since_time = datetime.datetime.utcnow() - datetime.timedelta(hours=24)
    since_str = since_time.isoformat()  # e.g. "2025-01-11T00:25:23.641597"

    url = BACKEND_SERVICE_URL + "/api/students/questions"
    try:
        response = requests.get(url, params={"since": since_str})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return

    data = response.json()
    questions_be = data
    
    questions_ml = await get_all_questions()
    
    scores_df = success_evaluator_for_all(questions_ml, questions_be)
    
    return scores_df    