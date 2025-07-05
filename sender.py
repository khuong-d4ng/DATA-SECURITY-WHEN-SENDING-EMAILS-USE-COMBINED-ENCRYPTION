import os, base64, json
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asy_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hmac

# Load khóa
def load_key(path, private=False):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None) if private else serialization.load_pem_public_key(f.read())

sender_priv = load_key("sender_private.pem", private=True)
receiver_pub = load_key("receiver_public.pem")

# Giai đoạn handshake
print("Người gửi: Hello!")
print("Người nhận: Ready!")

# Metadata
filename = "email.txt"
timestamp = datetime.utcnow().isoformat()
metadata = f"{filename}|{timestamp}".encode()

# Ký metadata
signature = sender_priv.sign(
    metadata,
    asy_padding.PKCS1v15(),
    hashes.SHA512()
)

# Tạo Session Key + IV
session_key = os.urandom(32)
iv = os.urandom(16)

# Mã hóa file bằng AES-CBC
with open(filename, "rb") as f:
    plaintext = f.read()
cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv))
encryptor = cipher.encryptor()
padding_len = 16 - (len(plaintext) % 16)
plaintext += bytes([padding_len]) * padding_len
ciphertext = encryptor.update(plaintext) + encryptor.finalize()

# Mã hóa Session Key bằng RSA
enc_session_key = receiver_pub.encrypt(
    session_key,
    asy_padding.PKCS1v15()
)

# Tính hash
expiration = (datetime.utcnow() + timedelta(hours=24)).isoformat() + "Z"
digest = hashes.Hash(hashes.SHA512())
digest.update(iv + ciphertext + expiration.encode())
hash_value = digest.finalize().hex()

# Gói tin
packet = {
    "iv": base64.b64encode(iv).decode(),
    "cipher": base64.b64encode(ciphertext).decode(),
    "hash": hash_value,
    "sig": base64.b64encode(signature).decode(),
    "exp": expiration,
    "enc_session_key": base64.b64encode(enc_session_key).decode(),
    "metadata": metadata.decode()
}

with open("packet.json", "w") as f:
    json.dump(packet, f, indent=4)

print("Gửi packet.json đến người nhận.")
