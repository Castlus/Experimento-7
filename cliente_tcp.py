import socket
import time

HOST = "127.0.0.1"
PORT = 5000
ARQUIVO = "arquivo_teste.bin"
TAM_LEITURA = 4096

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Conectando ao servidor...")
cliente.connect((HOST, PORT))
print(f"Conexao estabelecida. Porta local: {cliente.getsockname()[1]}")

inicio = time.perf_counter()
enviados = 0
with open(ARQUIVO, "rb") as f:
    while True:
        bloco = f.read(TAM_LEITURA)
        if not bloco:
            break
        cliente.sendall(bloco)
        enviados += len(bloco)

cliente.shutdown(socket.SHUT_WR)
fim = time.perf_counter()
cliente.close()

print()
print("--- ENVIO TCP ---")
print(f"Bytes enviados: {enviados}")
print(f"Tempo de envio: {fim - inicio:.9f} s")
