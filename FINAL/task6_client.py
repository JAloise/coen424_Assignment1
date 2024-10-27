import grpc
import prize_pb2
import prize_pb2_grpc

def run():
    cloud_run_url = "grpc-server-751936615562.us-central1.run.app"

    credentials = grpc.ssl_channel_credentials()

    with grpc.secure_channel(f'{cloud_run_url}:443', credentials) as channel:
        stub = prize_pb2_grpc.NobelPrizeServiceStub(channel)

        print("Which query do you want to run:")
        print("1: Get total laureates by category and year range")
        print("2: Get total laureates with a keyword in motivation")
        print("3: Get laureate details by first and last name")
        
        choice = input("Enter query number: ").strip()

        if choice == "1":
            # Query 1
            try:
                category = input("Enter the category (e.g. mathematics): ").strip()
                start_year = int(input("Enter start year (e.g 2013): ").strip())
                end_year = int(input("Enter the end year (e.g. 2020): ").strip())

                response = stub.GetLaureatesByCategoryAndYearRange(
                    prize_pb2.CategoryYearRequest(category=category, start_year=start_year, end_year=end_year)
                )
                print(f"Total laureates in {category} ({start_year}-{end_year}): {response.total_laureates}")
            except grpc.RpcError as e:
                print(f"gRPC Error: {e.code()} - {e.details()}")
            except ValueError:
                print("Invalid input.")

        elif choice == "2":
            # Query 2
            try:
                keyword = input("Enter a keyword to search in motivation (e.g. courage): ").strip()

                response = stub.GetLaureatesByKeyword(
                    prize_pb2.KeywordRequest(keyword=keyword)
                )
                print(f"Total number of laureates with '{keyword}' in the motivation: {response.total_laureates}")
            except grpc.RpcError as e:
                print(f"Error: {e.code()} - {e.details()}")

        elif choice == "3":
            # Query 3
            try:
                first_name = input("Enter first name: ").strip()
                last_name = input("Enter last name: ").strip()

                response = stub.GetLaureateByName(
                    prize_pb2.NameRequest(first_name=first_name, last_name=last_name)
                )
                if response.year:
                    print(f"{first_name} {last_name}'s Nobel Prize: Year: {response.year}, Category: {response.category}, Motivation: {response.motivation}")
                else:
                    print(f"Not found.")
            except grpc.RpcError as e:
                print(f"gRPC Error: {e.code()} - {e.details()}")

        else:
            print("Invalid choice. Script exiting.")

if __name__ == '__main__':
    run()
