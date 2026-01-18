from concurrent import futures
import grpc
from app import terms_pb2, terms_pb2_grpc, crud
from database import SessionLocal, Base, engine
from schemas import TermCreate

class TermsServiceServicer(terms_pb2_grpc.TermsServiceServicer):

    def CreateTerm(self, request, context):
        db = SessionLocal()
        try:
            term_data = TermCreate(keyword=request.keyword, description=request.description)
            term = crud.create_term(db, term_data)
            return terms_pb2.TermResponse(
                id=term.id,
                keyword=term.keyword,
                description=term.description
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return terms_pb2.TermResponse()
        finally:
            db.close()

    def GetTerm(self, request, context):
        db = SessionLocal()
        try:
            term = crud.get_term_by_keyword(db, request.keyword)
            if not term:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Term not found")
                return terms_pb2.TermResponse()
            return terms_pb2.TermResponse(
                id=term.id,
                keyword=term.keyword,
                description=term.description
            )
        finally:
            db.close()

def serve():
    Base.metadata.create_all(bind=engine)

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )
    terms_pb2_grpc.add_TermsServiceServicer_to_server(
        TermsServiceServicer(), server
    )
    server.add_insecure_port("0.0.0.0:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
