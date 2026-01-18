import grpc
from app import terms_pb2, terms_pb2_grpc

GRPC_TIMEOUT = 20.0

class TermsGrpcClient:
    def __init__(self, host: str = "127.0.0.1:50051"):
        self.channel = grpc.insecure_channel(host)
        self.stub = terms_pb2_grpc.TermsServiceStub(self.channel)

    def create_term(self, keyword: str, description: str):
        print(f"[CLIENT] CreateTerm called with: {keyword}")
        return self.stub.CreateTerm(
            terms_pb2.CreateTermRequest(
                keyword=keyword,
                description=description
            ),
            timeout=GRPC_TIMEOUT
        )

    def get_term(self, keyword: str):
        print(f"[CLIENT] GetTerm called with: {keyword}")
        return self.stub.GetTerm(
            terms_pb2.GetTermRequest(keyword=keyword),
            timeout=GRPC_TIMEOUT
        )
