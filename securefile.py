import socket
import os
from cryptography.fernet import Fernet

# Generate a key for encryption/decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Save the key to a file for later use
with open('secret.key', 'wb') as key_file:
    key_file.write(key)

# Function to decrypt a file
def decrypt_file(file_path, output_path):
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    with open(output_path, 'wb') as file:
        file.write(decrypted_data)

def server_program():
    host = '127.0.0.1'
    port = 65432
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server is listening for incoming connections...")

    conn, address = server_socket.accept()
    print(f"Connection from {address} has been established!")

    # Receive the file
    file_name = conn.recv(1024).decode()
    with open(file_name + '.enc', 'wb') as file:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            file.write(data)

    # Decrypt the file
    decrypt_file(file_name + '.enc', file_name)
    print(f"Received and decrypted file: {file_name}")

    conn.close()

if __name__ == "__main__":
    server_program()
