# Blockchain Contract Parser

## 📁 Usage

```bash
python main.py -h
```

```text
usage: main.py [-h] [-a ADDRESSES [ADDRESSES ...]] [-t TRANSACTIONS [TRANSACTIONS ...]] [-l LAST]

Blockchain Contract Parser

options:
  -h, --help            show this help message and exit
  -a ADDRESSES [ADDRESSES ...], --addresses ADDRESSES [ADDRESSES ...]
                        List of address IDs containing the contracts to be parsed
  -t TRANSACTIONS [TRANSACTIONS ...], --transactions TRANSACTIONS [TRANSACTIONS ...]
                        List of transactions IDs containing the contracts to be parsed
  -l LAST, --last LAST  The number of last transactions containing contracts to be parsed <= 100_000
```

## 🤖 Bypass AntiBot

Copy _.env.sample_ file and fill the `cf_clearance` cookie value:

```bash
cp .env.sample .env
```
