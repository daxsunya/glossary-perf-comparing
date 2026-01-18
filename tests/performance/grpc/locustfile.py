from locust import User, task, between, events
from locust.exception import RescheduleTask
import random
import string
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.grpc_client import TermsGrpcClient

def random_keyword(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

class GrpcUser(User):
    wait_time = between(0.1, 0.3)

    def on_start(self):
        self.client = TermsGrpcClient(host="127.0.0.1:50051")
        self.keywords = []

    def grpc_request(self, name, func, *args, **kwargs):
        start_time = time.perf_counter()
        try:
            response = func(*args, **kwargs)
        except Exception as e:
            total_time = (time.perf_counter() - start_time) * 1000
            events.request.fire(
                request_type="gRPC",
                name=name,
                response_time=total_time,
                response_length=0,
                exception=e
            )
            raise RescheduleTask()
        else:
            total_time = (time.perf_counter() - start_time) * 1000

            response_size = (
                len(response.SerializeToString())
                if response is not None
                else 0
            )

            events.request.fire(
                request_type="gRPC",
                name=name,
                response_time=total_time,
                response_length=response_size,
                exception=None
            )
            return response

    @task(7)
    def read_term(self):
        if not self.keywords:
            return
        keyword = random.choice(self.keywords)
        self.grpc_request("GetTerm", self.client.get_term, keyword)

    @task(10)
    def create_term(self):
        keyword = random_keyword()
        self.grpc_request("CreateTerm", self.client.create_term, keyword, "Created by gRPC locust")
        self.keywords.append(keyword)
