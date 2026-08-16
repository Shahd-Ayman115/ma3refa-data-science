# Ma3refa Data Science

## Overview

This repository contains the Data Science component of **Ma3refa**, an AI-powered smart assessment and learning platform.

The Data Science component focuses on analyzing student quiz performance and providing personalized quiz recommendations based on the student's weakest topics.

## Technologies & Libraries

* Python
* FastAPI
* Pydantic
* Uvicorn
* Jupyter Notebook
* Vercel

## Project Structure

```text
ma3refa-data-science/
│
├── ma3refa-ds/
│   ├── api/
│   │   └── index.py
│   │
│   ├── requirements.txt
│   ├── vercel.json
│   └── Data__Analysis.ipynb
│
├── datasets/
│   ├── users.csv
│   ├── categories.csv
│   ├── subcategories.csv
│   ├── user_subcategory_points.csv
│   ├── quizzes.csv
│   ├── answers.csv
│   └── allowed_topics.csv
│
└── README.md
```

### Files and Folders

* **`Data__Analysis.ipynb`**
  Contains the data analysis and exploration of student quiz performance.

* **`api/index.py`**
  Contains the FastAPI application and recommendation system logic.

* **`requirements.txt`**
  Contains the Python dependencies required to run the API.

* **`vercel.json`**
  Contains the configuration used to deploy the API on Vercel.

* **`datasets/`**
  Contains the synthetic datasets used for data analysis, development, testing, and demonstration.

## Data Analysis

The data analysis focuses on student quiz performance, including:

* Quiz scores
* Categories and subcategories
* Student performance
* Topic-level performance
* Quiz completion
* Identification of weak topics

The analysis is documented in `Data__Analysis.ipynb`.

The analysis was performed using synthetic datasets created for development, testing, and demonstration purposes.

## Recommendation System

The recommendation system provides personalized recommendations based on the student's recent quiz performance.

### Flow

1. The backend sends the student's ID and recent quiz results to the Data Science API.
2. The API considers the latest 5 quizzes.
3. Answers are grouped by topic.
4. The accuracy of each topic is calculated.
5. Topics are sorted based on their accuracy.
6. The 3 weakest topics are selected.
7. A difficulty level is assigned based on the student's accuracy.
8. The recommendations are returned to the backend.

### Difficulty Rules

| Accuracy            | Difficulty |
| ------------------- | ---------- |
| Less than 40%       | Easy       |
| 40% – less than 70% | Medium     |
| 70% or higher       | Hard       |

## API

The recommendation service is implemented using FastAPI.

### Health Check

**GET**

```text
/api
```

Response:

```json
{
  "message": "Data Science API is running"
}
```

### Recommendations

**POST**

```text
/api/recommendations
```

### Request

The backend sends the student's ID and recent quiz results.

Example:

```json
{
  "student_id": 1,
  "recent_quizzes": [
    {
      "quiz_id": 101,
      "subcategory": "Python",
      "difficulty": "medium",
      "answers": [
        {
          "topic": "Loops",
          "is_correct": false
        },
        {
          "topic": "Functions",
          "is_correct": true
        }
      ]
    }
  ]
}
```

Each quiz contains:

* `quiz_id`
* `subcategory`
* `difficulty`
* `answers`

Each answer contains:

* `topic`
* `is_correct`

### Response

```json
{
  "student_id": 1,
  "recommendations": [
    {
      "subcategory": "Python",
      "topic": "Loops",
      "difficulty": "easy"
    }
  ]
}
```

The API returns the student's ID and the recommended topics with their corresponding subcategory and difficulty.

## Installation

Make sure Python is installed, then install the required dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

From the `ma3refa-ds` directory, run:

```bash
uvicorn api.index:app --reload
```

The API will run locally at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation can be accessed at:

```text
http://127.0.0.1:8000/docs
```

## Deployment

The API is configured for deployment using **Vercel**.

The `vercel.json` configuration routes requests to the FastAPI application in `api/index.py`.

After deployment, the backend can communicate with the Data Science API through the deployed API URL.
