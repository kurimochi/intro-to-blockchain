import argparse
import sys
from hashlib import sha256


def count_leading_zero_bits(data: bytes):
    val = int.from_bytes(data)
    total_bits = len(data) * 8
    return total_bits - val.bit_length()


def validate_hashcash(message: bytes, nonce: int, difficulty: int):
    hash = sha256(
        message + nonce.to_bytes((nonce.bit_length() + 7) // 8, "little")
    ).digest()
    zero_count = count_leading_zero_bits(hash)
    return difficulty <= zero_count


# Parser
parser = argparse.ArgumentParser(description="SHA-256 HashCash")

parser.add_argument("message", help="Message (String, Hex, or Filepath)", type=str)
parser.add_argument("difficulty", help="HashCash Difficulty", type=int)
parser.add_argument(
    "-f",
    "--format",
    help="Message format",
    choices=["str", "hex", "path"],
    default="str",
)
parser.add_argument(
    "-s", "--start", help="Starting point for nonce search", type=int, default=0
)

args = parser.parse_args()

print("=" * 20, "SHA-256 HashCash", "=" * 20)

# Message
message = None
match args.format:
    case "str":
        message = args.message.encode()
    case "hex":
        try:
            message = bytes.fromhex(args.message)
        except ValueError:
            sys.exit("[-] A non-hexadecimal value found")
    case "path":
        try:
            with open(args.message, "rb") as f:
                message = f.read()
        except FileNotFoundError:
            sys.exit("[-] The file at the specified path could not be found")

print(f"[*] Message: {message.hex()}")
print(f"[*] Difficulty: {args.difficulty}")

# Nonce Search
nonce_cand = args.start
while True:
    if not nonce_cand % 100000:
        print(f"[*] Trying {nonce_cand}")
    if validate_hashcash(message, nonce_cand, args.difficulty):
        break
    nonce_cand += 1

hash = sha256(
    message + nonce_cand.to_bytes((nonce_cand.bit_length() + 7) // 8, "little")
).hexdigest()
print("[+] Found!")
print(f"[+] Nonce: {nonce_cand}")
print(f"[+] SHA-256 Hash: {hash}")
