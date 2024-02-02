# Blockchain Contract Parser

## 📁 Usage

```bash
docker compose run analyzer -h
```

```text
usage: main.py [-h] [-a ADDRESSES [ADDRESSES ...]]
               [-t TRANSACTIONS [TRANSACTIONS ...]] [-l LAST]
               [--etherscan] [--analyze] [--decompile]

Smart Contract Security Tool

options:
  -h, --help            show this help message and exit

Address loader options:
  -a ADDRESSES [ADDRESSES ...], --addresses ADDRESSES [ADDRESSES ...]
                        List of address IDs containing the contracts to be parsed
  -t TRANSACTIONS [TRANSACTIONS ...], --transactions TRANSACTIONS [TRANSACTIONS ...]
                        List of transactions IDs containing the contracts to be parsed
  -l LAST, --last LAST  The number of last transactions containing contracts to be parsed <= 100_000

Scanner options:
  --etherscan           Download the source code of contracts using Etherscan

Analyzer options:
  --analyze             Run static code analysis using Semgrep
  --decompile           Run bytecode decompilation using Panoramix
```

## 🤖 Bypass AntiBot

Copy _.env.sample_ file and fill the `cf_clearance` cookie value:

```bash
cp .env.sample .env
```
