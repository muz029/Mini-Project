from typing import Optional
from pymongo import MongoClient, ASCENDING

class MongoStorage:
    def __init__(self, uri: str):
        self.client = MongoClient(uri)
        self.db = self.client.get_default_database() or self.client["botzilla"]
        self.users = self.db["users"]
        self.users.create_index([("telegram_id", ASCENDING)], unique=True)

    def upsert_user(self, telegram_id: int, username: str, first_name: str, last_name: str,
                    profile_pic_url: str, joined_at: str, status: str = "unverified") -> None:
        self.users.update_one(
            {"telegram_id": telegram_id},
            {"$setOnInsert": {"joined_at": joined_at, "profile_pic_url": profile_pic_url, "status": status},
             "$set": {"username": username, "first_name": first_name, "last_name": last_name}},
            upsert=True,
        )

    def get_user(self, telegram_id: int) -> Optional[dict]:
        return self.users.find_one({"telegram_id": telegram_id}, {"_id": 0})

    def update_status(self, telegram_id: int, status: str) -> None:
        self.users.update_one({"telegram_id": telegram_id}, {"$set": {"status": status}})

    def count_users(self) -> int:
        return self.users.estimated_document_count()
