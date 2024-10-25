import grpc
import prize_pb2
import prize_pb2_grpc

def run():
    # Establish connection to the server
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = prize_pb2_grpc.NobelPrizeServiceStub(channel)

        # Query 1: Category and Year Range
        response = stub.GetLaureatesByCategoryAndYearRange(
            prize_pb2.CategoryYearRequest(category="physics", start_year=2013, end_year=2023)
        )
        print(f"Total laureates in physics (2013-2023): {response.total_laureates}")

        # Query 2: Keyword in motivation
        response = stub.GetLaureatesByKeyword(
            prize_pb2.KeywordRequest(keyword="discovery")
        )
        print(f"Total laureates with 'discovery' in motivation: {response.total_laureates}")

        # Query 3: Laureate by Name
        response = stub.GetLaureateByName(
            prize_pb2.NameRequest(first_name="Albert", last_name="Einstein")
        )
        print(f"Albert Einstein's Nobel Prize: Year: {response.year}, Category: {response.category}, Motivation: {response.motivation}")

if __name__ == '__main__':
    run()