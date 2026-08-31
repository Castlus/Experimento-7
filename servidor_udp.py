import hashlib
import socket
import struct
import time

HOST = "127.0.0.1"
PORT = 5001
SAIDA = "recebido_udp.bin"
TAM_BLOCO = 1400
TIMEOUT = 5.0  # segundos sem receber nada antes de encerrar


def sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# buffer de recepcao maior evita descarte pelo proprio sistema operacional,
# que confundiria o resultado do experimento de perda
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4 * 1024 * 1024)
servidor.bind((HOST, PORT))
print(f"Servidor UDP aguardando datagramas em {HOST}:{PORT} ...")

blocos = {}
recebidos = 0
inicio = None
fim = None
teve_marcador = False

while True:
    try:
        dados, endereco = servidor.recvfrom(65535)
    except socket.timeout:
        print("Timeout atingido. O marcador de fim nao chegou (provavel perda).")
        break

    if inicio is None:
        inicio = time.perf_counter()
        servidor.settimeout(TIMEOUT)
        print(f"Primeiro datagrama de {endereco}")

    if dados == b"FIM":
        teve_marcador = True
        break

    seq = struct.unpack("!I", dados[:4])[0]
    if seq not in blocos:
        recebidos += 1
    blocos[seq] = dados[4:]

fim = time.perf_counter()
servidor.close()

if not blocos:
    print("Nenhum bloco de dados recebido.")
    raise SystemExit(1)

maior = max(blocos)
perdidos = [i for i in range(maior + 1) if i not in blocos]

with open(SAIDA, "wb") as f:
    for seq in sorted(blocos):
        f.seek(seq * TAM_BLOCO)
        f.write(blocos[seq])

print()
print("--- RESULTADO UDP ---")
print(f"Datagramas de dados recebidos: {recebidos}")
print(f"Maior numero de sequencia visto: {maior}")
print(f"Blocos perdidos: {len(perdidos)}")
if perdidos:
    amostra = ", ".join(str(p) for p in perdidos[:25])
    sufixo = " ..." if len(perdidos) > 25 else ""
    print(f"Sequencias perdidas: {amostra}{sufixo}")
print(f"Marcador de fim recebido: {'sim' if teve_marcador else 'nao'}")
print(f"Tempo de recepcao: {fim - inicio:.9f} s")
print(f"Arquivo salvo: {SAIDA}")
print(f"SHA-256: {sha256(SAIDA)}")
