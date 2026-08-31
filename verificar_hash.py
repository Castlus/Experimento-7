import hashlib
import os
import sys


def sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


if len(sys.argv) != 3:
    print("Uso: python verificar_hash.py <original> <recebido>")
    raise SystemExit(1)

original, recebido = sys.argv[1], sys.argv[2]
h1, h2 = sha256(original), sha256(recebido)

print(f"{original}")
print(f"  tamanho: {os.path.getsize(original)} bytes")
print(f"  SHA-256: {h1}")
print()
print(f"{recebido}")
print(f"  tamanho: {os.path.getsize(recebido)} bytes")
print(f"  SHA-256: {h2}")
print()

if h1 == h2:
    print("RESULTADO: hashes identicos, arquivo integro.")
else:
    print("RESULTADO: hashes diferentes, arquivo corrompido ou incompleto.")
