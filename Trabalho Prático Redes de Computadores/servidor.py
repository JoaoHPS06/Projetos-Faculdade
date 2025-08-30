import socket
import threading
import os
import struct

SERVER_ADDR = ("localhost", 12345)
BUFFER_SIZE = 1024

logged_clients = set()

users = {
    "user1": "password1",
    "user2": "password2",
}

def authenticate(data):
    try:
        username, password = data.decode().split(":")
        if username in users and users[username] == password:
            return "SUCCESS"
        else:
            return "FAILURE"
    except Exception as e:
        print(f"Authentication error: {e}")
        return "FAILURE"
    

def handle_client(s, data, addr):
    if addr in logged_clients:
        commands = data.decode().split(" ")
        n = len(commands)
        if commands[0] == "get" and n == 2:
            filename = commands[1]
            if not os.path.exists(filename):
                s.sendto(b"Arquivo nao encontrado", addr)
                return

            with open(filename, "rb") as f:
                file_id = 0
                while True:
                    chunk = f.read(BUFFER_SIZE)
                    if not chunk:
                        break

                    pacote = struct.pack("I", file_id) + chunk
                    s.sendto(pacote, addr)

                    # Aguarda ACK
                    try:
                        ack, _ = s.recvfrom(1024)
                        if ack.decode() == f"ACK{file_id}":
                            print(f"ACK {file_id} recebido de {addr}")
                            file_id += 1
                        else:
                            f.seek(f.tell() - len(chunk))  # volta para reenviar
                    except socket.timeout:
                        f.seek(f.tell() - len(chunk))  # timeout → reenviar

                # Envia fim
                s.sendto(b"END", addr)
                print(f"Arquivo {filename} enviado com sucesso para {addr}")
            
        elif commands[0] == "put" and n == 2:
            filename = commands[1]
            print(f"Iniciando recepcao do arquivo {filename} de {addr}")

            with open(filename, "wb") as f:
                while True:
                    pacote, _ = s.recvfrom(1028)  # 4 bytes ID + até 1024 dados

                    # Se for mensagem de fim
                    if pacote == b"END":
                        print(f"Arquivo {filename} recebido com sucesso.")
                        break

                    # Extrair ID
                    pacote_id = struct.unpack("I", pacote[:4])[0]
                    dados = pacote[4:]

                    # Escrever no arquivo
                    f.write(dados)

                    # Mandar ACK
                    s.sendto(f"ACK{pacote_id}".encode(), addr)

            response = f"Upload de {filename} concluido".encode()
            s.sendto(response, addr)
            return
            
        elif commands[0] == "ls":
            arquivos = os.listdir(".")
            response = "\n".join(arquivos).encode()
            s.sendto(response, addr)
            return

        elif commands[0] == "cd" and n == 2:
            pasta = commands[1]
            if os.path.isdir(pasta):
                os.chdir(pasta)
                response = f"Diretorio alterado para {pasta}".encode()
            else:
                response = b"Pasta inexistente"
            
            s.sendto(response, addr)
            return

        elif commands[0] == "cd..":
            os.chdir("..")
            response = b"Diretorio alterado para o pai"
            s.sendto(response, addr)
            return

        elif commands[0] == "mkdir" and n == 2:
            pasta = commands[1]
            try:
                os.mkdir(pasta)
                response = f"Pasta '{pasta}' criada".encode()
            except FileExistsError:
                response = b"Pasta ja existe"
            
            s.sendto(response, addr)
            return
           
        elif commands[0] == "rmdir" and n == 2:
            pasta = commands[1]
            try:
                os.rmdir(pasta)
                response = f"Pasta '{pasta}' removida".encode()
            except FileNotFoundError:
                response = b"Pasta inexistente"
            except OSError:
                response = b"Pasta nao esta vazia"
            
            s.sendto(response, addr)
            return

        elif commands[0] == "quit":
            logged_clients.remove(addr)
            response = b"Logged out successfully"
            s.sendto(response, addr)
            return


    if authenticate(data) == "SUCCESS":
        logged_clients.add(addr)
        response = b"SUCCESS"  
    else:
        print(f"Client {addr} failed to log in.")
        response = b"FAILURE"

    s.sendto(response, addr)
    print(f"Sent response to {addr}")

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(SERVER_ADDR)
    print("Server is listening on port 12345...")
    while True:
        data, addr = s.recvfrom(1024)
        threading.Thread(target=handle_client, args=(s, data, addr)).start()
    

    s.close()

if __name__ == "__main__":
    main()
