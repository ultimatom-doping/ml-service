from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from app.services.question_service import get_all_questions
import pandas as pd
import math

def calculate_confidence_score(total_attempts):
    return min(math.log(total_attempts, 5) / 3, 1)

def update_function(prev_score, new_score):
    lr = 0.1
    updated_score = prev_score*lr + new_score(1-lr)
    return updated_score

def difficulty_calculator(questions):
    df = pd.DataFrame(questions)
    df['total_attempts'] = df['correct_attempts'] + df['incorrect_attempts'] + df['empty_attempts']
    df['difficulty'] = 1 - ((df['correct_attempts'] - df['incorrect_attempts'] * 0.25) / df['total_attempts'])

    X = df[["difficulty"]]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=9, random_state=42, n_init=10)
    df["difficulty_cluster"] = kmeans.fit_predict(X_scaled) + 1

    df["confidence"] = df["total_attempts"].apply(calculate_confidence_score)

    new_cluster_mapping = sort_difficulty_clusters(df)
    df["difficulty_cluster"] = df["difficulty_cluster"].map(new_cluster_mapping)

    return df.to_dict(orient="records")

async def trigger_job():
    questions = await get_all_questions()
    result = difficulty_calculator(questions)
    return result

def sort_difficulty_clusters(df_w_clusters):
    cluster_difficulty_means = df_w_clusters.groupby("difficulty_cluster")["difficulty"].mean()

    sorted_clusters = cluster_difficulty_means.sort_values().index
    new_cluster_mapping = {old: new for new, old in enumerate(sorted_clusters)}

    return new_cluster_mapping