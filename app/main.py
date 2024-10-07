import socket  # noqa: F401

def create_message(correlation_id, error_code=0):
    id_bytes = correlation_id.to_bytes(4, byteorder='big')
    error_code_bytes = error_code.to_bytes(2, byteorder='big')
    return len(id_bytes + error_code_bytes).to_bytes(4, byteorder='big') + id_bytes + error_code_bytes

def client_handler(client, addr):
    data = client.recv(1024)
    message_length = int.from_bytes(data[:4], byteorder='big')
    request_api_key = int.from_bytes(data[4:6], byteorder='big')
    request_api_version = version_check(int.from_bytes(data[6:8], byteorder='big'))
    correlation_id = int.from_bytes(data[8:12], byteorder='big')
    if not request_api_version:
        client.sendall(create_message(correlation_id=correlation_id, error_code=35))
    # client_id
    # tagged_fields
    print(data)
    client.sendall(create_message(correlation_id))

def version_check(request_api_version):
    return request_api_version if request_api_version in [0, 1, 2, 3, 4] else False

def main():
    # You can use print statements as follows for debugging,
    # they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    server = socket.create_server(("localhost", 9092), reuse_port=True)
    
    while True:
        client, addr = server.accept() # wait for client
        client_handler(client, addr)
    

if __name__ == "__main__":
    main()
