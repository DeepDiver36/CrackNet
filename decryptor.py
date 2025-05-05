# ---------- Caesar Cipher Decryption ----------

def caesar_decrypt(ciphertext, shift):
    """Decrypts Caesar cipher with the given shift."""
    decrypted = ''
    for char in ciphertext:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            decrypted += chr((ord(char) - offset - shift) % 26 + offset)
        else:
            decrypted += char
    return decrypted

# ---------- XOR Cipher Decryption ----------

def xor_decrypt(ciphertext, key):
    """Decrypts XOR cipher using the given key."""
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(ciphertext))

# ---------- Base64 Decryption ----------

def base64_decrypt(ciphertext):
    """Decrypts a Base64 encoded ciphertext."""
    import base64
    return base64.b64decode(ciphertext).decode('utf-8', errors='ignore')


# ---------- RSA Decryption (No external library) ----------


def egcd(a, b):
    """Extended Euclidean Algorithm to find modular inverse."""
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

def modinv(a, m):
    """Modular inverse of a under modulo m."""
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception("Modular inverse does not exist.")
    return x % m

def isqrt(n):
    """Integer square root for factoring n."""
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

def rsa_decrypt(ciphertext, d=None, n=None, e=None):
    if not n:
        return "❌ Missing modulus (n)"

    if not d:
        if not e:
            return "❌ Need either private exponent (d) or public exponent (e)"
        
        # Try factoring n to compute d
        for i in range(2, isqrt(n) + 1):
            if n % i == 0:
                p = i
                q = n // i
                phi = (p - 1) * (q - 1)
                try:
                    d = modinv(e, phi)
                    print(f"✔ Found p={p}, q={q}, computed φ={phi}, d={d}")
                except Exception as err:
                    return f"❌ {err}"
                break
        else:
            return "❌ Failed to factor n and compute d"

    # Now decrypt using d
    plaintext = ''
    ciphertexts = ciphertext.split()
    for i in ciphertexts:
        i = int(i)
        i = i**d
        i = i % n
        
        plaintext = plaintext + str(i) + ' '

   

    return plaintext

