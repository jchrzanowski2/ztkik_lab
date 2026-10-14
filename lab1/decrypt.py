from math import gcd

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Table 2.1 from the lecture (probability of letter occurrence in English)
P_ENG = {'A': .082, 'B': .015, 'C': .028, 'D': .043, 'E': .127, 'F': .022,
         'G': .020, 'H': .061, 'I': .070, 'J': .002, 'K': .008, 'L': .040,
         'M': .024, 'N': .067, 'O': .075, 'P': .019, 'Q': .001, 'R': .060,
         'S': .063, 'T': .091, 'U': .028, 'V': .010, 'W': .023, 'X': .001,
         'Y': .020, 'Z': .001}

# Your ciphertext
CIPHERTEXT = (
    "HEJJWIEEFHKGAOBMXHKYCMZGRENHAEEFKXFRKFLURJOYONWAEEFRMYKUGMVUGNKREUNMBMZWEXMZMQMQRMZGNHMGYMXMIHMZMGEQMEXMLJUAGKXOXYEXGLOYUEUGAKFAMNOXNEKYEQLUNMZIKONGGMYEXFGKXFNKCMGEBMZNHMMXNOZMOXTZKGNZUYNUZMRKFRMYKUGMOXNHMZMKJIEZJFKFMBOYMFEMGXNHKYCMBMZWNHOXAONKJIKWGMPLJEONGKGLMYOTOYLZENEYEJKFMGOAXTJKIEZKQOGYEXTOAUZMFFMBOYM"
)

def mod_inverse(a, m=26):
    """a^(-1) mod m (modular inverse)"""
    return pow(a, -1, m)

def decrypt(ciphertext, a, b):
    """d(y) = a^(-1) * (y - b) mod 26."""
    a_inv = mod_inverse(a)
    return "".join(ALPHABET[a_inv * (ALPHABET.index(c) - b) % 26].lower() for c in ciphertext)

def english_score(text):
    """Calculates the average letter probability - checks if the text is English (approx. 0.065) or gibberish (approx. 0.038)"""
    return sum(P_ENG[c.upper()] for c in text) / len(text)

def solve_system(x1, y1, x2, y2):
    """Solves the system of equations from the lecture (page 14): a*x1 + b = y1 and a*x2 + b = y2 (mod 26)."""
    dx, dy = (x1 - x2) % 26, (y1 - y2) % 26
    g = gcd(dx, 26)
    if dy % g != 0:
        return [] # inconsistent system
    m = 26 // g
    a0 = (dy // g) * pow(dx // g, -1, m) % m
    return [(a, (y1 - a * x1) % 26) for a in range(a0, 26, m)]

def cryptanalysis(ciphertext, threshold=0.055):
    # STEP 1: Frequency analysis (lecture pages 12-13)
    counter = {c: ciphertext.count(c) for c in ALPHABET}
    print("--- CIPHERTEXT HISTOGRAM ---")
    print(" ".join(f"{c}:{counter[c]}" for c in ALPHABET if counter[c]))

    # STEP 2: Determining the most frequent letters (lecture page 13 - Example 2.10)
    cipher_freq = sorted(ALPHABET, key=lambda c: (-counter[c], c))[:6]
    plain_freq = sorted(ALPHABET, key=lambda c: -P_ENG[c])[:6]
    print(f"\nMost frequent in ciphertext: {cipher_freq}")
    print(f"Most frequent in English   : {[j.lower() for j in plain_freq]}\n")

    # STEP 3: Testing hypotheses for letter pairs
    failed_attempts = []
    print("--- TESTING HYPOTHESES ---")
    for i in range(len(plain_freq)):
        for j in range(i + 1, len(plain_freq)):
            p1, p2 = plain_freq[i], plain_freq[j]
            for c1 in cipher_freq:
                for c2 in cipher_freq:
                    if c1 == c2:
                        continue
                    
                    x1, y1 = ALPHABET.index(p1), ALPHABET.index(c1)
                    x2, y2 = ALPHABET.index(p2), ALPHABET.index(c2)
                    hyp = f"{c1}={p1.lower()}, {c2}={p2.lower()}"

                    # Solving the system
                    keys = solve_system(x1, y1, x2, y2)
                    if not keys:
                        print(f"{hyp}: inconsistent system")
                        continue
                        
                    for a, b in keys:
                        if gcd(a, 26) != 1:
                            print(f"{hyp}: (a, b) = ({a}, {b}) -> INVALID, GCD({a}, 26) = {gcd(a, 26)}")
                            failed_attempts.append((a, b, "invalid (GCD != 1)"))
                            continue
                            
                        plaintext = decrypt(ciphertext, a, b)
                        M = english_score(plaintext)
                        
                        if M >= threshold:
                            return (a, b), plaintext, failed_attempts
                        failed_attempts.append((a, b, f"gibberish (M={M:.3f})"))
                        
    return None, None, failed_attempts

def main():
    print("="*50)
    print("AFFINE CIPHER CRYPTANALYSIS")
    print("="*50)
    print(f"Ciphertext ({len(CIPHERTEXT)} letters):\n{CIPHERTEXT}\n")
    
    key, plaintext, failed_attempts = cryptanalysis(CIPHERTEXT)

    print("\nIneffective keys:", ", ".join(f"({a}, {b}) {p}" for a, b, p in failed_attempts) or "none")
    if key is None:
        return

    a, b = key
    print(f"\n[+] FOUND AFFINE KEY: a={a}, b={b}")
    print(f"Plaintext:\n{plaintext}")

if __name__ == "__main__":
    main()