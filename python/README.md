# Exbitron.com API 

#### Install

```
pip install requests
curl https://github.com/exbitron/api/raw/main/python/exbitron.py
```

#### Usage

```python
import exbitron

# access public apis
client = exbitron.Client()
print(client.get_public("/api/v2/peatio/public/markets/"))

# access secret apis
client = exbitron.Client(
    access_key="*****",
    secret_key="*****"
)
print(client.get("/api/v2/peatio/account/balances"))
```