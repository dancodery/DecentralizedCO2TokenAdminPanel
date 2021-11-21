import json
import requests
from requests.auth import HTTPBasicAuth

COUNTERPARTY_HOST = "api.counterparty.io"
# COUNTERPARTY_PORT = 4000 # mainnet
COUNTERPARTY_PORT = 14000  # testnet
COUNTERPARTY_SSL_PORT = 14001  # testnet

COUNTERBLOCK_HOST = "api.counterparty.io"
COUNTERBLOCK_PORT = 14100  # testnet
COUNTERBLOCK_SSL_PORT = 14101  # testnet


if __name__ == '__main__':
    # JSON RPC API
    url = "http://" + COUNTERPARTY_HOST + ":" + str(COUNTERPARTY_PORT) + "/api/"
    headers = {"content-type": "application/json"}
    auth = HTTPBasicAuth("rpc", "rpc")

    # payload = {
    #     "method": "get_running_info",
    #     "params": {},
    #     "jsonrpc": "2.0",
    #     "id": 0
    # }
    # payload = {
    #     "method": "get_balances",
    #     "params": {
    #         "filters": [{"field": "address", "op": "==", "value": "14qqz8xpzzEtj6zLs3M1iASP7T4mj687yq"},
    #                     {"field": "address", "op": "==", "value": "1bLockjTFXuSENM8fGdfNUaWqiM4GPe7V"}],
    #         "filterop": "or"
    #     },
    #     "jsonrpc": "2.0",
    #     "id": 0
    # }
    # payload = {
    #     "method": "get_debits",
    #     "params": {
    #         "filters": [{"field": "asset", "op": "==", "value": "XCP"},
    #                     {"field": "quantity", "op": ">", "value": 200000000}],
    #         "filterop": "AND",
    #         "order_by": "quantity",
    #         "order_dir": "desc"
    #     },
    #     "jsonrpc": "2.0",
    #     "id": 0
    # }
    # payload = {
    #     "method": "create_send",
    #     "params": {
    #         "source": "1CUdFmgK9trTNZHALfqGvd8d6nUZqH2AAf",
    #         "destination": "17rRm52PYGkntcJxD2yQF9jQqRS4S2nZ7E",
    #         "asset": "XCP",
    #         "quantity": 100000000
    #     },
    #     "jsonrpc": "2.0",
    #     "id": 0
    # }
    # payload = {
    #     "method": "create_issuance",
    #     "params": {
    #         "source": "1CUdFmgK9trTNZHALfqGvd8d6nUZqH2AAf",
    #         "asset": "MYASSET",
    #         "quantity": 1000,
    #         "description": "my asset is cool",
    #         "divisible": False
    #     },
    #     "jsonrpc": "2.0",
    #     "id": 0
    # }
    # payload = {
    #     "method": "create_issuance",
    #     "params": {
    #         "source": "1CUdFmgK9trTNZHALfqGvd8d6nUZqH2AAf",
    #         "transfer_destination": "17rRm52PYGkntcJxD2yQF9jQqRS4S2nZ7E",
    #         "asset": "MYASSET",
    #         "quantity": 0
    #     },
    #     "jsonrpc": "2.0",
    #     "id": 0
    # }
    # payload = {
    #     "method": "create_issuance",
    #     "params": {
    #         "source": "1CUdFmgK9trTNZHALfqGvd8d6nUZqH2AAf",
    #         "asset": "MYASSET",
    #         "quantity": 0,
    #         "description": "LOCK"
    #     },
    #     "jsonrpc": "2.0",
    #     "id": 0
    # }
    # payload = {
    #     "method": "get_balances",
    #     "params": {
    #         "filters": [{"field": "address", "op": "==", "value": "mrBSAR1pw3BQzobjimoR8r8cXYm4KVmftD"}],
    #         "allow_unconfirmed_inputs": True
    #     },
    #     "jsonrpc": "2.0",
    #     "id": 0
    # }
    payload = {
        "method": "get_burns",
        "params": {
            "filters": {"field": "burned", "op": ">", "value": 20000000},
            "filterop": "AND",
            "order_by": "tx_hash",
            "order_dir": "asc",
            "start_block": 280537,
            "end_block": 280539
        },
        "jsonrpc": "2.0",
        "id": 0
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    print("Response: ", json.dumps(json.loads(response.text), indent=4, sort_keys=True))

    # # REST API
    # url = "http://" + COUNTERPARTY_HOST + ":" + str(COUNTERPARTY_PORT) + "/rest/"
    # headers = {"content-type": "application/json"}
    # query = "sends/get?source=mn6q3dS2EnDUx3bmyWc6D4szJNVGtaR7zc&destination=mtQheFaSfWELRB2MyMBaiWjdDm6ux9Ezns&op=AND"
    # print(url + query)
    # response = requests.get(url + query, headers=headers)
    # print("Response: ", response.text)
