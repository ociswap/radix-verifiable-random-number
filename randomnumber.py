# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
#     "argon2-cffi"
# ]
# ///

import sys
import time
import hashlib
from datetime import datetime, timezone
import requests
from argon2 import PasswordHasher

GATEWAY_URL = "https://mainnet.radixdlt.com"
MEMORY_COST_MB = 1024
TIME_COST = 50
SALT = b"00000000"  # the "secret" we are hashing is public, disabling the salt for verifiability is fine


def parse_args():
    timestamp = datetime.now(timezone.utc).date().isoformat()
    upper_bound = 50

    if len(sys.argv) >= 2:
        timestamp = sys.argv[1]

    if len(sys.argv) >= 3:
        try:
            upper_bound = int(sys.argv[2])
            if upper_bound <= 0:
                raise ValueError("Max value must be positive")
        except ValueError:
            raise ValueError("Max value must be a valid integer")

    return timestamp, upper_bound


AT_LEDGER_STATE_TIMESTAMP, UPPER_BOUND = parse_args()


def fetch_last_transaction_hash(at_ledger_state_timestamp: str) -> str:
    response = requests.post(
        f"{GATEWAY_URL}/stream/transactions",
        json={
            "at_ledger_state": {"timestamp": at_ledger_state_timestamp},
            "limit_per_page": 1,
        },
    )
    response.raise_for_status()
    return response.json()["items"][0]["intent_hash"]


def slow_hash(data: str) -> bytes:
    ph = PasswordHasher(time_cost=TIME_COST, memory_cost=MEMORY_COST_MB * 1024)
    argon_hash = ph.hash(data, salt=SALT)
    return hashlib.sha256(argon_hash.encode()).digest()


def random_number(seed: bytes, upper_bound: int) -> str:
    return int.from_bytes(seed) % upper_bound


last_transaction_hash = fetch_last_transaction_hash(AT_LEDGER_STATE_TIMESTAMP)

start_time = time.time()
seed = slow_hash(last_transaction_hash)
elapsed_ms = (time.time() - start_time) * 1000

print(
    f"Random number for {AT_LEDGER_STATE_TIMESTAMP}: {random_number(seed, UPPER_BOUND)}"
)
print(f"Took {elapsed_ms:.2f}ms")
