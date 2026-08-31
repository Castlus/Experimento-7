import hashlib
import socket
import time

HOST = "127.0.0.1"
PORT = 5000
SAIDA = "recebido_tcp.bin"


def sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind((HOST, PORT))
servidor.listen(1)
print(f"Servidor TCP aguardando conexao em {HOST}:{PORT} ...")

conexao, endereco = servidor.accept()
print(f"Conexao recebida de {endereco}")

inicio = time.perf_counter()
total = 0
with open(SAIDA, "wb") as f:
    while True:
        dados = conexao.recv(65536)
        if not dados:
            break
        f.write(dados)
        total += len(dados)
fim = time.perf_counter()

conexao.close()
servidor.close()

print()
print("--- RESULTADO TCP ---")
print(f"Bytes recebidos: {total}")
print(f"Tempo de recepcao: {fim - inicio:.9f} s")
print(f"Arquivo salvo: {SAIDA}")
print(f"SHA-256: {sha256(SAIDA)}")
