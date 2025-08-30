import socket
import sys
import struct
import os

SERVER_ADDR = ("localhost", 12345)
BUFFER_SIZE = 1024

def auth_login(sock):
    username = input("Usuário: ")
    password = input("Senha: ")

    sock.sendto(f"{username}:{password}".encode(), SERVER_ADDR)
    data, addr = sock.recvfrom(1024)
    response = data.decode()

    if response == "SUCCESS":
        print("Login successful.")
        return True
    else:
        print("Login failed.")
        return False

def send_file(sock, filename):
    if not os.path.exists(filename):
        print("Arquivo não encontrado.")
        return

    sock.sendto(f"put {filename}".encode(), SERVER_ADDR)

    with open(filename, "rb") as f:
        file_id = 0
        while True:
            chunk = f.read(BUFFER_SIZE)
            if not chunk:
                break

            pacote = struct.pack("I", file_id) + chunk
            sock.sendto(pacote, SERVER_ADDR)

            try:
                ack, _ = sock.recvfrom(1024)
                if ack.decode() == f"ACK{file_id}":
                    print(f"Pacote {file_id} confirmado.")
                    file_id += 1
                else:
                    f.seek(f.tell() - len(chunk))
            except socket.timeout:
                f.seek(f.tell() - len(chunk))

        sock.sendto(b"END", SERVER_ADDR)
        print("Arquivo enviado com sucesso.")

def receive_file(sock, filename):
    with open("download_" + filename, "wb") as f:
        while True:
            pacote, _ = sock.recvfrom(BUFFER_SIZE + 4)

            if pacote == b"END":
                print(f"Arquivo {filename} recebido com sucesso.")
                break

            pacote_id = struct.unpack("I", pacote[:4])[0]
            dados = pacote[4:]
            f.write(dados)

            sock.sendto(f"ACK{pacote_id}".encode(), SERVER_ADDR)

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(2)

    if not auth_login(s):
        s.close()
        sys.exit(1)
    
    while True:
        comando = input("Digite um comando (ls, cd, mkdir, rmdir, put, get, quit): ")

        if comando.startswith("put"):
            _, filename = comando.split(" ", 1)
            send_file(s, filename)

        elif comando.startswith("get"):
            _, filename = comando.split(" ", 1)
            s.sendto(comando.encode(), SERVER_ADDR)
            receive_file(s, filename)

        elif comando == "quit":
            s.sendto(b"quit", SERVER_ADDR)
            print("Encerrando cliente...")
            break

        else:
            s.sendto(comando.encode(), SERVER_ADDR)
            data, addr = s.recvfrom(1024)
            print(f"Resposta do servidor: {data.decode()}")

    s.close()

if __name__ == "__main__":
    main()
