import pandas as pd

# Puan hesaplama fonksiyonu
def calculate_score(row):
    if row["result"] == 'incorrect':
        score = (8 - row["cluster"]) * (-0.25)
    elif row["result"] == 'skipped':
        score = (8 - row["cluster"]) * (0)
    elif row["result"] == 'correct':
        score = row["cluster"] * 1

    # score = score / (2**row['attempt']) if score > 0 else score * (2**row['attempt'])
    score = score * (row['confidence_score'] if row['confidence_score'] > 0 else 0)
    
    return score

def success_evaluator_for_all(df2):
    df_merged = df.merge(df2[["question_id", "cluster", "confidence_score"]], on="question_id", how="left")

    # Yeni sütun olarak puanı ekleme
    df_merged["score"] = df_merged.apply(calculate_score, axis=1)
    
    # Öğrencinin ortalama puanını hesaplama
    student_scores = df_merged.groupby(["student_id", "subject", "cluster"])["score"].mean().reset_index().groupby('student_id', 'subject')['score'].sum().reset_index()

    return student_scores

    