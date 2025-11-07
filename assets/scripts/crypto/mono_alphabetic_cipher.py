import argparse
import string
import sys
import matplotlib.pyplot as plt
from collections import Counter

def validate_key(key):
    if len(key) != 26 or not key.isalpha() or len(set(key.lower())) != 26:
        raise ValueError("The key must be a 26-character string containing all the letters of the alphabet exactly once.")

def create_cipher_maps(key, decrypt=False):
    alphabet = string.ascii_lowercase
    if decrypt:

        return dict(zip(key.lower(), alphabet)), dict(zip(key.upper(), alphabet.upper()))
    else:

        return dict(zip(alphabet, key.lower())), dict(zip(alphabet.upper(), key.upper()))

def process_file(input_file, output_file, cipher_map_lower, cipher_map_upper):
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                encrypted_line = ''.join(
                    cipher_map_lower.get(char, cipher_map_upper.get(char, char)) for char in line
                )
                outfile.write(encrypted_line)
    except FileNotFoundError:
        print(f"Error : The file '{input_file}' havn't been founded.")
        sys.exit(1)

def count_letters(text):
    text = text.lower()
    return Counter(char for char in text if char.isalpha())

def plot_letter_frequency(letter_counts):
    letters, counts = zip(*sorted(letter_counts.items()))
    plt.bar(letters, counts)
    plt.xlabel("Letters")
    plt.ylabel("Frequencies")
    plt.title("Frequency of letters in the text")
    plt.show()

def crack_cipher(input_file, output_file):

    try:
        with open(input_file, 'r') as infile:
            encrypted_text = infile.read()
        letter_counts = count_letters(encrypted_text)
        cipher_freq_order = sorted(letter_counts, key=letter_counts.get, reverse=True)
        english_freq_order = "etaoinshrdlucmfwypvbgkjqxz"
        mapping = {}
        for i, letter in enumerate(cipher_freq_order):
            if i < len(english_freq_order):
                mapping[letter] = english_freq_order[i]
    
        cipher_map_lower = mapping
        cipher_map_upper = {k.upper(): v.upper() for k, v in mapping.items()}
        
 
        with open(output_file, 'w') as outfile:
            for char in encrypted_text:
                if char.islower():
                    outfile.write(cipher_map_lower.get(char, char))
                elif char.isupper():
                    outfile.write(cipher_map_upper.get(char, char))
                else:
                    outfile.write(char) 
        
        print("Cracked text written in the output file", output_file)
        print("Result :")
        for cipher_letter in sorted(mapping):
            print(f"  {cipher_letter} -> {mapping[cipher_letter]}")
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{input_file}' n'a pas été trouvé.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Outil de chiffrement monoalphabétique")
    parser.add_argument("-i", required=True, help="Fichier d'entrée")
    parser.add_argument("-o", required=True, help="Fichier de sortie")
    parser.add_argument("-K", help="Clé (26 lettres, requise pour les modes chiffrement/déchiffrement)")
    parser.add_argument("-e", action="store_true", help="Mode chiffrement")
    parser.add_argument("-d", action="store_true", help="Mode déchiffrement")
    parser.add_argument("-c", action="store_true", help="Mode crack (analyse fréquentielle)")

    args = parser.parse_args()

    if sum([args.e, args.d, args.c]) != 1:
        print("Erreur : Spécifiez exactement un mode : -e (chiffrement), -d (déchiffrement) ou -c (crack).")
        sys.exit(1)

    if args.c:
        crack_cipher(args.i, args.o)
        sys.exit(0)

    if (args.e or args.d) and args.K is None:
        print("Erreur : La clé (-K) est requise pour les modes chiffrement ou déchiffrement.")
        sys.exit(1)

    try:
        if args.K:
            validate_key(args.K)
    except ValueError as e:
        print(f"Erreur : {e}")
        sys.exit(1)

    if args.K:
        cipher_map_lower, cipher_map_upper = create_cipher_maps(args.K, decrypt=args.d)
        process_file(args.i, args.o, cipher_map_lower, cipher_map_upper)

    # Analyse du texte traité et affichage de la fréquence des lettres
    with open(args.o, 'r') as outfile:
        processed_text = outfile.read()
        letter_counts = count_letters(processed_text)
        plot_letter_frequency(letter_counts)
        print("Analyse fréquentielle du texte traité :")
        for letter, count in sorted(letter_counts.items()):
            print(f"  {letter} : {count}")

if __name__ == "__main__":
    main()
