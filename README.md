# Blockchain Contract Parser

## 📁 Usage

```bash
docker compose run analyzer -h
```

```text
usage: main.py [-h] [-a ADDRESSES [ADDRESSES ...]] [-t TRANSACTIONS [TRANSACTIONS ...]]
               [--etherscan] [--decompile] [--semgrep] [--mythril] [--slither]

Smart Contract Security Tool

options:
  -h, --help            show this help message and exit

Address loader options:
  -a ADDRESSES [ADDRESSES ...], --addresses ADDRESSES [ADDRESSES ...]
                        List of address IDs containing the contracts to be parsed
  -t TRANSACTIONS [TRANSACTIONS ...], --transactions TRANSACTIONS [TRANSACTIONS ...]
                        List of transactions IDs containing the contracts to be parsed

Scanner options:
  --etherscan           Download the source code of contracts using Etherscan

Analyzer options:
  --decompile           Run bytecode decompilation using Panoramix
  --semgrep             Run static code analysis using Semgrep
  --mythril             Run static code analysis using Mythril
  --slither             Run static code analysis using Slither
  --openai              Run code analysis using OpenAI model
```

## 🤖 Bypass AntiBot

Copy _.env.sample_ file and fill the `cf_clearance` cookie value:

```bash
cp .env.sample .env
```
