import argparse

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

######################################################################################################################

def encrypt(text, columns):
    padding = '_' * ((columns - len(text) % columns) % columns)
    text += padding

    matrix = [list(text[i:i+columns]) for i in range(0, len(text), columns)]

    transposed = zip(*matrix)
    encrypted = ''.join(''.join(col) for col in transposed)
    return encrypted


def decrypt(text, columns):
    rows = len(text) // columns
    matrix = [[''] * columns for _ in range(rows)]


    idx = 0
    for col in range(columns):
        for row in range(rows):
            matrix[row][col] = text[idx]
            idx += 1

    decrypted = ''.join(''.join(row) for row in matrix)
    return decrypted.rstrip('_')

######################################################################################################################
with open('message.txt', 'r') as f:
    message = (f.read())
with open('output.txt', 'r') as f:
    output = (f.read())
with open('verif.txt', 'r') as f:
    verif = (f.read())

print('\n')
print(message,' <-- message')
print(output,' <-- output')
print(verif.rstrip('_'),' <-- verify')
######################################################################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transposition cipher script.')
    parser.add_argument('-i', '--input', required=True, help='Input file')
    parser.add_argument('-o', '--output', required=True, help='Output file')
    parser.add_argument('-k', '--columns', type=int, required=True, help='Number of columns')
    parser.add_argument('-e', '--encrypt', action='store_true', help='Encrypt mode')
    parser.add_argument('-d', '--decrypt', action='store_true', help='Decrypt mode')
    args = parser.parse_args()

    if args.encrypt == args.decrypt:
        print("❌ Please specify either -e (encrypt) or -d (decrypt), but not both.")
        exit(1)

    text = read_file(args.input)

    if args.encrypt:
        result = encrypt(text, args.columns)
    else:
        result = decrypt(text, args.columns)

    write_file(args.output, result)
    #print("✅ Operation completed successfully.")
    if message == verif.rstrip('_'):
        print("✅ Verification passed")
    print('\n')


