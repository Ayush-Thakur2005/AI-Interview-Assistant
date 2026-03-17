"""
Seed script — populates the questions table with starter data.
Run: python seed_questions.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, init_db
from app.models.question import Question

QUESTIONS = [
    # ── Coding ────────────────────────────────────────────────────────────────
    {
        "id": "two-sum",
        "interview_type": "coding",
        "title": "Two Sum",
        "difficulty": "Easy",
        "description": (
            "Given an array of integers `nums` and an integer `target`, return indices of "
            "the two numbers such that they add up to `target`.\n\n"
            "Example:\nInput: nums = [2,7,11,15], target = 9\nOutput: [0,1]"
        ),
        "category": "arrays",
        "starter_code": {
            "python": "def two_sum(nums, target):\n    # Your code here\n    pass",
            "javascript": "function twoSum(nums, target) {\n  // Your code here\n}",
            "cpp": "#include <vector>\nusing namespace std;\n\nvector<int> twoSum(vector<int>& nums, int target) {\n    // Your code here\n}",
        },
        "test_cases": [
            {"input": [[2, 7, 11, 15], 9], "expected": [0, 1]},
            {"input": [[3, 2, 4], 6], "expected": [1, 2]},
            {"input": [[3, 3], 6], "expected": [0, 1]},
        ],
        "tags": ["array", "hash-map", "easy"],
    },
    {
        "id": "merge-intervals",
        "interview_type": "coding",
        "title": "Merge Intervals",
        "difficulty": "Medium",
        "description": (
            "Given an array of intervals where `intervals[i] = [starti, endi]`, merge all overlapping intervals.\n\n"
            "Example:\nInput: [[1,3],[2,6],[8,10],[15,18]]\nOutput: [[1,6],[8,10],[15,18]]"
        ),
        "category": "arrays",
        "starter_code": {
            "python": "def merge(intervals):\n    # Your code here\n    pass",
            "javascript": "function merge(intervals) {\n  // Your code here\n}",
            "cpp": "#include <vector>\n#include <algorithm>\nusing namespace std;\n\nvector<vector<int>> merge(vector<vector<int>>& intervals) {\n    // Your code here\n}",
        },
        "test_cases": [
            {"input": [[[1, 3], [2, 6], [8, 10], [15, 18]]], "expected": [[1, 6], [8, 10], [15, 18]]},
        ],
        "tags": ["array", "sorting", "medium"],
    },
    {
        "id": "lru-cache",
        "interview_type": "coding",
        "title": "LRU Cache",
        "difficulty": "Medium",
        "description": (
            "Design a data structure that follows Least Recently Used (LRU) cache constraints.\n\n"
            "Implement `LRUCache(capacity)`, `get(key)`, and `put(key, value)` — all in O(1) time."
        ),
        "category": "design",
        "starter_code": {
            "python": "class LRUCache:\n    def __init__(self, capacity: int):\n        pass\n\n    def get(self, key: int) -> int:\n        pass\n\n    def put(self, key: int, value: int) -> None:\n        pass",
            "javascript": "class LRUCache {\n  constructor(capacity) {}\n  get(key) {}\n  put(key, value) {}\n}",
            "cpp": "class LRUCache {\npublic:\n    LRUCache(int capacity) {}\n    int get(int key) {}\n    void put(int key, int value) {}\n};",
        },
        "test_cases": [],
        "tags": ["design", "linked-list", "hash-map", "medium"],
    },
    # ── System Design ─────────────────────────────────────────────────────────
    {
        "id": "url-shortener",
        "interview_type": "system_design",
        "title": "Design URL Shortener",
        "difficulty": "Medium",
        "description": "Design a scalable URL shortener service like bit.ly that handles millions of requests per day.",
        "category": "web-services",
        "starter_code": None,
        "test_cases": None,
        "tags": ["scalability", "hashing", "databases"],
    },
    {
        "id": "twitter-feed",
        "interview_type": "system_design",
        "title": "Design a Social Media Feed",
        "difficulty": "Hard",
        "description": "Design a Twitter-like social media feed system supporting millions of users and real-time updates.",
        "category": "social",
        "starter_code": None,
        "test_cases": None,
        "tags": ["feed", "caching", "pub-sub", "scalability"],
    },
    {
        "id": "ride-sharing",
        "interview_type": "system_design",
        "title": "Design a Ride-Sharing System",
        "difficulty": "Hard",
        "description": "Design a ride-sharing platform like Uber supporting real-time driver-rider matching and location tracking.",
        "category": "geospatial",
        "starter_code": None,
        "test_cases": None,
        "tags": ["geospatial", "real-time", "matching"],
    },
    {
        "id": "chat-app",
        "interview_type": "system_design",
        "title": "Design a Real-Time Chat Application",
        "difficulty": "Medium",
        "description": "Design a real-time messaging system supporting 1:1 and group chats with delivery receipts.",
        "category": "messaging",
        "starter_code": None,
        "test_cases": None,
        "tags": ["websockets", "messaging", "real-time"],
    },
    # ── Behavioral ────────────────────────────────────────────────────────────
    {
        "id": "conflict-resolution",
        "interview_type": "behavioral",
        "title": "Conflict Resolution",
        "difficulty": None,
        "description": "Tell me about a time you had to resolve a conflict within your team.",
        "category": "teamwork",
        "starter_code": None,
        "test_cases": None,
        "tags": ["conflict", "teamwork", "communication"],
    },
    {
        "id": "difficult-decision",
        "interview_type": "behavioral",
        "title": "Difficult Technical Decision",
        "difficulty": None,
        "description": "Tell me about a time you had to make a difficult technical decision under pressure.",
        "category": "decision-making",
        "starter_code": None,
        "test_cases": None,
        "tags": ["decision-making", "leadership"],
    },
    {
        "id": "learning-quickly",
        "interview_type": "behavioral",
        "title": "Learning Quickly",
        "difficulty": None,
        "description": "Describe a situation where you had to learn something new very quickly.",
        "category": "growth",
        "starter_code": None,
        "test_cases": None,
        "tags": ["learning", "adaptability"],
    },
    {
        "id": "led-project",
        "interview_type": "behavioral",
        "title": "Led a Challenging Project",
        "difficulty": None,
        "description": "Describe a challenging project you led from start to finish.",
        "category": "leadership",
        "starter_code": None,
        "test_cases": None,
        "tags": ["leadership", "project-management"],
    },
]


def seed():
    init_db()
    db = SessionLocal()
    added = 0
    for q_data in QUESTIONS:
        existing = db.query(Question).filter(Question.id == q_data["id"]).first()
        if not existing:
            q = Question(**q_data)
            db.add(q)
            added += 1
    db.commit()
    db.close()
    print(f"Seeded {added} questions ({len(QUESTIONS) - added} already existed).")


if __name__ == "__main__":
    seed()
