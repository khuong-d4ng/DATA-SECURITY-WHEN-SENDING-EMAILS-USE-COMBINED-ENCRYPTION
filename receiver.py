import base64, json
from datetime import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asy_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Load khóa
def load_key(path, private=False):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None) if private else serialization.load_pem_public_key(f.read())

receiver_priv = load_key("receiver_private.pem", private=True)
sender_pub = load_key("sender_public.pem")

# Đọc gói tin
with open("packet.json", "r") as f:
    packet = json.load(f)

# Kiểm tra thời hạn
now = datetime.utcnow()
exp = datetime.strptime(packet["exp"], "%Y-%m-%dT%H:%M:%S.%fZ")

if now > exp:
    print("❌ Quá hạn giải mã. Gửi NACK (timeout)")
    exit()

# Kiểm tra chữ ký
metadata = packet["metadata"].encode()
sig = base64.b64decode(packet["sig"])
try:
    sender_pub.verify(sig, metadata, asy_padding.PKCS1v15(), hashes.SHA512())
except:
    print("❌ Sai chữ ký. Gửi NACK (invalid signature)")
    exit()

# Giải mã Session Key
session_key = receiver_priv.decrypt(
    base64.b64decode(packet["enc_session_key"]),
    asy_padding.PKCS1v15()
)

# Kiểm tra hash
iv = base64.b64decode(packet["iv"])
ciphertext = base64.b64decode(packet["cipher"])
digest = hashes.Hash(hashes.SHA512())
digest.update(iv + ciphertext + packet["exp"].encode())
if digest.finalize().hex() != packet["hash"]:
    print("❌ Hash không khớp. Gửi NACK (integrity error)")
    exit()

# Giải mã file
cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv))
decryptor = cipher.decryptor()
padded_plain = decryptor.update(ciphertext) + decryptor.finalize()
pad_len = padded_plain[-1]
plaintext = padded_plain[:-pad_len]

# Lưu lại file
with open("received_email.txt", "wb") as f:
    f.write(plaintext)

print("✅ Giải mã thành công. Gửi ACK tới người gửi.")
