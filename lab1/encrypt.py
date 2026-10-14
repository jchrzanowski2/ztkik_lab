import random
from math import gcd

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def generate_affine_ciphertext():
    raw_text = (
        "The quick brown fox jumps over the lazy dog. "
        "Programming in Python is fun and rewarding! "
        "Artificial intelligence is changing the world every single day. "
        "Keep learning and pushing your boundaries to achieve greatness in everything you do."
    )

    # 2. Text sanitization (only letters, no spaces or punctuation, uppercase)
    clean_text = ''.join(char.upper() for char in raw_text if char.isalpha())

    # 3. Drawing a valid key for the affine cipher
    # 'a' must be coprime with 26 (i.e., odd and not 13)
    valid_a_values = [a for a in range(1, 26) if gcd(a, 26) == 1]
    a = random.choice(valid_a_values)
    b = random.randint(0, 25) # 'b' can be any number from 0 to 25

    # 4. Encryption using the affine algorithm E(x) = (a*x + b) mod 26
    cryptogram = ""
    for char in clean_text:
        x = ALPHABET.index(char)      # Converts letter to number (A=0, B=1...)
        y = (a * x + b) % 26          # Affine formula
        cryptogram += ALPHABET[y]     # Converts number back to letter

    # 5. Displaying the results
    print(f"Text length: {len(clean_text)} characters.\n")

    print("--- AFFINE CIPHER KEY ---")
    print(f"Encryption formula: E(x) = ({a} * x + {b}) mod 26")
    print(f"a = {a}, b = {b}\n")

    print("--- ORIGINAL TEXT (SANITIZED) ---")
    for i in range(0, len(clean_text), 50):
        print(clean_text[i:i+50])

    print("\n--- CRYPTOGRAM (COPY THIS TO THE CRACKING SCRIPT) ---")
    for i in range(0, len(cryptogram), 50):
        print(cryptogram[i:i+50])

if __name__ == "__main__":
    generate_affine_ciphertext()