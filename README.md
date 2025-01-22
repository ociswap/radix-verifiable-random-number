# Radix Verifiable Random Number Generator

This script generates a verifiable random number using the Radix Network's transaction history as a source of entropy.

## How it works

1. The script fetches the latest transaction hash from the Radix Network for a given timestamp (defaults to today)
2. It then performs a computationally intensive hash operation using Argon2 (memory-hard hashing function) followed by SHA256
3. The resulting hash is converted to a random number within the specified upper bound (defaults to 50)

The security of this random number generation relies on two key elements:

1. The use of Argon2, a memory-hard function (MHF), which requires both significant memory and computational resources to compute
2. The unpredictability of Radix Network transaction hashes as a source of entropy

An attacker attempting to manipulate the output would need to:
- Find a transaction hash that produces their desired number
- Submit this transaction to the Radix Network
- Have it be the latest transaction at the target timestamp

The memory-hard properties of Argon2 make finding a suitable transaction hash computationally expensive, as each hash attempt requires:
- Significant RAM usage (configurable, typically gigabytes)
- Sequential memory operations that cannot be parallelized effectively
- Substantial CPU time

While an attacker only needs to find one suitable transaction, the computational cost of testing each potential transaction hash makes the search process impractical within a reasonable timeframe.

The process is deterministic - given the same timestamp input, it will always produce the same random number, making it verifiable by anyone running the script.

## Prerequisites

This project uses [uv](https://docs.astral.sh/uv/getting-started/installation/) for dependency management.
Follow the installation instructions in the link to set it up.

Alternatively, you can install the dependencies manually:

```bash
pip install requests argon2-cffi
```

## Running the script

Basic usage (defaults to today and 50 as upper bound):

```bash
uv run randomnumber.py
```

To specify a different timestamp or upper bound, for example January 21, 2024 with an upper bound of 100:

```bash
uv run randomnumber.py 2024-01-21 100
```

## Feedback

If you have any questions or suggestions, please feel free to open an issue or contact me directly.

## License

This script is open-sourced under the MIT License - see the LICENSE file for details.
