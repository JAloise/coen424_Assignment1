# coen424_Assignment1

## Task 1 Data Storage and Query on Redis
### Task 1.1
- Load Data to Redis Cloud. Keys type are JSON

### Task 1.2
- ```FT.CREATE prizeIdx ON JSON PREFIX 1 "prizes:" SCHEMA $.year AS year TEXT $.category AS category TEXT $.laureates[*].firstname AS firstname TEXT $.laureates[*].surname AS surname TEXT $.laureates[*].motivation AS motivation TEXT```
  - EX: ```FT.SEARCH prizeIdx @year:2020```
  - EX: ```FT.SEARCH prizeIdx @category:peace```
- BONUS: 

 ### Task 1.3
- See query.py files

## Task 2 Data Model Design
- Install gRPC: 
  - ```python -m pip install grpcio```
- Install gRPC tools: 
  - ```python -m pip install grpcio-tools``` 

- To run .proto file: 
  - ```python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. prize.proto```

