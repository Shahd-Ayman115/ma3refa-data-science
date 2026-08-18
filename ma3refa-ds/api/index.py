import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List


app = FastAPI()
DS_SECRET = os.getenv("DS_SECRET")


# =========================================================
# DATA MODELS
# =========================================================

class Answer(BaseModel):
    topic: str
    is_correct: bool


class Quiz(BaseModel):
    quiz_id: int
    subcategory: str
    difficulty: str
    answers: List[Answer]


class RecommendationRequest(BaseModel):
    student_id: int
    recent_quizzes: List[Quiz]


# =========================================================
# HOME
# =========================================================

@app.get("/api")
def home():
    return {
        "message": "Data Science API is running"
    }


# =========================================================
# RECOMMENDATION LOGIC
# =========================================================

def recommend_quizzes(recent_quizzes):

    topic_stats = {}

    # -----------------------------------------
    # Analyze the last 5 quizzes
    # -----------------------------------------

    for quiz in recent_quizzes:

        for answer in quiz.answers:

            topic = answer.topic

            if topic not in topic_stats:
                topic_stats[topic] = {
                    "correct": 0,
                    "total": 0,
                    "subcategory": quiz.subcategory
                }

            topic_stats[topic]["total"] += 1

            if answer.is_correct:
                topic_stats[topic]["correct"] += 1


    # -----------------------------------------
    # Calculate accuracy for every topic
    # -----------------------------------------

    topic_performance = []

    for topic, data in topic_stats.items():

        accuracy = data["correct"] / data["total"]

        topic_performance.append({
            "topic": topic,
            "subcategory": data["subcategory"],
            "accuracy": accuracy,
            "correct": data["correct"],
            "total": data["total"]
        })


    # -----------------------------------------
    # Find weakest topics
    # Maximum 2 recommendations per subcategory
    # Maximum 3 recommendations overall
    # -----------------------------------------

    topic_performance.sort(
        key=lambda x: x["accuracy"]
    )

    weakest_topics = []
    subcategory_counts = {}

    for topic in topic_performance:

        subcategory = topic["subcategory"]

        # Skip if this subcategory already has 2 recommendations
        if subcategory_counts.get(subcategory, 0) >= 2:
            continue

        weakest_topics.append(topic)

        subcategory_counts[subcategory] = (
            subcategory_counts.get(subcategory, 0) + 1
        )

        # Stop after 3 recommendations
        if len(weakest_topics) == 3:
            break


    # -----------------------------------------
    # Create recommendations
    # -----------------------------------------

    recommendations = []

    for topic in weakest_topics:

        accuracy = topic["accuracy"]

        # Difficulty decision
        if accuracy < 0.40:
            difficulty = "easy"

        elif accuracy < 0.70:
            difficulty = "medium"

        else:
            difficulty = "hard"

        recommendations.append({
            "subcategory": topic["subcategory"],
            "topic": topic["topic"],
            "difficulty": difficulty
        })


    return recommendations


# =========================================================
# RECOMMENDATION API
# =========================================================

@app.post("/api/recommendations")
def get_recommendations(
    request: RecommendationRequest,
    x_api_key: str = Header(None)
):

    # Check shared secret
    if x_api_key != DS_SECRET:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    # Take the latest 5 quizzes
    recent_quizzes = request.recent_quizzes[-5:]

    # Run recommendation system
    recommendations = recommend_quizzes(
        recent_quizzes
    )

    # Return recommendations
    return {
        "student_id": request.student_id,
        "recommendations": recommendations
    }
