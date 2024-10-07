import socket  # noqa: F401
import concurrent.futures

supported_api_keys = [18]

def create_message(correlation_id, error_code=0, response_body=b''):
    message = b''
    id_bytes = correlation_id.to_bytes(4, byteorder='big')
    error_code_bytes = error_code.to_bytes(2, byteorder='big')

    length = len(id_bytes + error_code_bytes) + len(response_body)
    length_bytes = length.to_bytes(4, byteorder='big')

    message = length_bytes + id_bytes + error_code_bytes + response_body
    return message

def version_check(request_api_version):
    return request_api_version if request_api_version in [0, 1, 2, 3, 4] else False

def client_handler(client, addr):
    data = client.recv(1024)
    message_length = int.from_bytes(data[:4], byteorder='big')
    request_api_key = int.from_bytes(data[4:6], byteorder='big')
    request_api_version = version_check(int.from_bytes(data[6:8], byteorder='big'))
    correlation_id = int.from_bytes(data[8:12], byteorder='big')

    if not request_api_version:
        client.sendall(create_message(correlation_id, error_code=35))
    # client_id
    # tagged_fields
    # print(data)
    match request_api_key:
        case 18: APIVersions(client, correlation_id)
        case _: client.sendall( create_message(correlation_id) )
    
def APIVersions(client, correlation_id): # 18             
    tag_buffer = b'\00'
    throttle_time_ms_bytes = int(0).to_bytes(4, byteorder='big')
    min_ver = int(0).to_bytes(2, byteorder='big')
    max_ver = int(4).to_bytes(2, byteorder='big')
    
    response_body = (
        int(len(supported_api_keys) + 1).to_bytes(1)
        + supported_api_keys[0].to_bytes(2, byteorder='big')
        + min_ver
        + max_ver
        + tag_buffer
        + throttle_time_ms_bytes
        + tag_buffer
    )
    client.sendall( create_message(correlation_id, response_body=response_body) )


def main():
    # You can use print statements as follows for debugging,
    # they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    server = socket.create_server(("localhost", 9092), reuse_port=True)
    
    client, addr = server.accept() # wait for client
    while True:
        client_handler(client, addr)
    

if __name__ == "__main__":
    main()
