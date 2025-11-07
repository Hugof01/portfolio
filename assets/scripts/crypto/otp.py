def otp(plaintext, key):
    with open('plaintext.txt', 'r') as f:
        plaintext = f.read().strip()
    with open('key.txt', 'r') as f:
        key = f.read().strip()
    if len(key) < len(plaintext):
        raise ValueError("len(key) needs to be equal to len(plaintext)..")

    plaintext_bin = ''.join(format(ord(p), '08b') for p in plaintext)
    key_bin = ''.join(format(ord(k), '08b') for k in key)
    ciphertext_bin = ''.join(str(int(p) ^ int(k)) for p, k in zip(plaintext_bin, key_bin))
    with open('ciphertext.txt', 'w') as f:
        f.write(ciphertext_bin)
    return ciphertext_bin

def otp_decrypt(ciphertext, key):
    with open('ciphertext.txt', 'r') as f:
        ciphertext_bin = f.read().strip()
    with open('key.txt', 'r') as f:
        key = f.read().strip()
    key_bin = ''.join(format(ord(k), '08b') for k in key)
    plaintext_bin = ''.join(str(int(c) ^ int(k)) for c, k in zip(ciphertext_bin, key_bin))
    plaintext = ''.join(chr(int(plaintext_bin[i:i+8], 2)) for i in range(0, len(plaintext_bin), 8))
    with open('plaintext_verif.txt', 'w') as f:
        f.write(plaintext)
    return plaintext


with open('plaintext.txt', 'r') as f:
    plaintext = f.read().strip()
with open('key.txt', 'r') as f:
    key = f.read().strip()

plaintext_bin = ''.join(format(ord(p), '08b') for p in plaintext)
key_bin = ''.join(format(ord(k), '08b') for k in key)
ciphertext = otp('plaintext.txt', 'key.txt')
plaintext_verif = otp_decrypt('ciphertext.txt', 'key.txt')

print('\n')
print(plaintext_bin, '<-- Plaintext (in binary)')
print(key_bin, '<-- Key (in binary)')
print(ciphertext, '<-- Ciphertext (in binary)')
print(plaintext_verif, '<-- Plaintext verification')


def verif():
    with open('plaintext.txt', 'r') as f:
        plaintext = f.read().strip()
    with open('plaintext_verif.txt', 'r') as f:
        plaintext_verif = f.read().strip()
    if plaintext == plaintext_verif:
        print('Plaintext is verified ✅')
        print('\n')
    else:
        print('Plaintext is not verified ❌')
        print('\n')

verif()

