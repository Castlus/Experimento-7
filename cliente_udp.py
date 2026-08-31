import socket
import struct
import time

HOST = "127.0.0.1"
PORT = 5001
ARQUIVO = "arquivo_teste.bin"
TAM_BLOCO = 1400
REPETICOES_FIM = 3  # coloque 1 se quiser a contagem de pacotes mais limpa

cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4 * 1024 * 1024)

with open(ARQUIVO, "rb") as f:
    dados = f.read()

total = (len(dados) + TAM_BLOCO - 1) // TAM_BLOCO
print(f"Arquivo: {len(dados)} bytes")
print(f"Datagramas de dados a enviar: {total}")

inicio = time.perf_counter()
for seq in range(total):
    pedaco = dados[seq * TAM_BLOCO:(seq + 1) * TAM_BLOCO]
    cliente.sendto(struct.pack("!I", seq) + pedaco, (HOST, PORT))

for _ in range(REPETICOES_FIM):
    cliente.sendto(b"FIM", (HOST, PORT))
fim = time.perf_counter()

print(f"Porta local usada: {cliente.getsockname()[1]}")
cliente.close()

print()
print("--- ENVIO UDP ---")
print(f"Datagramas de dados enviados: {total}")
print(f"Datagramas de controle (FIM): {REPETICOES_FIM}")
print(f"Tempo de envio: {fim - inicio:.9f} s")
