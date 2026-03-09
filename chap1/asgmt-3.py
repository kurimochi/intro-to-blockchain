import sys
from hashlib import sha256

args = sys.argv
last_hash = args[1]
datas = args[2:]

iv = "0000"
current_hash = sha256(iv.encode()).hexdigest()

print("=" * 20, "SHA-256 Hash Chain Validation", "=" * 20)

print(f'IV : "{iv}" : {current_hash}\n')
for i, d in enumerate(datas):
    current_hash = sha256((current_hash + d).encode()).hexdigest()
    print(f'    Data {i} : "{d}" : {current_hash}')


print(f"\nCalculated Last Hash : {current_hash}")
print(f"Expected Last Hash : {last_hash}")
if last_hash == current_hash:
    print("[+] Result: OK!")
else:
    print("[-] Result: Failed...")
    sys.exit(1)
