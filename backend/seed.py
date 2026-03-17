"""
Seed Script: Populates the database with initial questions.
Run: python seed.py
"""
import asyncio
import uuid
from app.database import AsyncSessionLocal, init_db
from app.models.question import Question, Difficulty


CODING_QUESTIONS = [
    {
        "id": "two-sum",
        "title": "Two Sum",
        "difficulty": Difficulty.easy,
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nExample:\nInput: nums = [2,7,11,15], target = 9\nOutput: [0,1]",
        "tags": ["array", "hash-map"],
        "starter_code": {
            "python": "def two_sum(nums, target):\n    # Your code here\n    pass",
            "javascript": "function twoSum(nums, target) {\n  // Your code here\n}",
            "cpp": "#include <vector>\nusing namespace std;\nvector<int> twoSum(vector<int>& nums, int target) {\n    // Your code here\n}",
        },
        "test_cases": [
            {"input": "2 7 11 15\n9", "expected_output": "0 1"},
            {"input": "3 2 4\n6", "expected_output": "1 2"},
            {"input": "3 3\n6", "expected_output": "0 1"},
        ],
        "hints": ["Try using a hash map to store complements", "One-pass solution is possible in O(n)"],
        "interview_type": "coding",
    },
    {
        "id": "merge-intervals",
        "title": "Merge Intervals",
        "difficulty": Difficulty.medium,
        "description": "Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals.\n\nExample:\nInput: [[1,3],[2,6],[8,10],[15,18]]\nOutput: [[1,6],[8,10],[15,18]]",
        "tags": ["array", "sorting"],
        "starter_code": {
            "python": "def merge(intervals):\n    # Your code here\n    pass",
            "javascript": "function merge(intervals) {\n  // Your code here\n}",
        },
        "test_cases": [
            {"input": "[[1,3],[2,6],[8,10],[15,18]]", "expected_output": "[[1,6],[8,10],[15,18]]"},
        ],
        "hints": ["Sort intervals by start time first"],
        "interview_type": "coding",
    },
    {
        "id": "lru-cache",
        "title": "LRU Cache",
        "difficulty": Difficulty.medium,
        "description": "Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.\n\nImplement:\n- LRUCache(capacity)\n- get(key): Return value or -1\n- put(key, value): Update or insert",
        "tags": ["design", "hash-map", "linked-list"],
        "starter_code": {
            "python": "class LRUCache:\n    def __init__(self, capacity: int):\n        pass\n\n    def get(self, key: int) -> int:\n        pass\n\n    def put(self, key: int, value: int) -> None:\n        pass",
        },
        "test_cases": [],
        "hints": ["Use OrderedDict in Python", "Combine a doubly linked list with a hash map"],
        "interview_type": "coding",
    },
]

SYSTEM_DESIGN_QUESTIONS = [
    {"id": "url-shortener", "title": "Design a URL Shortener like bit.ly", "difficulty": Difficulty.medium, "description": "Design a scalable URL shortening service that can handle millions of redirects per day.", "tags": ["distributed-systems", "databases"], "interview_type": "system_design"},
    {"id": "twitter-feed", "title": "Design a Twitter-like Social Feed", "difficulty": Difficulty.hard, "description": "Design a scalable social media news feed system.", "tags": ["distributed-systems", "caching"], "interview_type": "system_design"},
    {"id": "ride-sharing", "title": "Design a Ride-sharing System", "difficulty": Difficulty.hard, "description": "Design the backend architecture for a ride-sharing platform like Uber.", "tags": ["distributed-systems", "geo-spatial"], "interview_type": "system_design"},
    {"id": "chat-app", "title": "Design a Real-time Chat Application", "difficulty": Difficulty.medium, "description": "Design a scalable real-time messaging system supporting millions of concurrent users.", "tags": ["websockets", "distributed-systems"], "interview_type": "system_design"},
]

BEHAVIORAL_QUESTIONS = [
    {"id": "conflict", "title": "Tell me about a time you resolved a conflict in your team.", "difficulty": None, "description": "Describe a situation where you had a disagreement with a colleague and how you resolved it.", "tags": ["leadership", "communication"], "interview_type": "behavioral"},
    {"id": "challenging-project", "title": "Describe a challenging project you led.", "difficulty": None, "description": "Walk me through a difficult project from start to finish.", "tags": ["leadership", "project-management"], "interview_type": "behavioral"},
    {"id": "technical-decision", "title": "Describe a difficult technical decision you made.", "difficulty": None, "description": "Tell me about a time you had to make a high-stakes technical choice.", "tags": ["technical-judgment"], "interview_type": "behavioral"},
    {"id": "learn-quickly", "title": "Describe learning something new quickly.", "difficulty": None, "description": "Tell me about a situation where you had to pick up a new skill rapidly.", "tags": ["adaptability", "growth"], "interview_type": "behavioral"},
]


async def seed():
    await init_db()
    async with AsyncSessionLocal() as db:
        all_questions = CODING_QUESTIONS + SYSTEM_DESIGN_QUESTIONS + BEHAVIORAL_QUESTIONS
        added = 0
        for q_data in all_questions:
            from sqlalchemy import select
            result = await db.execute(select(Question).where(Question.id == q_data["id"]))
            existing = result.scalar_one_or_none()
            if not existing:
                question = Question(
                    id=q_data["id"],
                    title=q_data["title"],
                    description=q_data["description"],
                    interview_type=q_data["interview_type"],
                    difficulty=q_data.get("difficulty"),
                    tags=q_data.get("tags", []),
                    starter_code=q_data.get("starter_code"),
                    test_cases=q_data.get("test_cases", []),
                    hints=q_data.get("hints", []),
                )
                db.add(question)
                added += 1
        await db.commit()
        print(f"Seeded {added} questions ({len(all_questions) - added} already existed)")


if __name__ == "__main__":
    asyncio.run(seed())
