FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY task6_server.py prize_pb2.py prize_pb2_grpc.py .

# Expose port
EXPOSE 50051

# Start server
CMD ["python", "task6_server.py"]
