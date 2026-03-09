from hashlib import sha256

datas = ["12345", "12346"]

print("=" * 20, "SHA-256 Hash", "=" * 20)
for d in datas:
    print(f'"{d}": {sha256(d.encode()).hexdigest()}')
