import sys
from hashlib import sha256

args = sys.argv

datas = args[1:]
iv = "0000"

print("=" * 20, "SHA-256 Hash Chain", "=" * 20)

current_hash = sha256(iv.encode()).hexdigest()
print(f'IV : "{iv}" : {current_hash}\n')

for i, d in enumerate(datas):
    current_hash = sha256((current_hash + d).encode()).hexdigest()
    print(f'    Data {i} : "{d}" : {current_hash}')

print(f"\nThe Last Hash : {current_hash}\n")
