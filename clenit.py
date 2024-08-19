import socket
from cryptography.fernet import Fernet

# Load the encryption key
with open('secret.key', 'rb') as key_file:
    key = key_file.read()
cipher_suite = Fernet(key)

# Function to encrypt a file
def encrypt_file(file_path, output_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = cipher_suite.encrypt(file_data)
    with open(output_path, 'wb') as file:
        file.write(encrypted_data)

def client_program():
    host = '127.0.0.1'
    port = 65432
    client_socket = socket.socket()
    client_socket.connect((host,port))

    file_name = 'example.txt'
    encrypted_file_name = file_name + '.enc'
    
    # Encrypt the file
    encrypt_file(file_name, encrypted_file_name)
    
    # Send the file name
    client_socket.send(file_name.encode())
    
    # Send the encrypted file
    with open(encrypted_file_name, 'rb') as file:
        while chunk := file.read(1024):
            client_socket.send(chunk)

    print(f"File {file_name} has been encrypted and sent.")
    client_socket.close()

if __name__ == "__main__":
    client_program()
