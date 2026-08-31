import hashlib
import os

NOME = "arquivo_teste.bin"
TAMANHO = 1024 * 1024


def sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


with open(NOME, "wb") as f:
    f.write(os.urandom(TAMANHO))

print(f"Arquivo gerado: {NOME}")
print(f"Tamanho: {os.path.getsize(NOME)} bytes")
print(f"SHA-256: {sha256(NOME)}")
