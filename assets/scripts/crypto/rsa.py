from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


message = b"This message is from me, I promise"


key = RSA.generate(4096)
private_key = key
public_key = key.publickey()

hash_msg = SHA256.new(message)

signature = pkcs1_15.new(private_key).sign(hash_msg)


print("[🔐] Private key (PEM):")
print(private_key.export_key().decode())

print("\n[📢] Public key (PEM):")
print(public_key.export_key().decode())

print("\n[📝] Message:", message.decode())
print("[🔍] SHA256(message):", hash_msg.hexdigest())
print("[✍️] Signature (hex):", signature.hex())

try:
    pkcs1_15.new(public_key).verify(hash_msg, signature)
    print("✅ Signature verified! Message is authentic.")
except (ValueError, TypeError):
    print("❌ Signature NOT valid.")

    
