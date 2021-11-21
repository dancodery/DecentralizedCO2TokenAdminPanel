from requests.auth import HTTPBasicAuth
import json
import requests

COUNTERPARTY_HOST = "api.counterparty.io"
# COUNTERPARTY_PORT = 4000 # mainnet
COUNTERPARTY_PORT = 14000  # testnet
COUNTERPARTY_SSL_PORT = 14001  # testnet

COUNTERBLOCK_HOST = "api.counterparty.io"
COUNTERBLOCK_PORT = 14100  # testnet
COUNTERBLOCK_SSL_PORT = 14101  # testnet

if __name__ == '__main__':
    url = "http://" + COUNTERPARTY_HOST + ":" + str(COUNTERPARTY_PORT) + "/api/"
    headers = {"content-type": "application/json"}
    auth = HTTPBasicAuth("rpc", "rpc")

    payload = {
        "method": "create_issuance",
        "params": {
            "source": "mx9zWHi8QMxMyB9RtDrtwyQeGNphPMYURK",
            "asset": "CARBONDIOXID",#"A8295361010163036000",
            "quantity": 1000,
            "allow_unconfirmed_inputs": True,
            "description": "my asset is cool",
            "divisible": True
        },
        "jsonrpc": "2.0",
        "id": 0
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    print("Response: ", json.dumps(json.loads(response.text), indent=4))
