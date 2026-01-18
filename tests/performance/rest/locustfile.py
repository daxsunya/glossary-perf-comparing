from locust import HttpUser, task, between
import random
import string
import time

import sys
sys.setrecursionlimit(2000)

def random_keyword(user_id: str, length=6):
    base = ''.join(random.choices(string.ascii_lowercase, k=length))
    return f"{base}-{user_id}"


class User(HttpUser):
    host = "http://127.0.0.1:8000"
    wait_time = between(0.5, 3.0)
    keywords: list[str]

    def on_start(self):
        self.user_id = str(random.randint(1000, 9999))
        self.keywords = []

        for _ in range(3):
            while True:
                keyword = random_keyword(self.user_id)
                payload = {
                    "keyword": keyword,
                    "definition": "Load testing term",
                    "description": "Created by locust"
                }
                try:
                    with self.client.post("/terms", json=payload, catch_response=True, name="/terms") as response:
                        if response.status_code in [200, 400]:
                            self.keywords.append(keyword)
                            response.success()
                            break
                        else:
                            response.failure(f"Unexpected status {response.status_code}")
                except Exception:
                    continue

    def on_stop(self):
        for keyword in self.keywords:
            try:
                self.client.delete(f"/terms/{keyword}", name="/terms")
                time.sleep(0.05)  # пауза 50 мс между DELETE
            except Exception as e:
                print(f"Failed to delete {keyword}: {e}")

    @task(7)
    def read_term(self):
        if not self.keywords:
            return
        keyword = random.choice(self.keywords)
        self.client.get(f"/terms/{keyword}", name="/terms/{keyword}")

    @task(3)
    def create_term(self):
        keyword = random_keyword(self.user_id)
        payload = {
            "keyword": keyword,
            "definition": "Load testing term",
            "description": "Created by locust"
        }

        with self.client.post(
                "/terms",
                json=payload,
                catch_response=True,
                name="/terms"
        ) as response:
            if response.status_code == 200:
                self.keywords.append(keyword)
                response.success()
            elif response.status_code == 400:
                self.keywords.append(keyword)
                response.success()
            else:
                response.failure(f"Unexpected status {response.status_code}")
