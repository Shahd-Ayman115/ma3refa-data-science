from fastapi import FastAPI
from pydantic import BaseModel
from typing import List


app = FastAPI()


# =========================================================
# DATA MODELS
# =========================================================

class Answer(BaseModel):
    topic: str
    is_correct: bool


class Quiz(BaseModel):
    quiz_id: int
    subcategory: str
    difficulty: int
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
    # -----------------------------------------

    topic_performance.sort(
        key=lambda x: x["accuracy"]
    )

    weakest_topics = topic_performance[:3]


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
            difficulty  = "hard"


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
    request: RecommendationRequest
):

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
