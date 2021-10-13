import exbitron

client = exbitron.Client(
    access_key="*****",
    secret_key="*****"
)
print(client.get("/api/v2/peatio/account/balances"))
