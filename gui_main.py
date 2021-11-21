import sys
import bip39
import requests
import json
import mnemonic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QStyleFactory, QMainWindow, QVBoxLayout, QPushButton, QWidget, \
    QHBoxLayout, QFileDialog, QPlainTextEdit, QLineEdit
from bip32utils import BIP32Key
from bip32utils import BIP32_HARDEN
from requests.auth import HTTPBasicAuth
from bitcoin.rpc import RawProxy
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

COUNTERPARTY_HOST = "api.counterparty.io"
# COUNTERPARTY_PORT = 4000 # mainnet
COUNTERPARTY_PORT = 14000  # testnet
COUNTERPARTY_SSL_PORT = 14001  # testnet

COUNTERBLOCK_HOST = "api.counterparty.io"
COUNTERBLOCK_PORT = 14100  # testnet
COUNTERBLOCK_SSL_PORT = 14101  # testnet

class Window(QWidget):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        # init settings
        self.setWindowTitle("C02 Token Admin Panel")
        # self.showMaximized()
        self.resize(500, 400)
        QApplication.setStyle(QStyleFactory.create('macintosh'))
        rpc_credentials_file = open('private_rpc_data.txt', 'r')
        rpc_credentials_file_lines = rpc_credentials_file.readlines()
        username = rpc_credentials_file_lines[0]
        password = rpc_credentials_file_lines[1]
        self.p = AuthServiceProxy("http://%s:%s@127.0.0.1:18332"%(username, password))

        # display content
        layout = QVBoxLayout(self)

        admin_label = QLabel("Admin Panel \n-\nDecentralized CO2 Certificate Token", self)
        admin_label.setFont(QFont("Arial", 20))
        layout.addWidget(admin_label)

        leaf_hbox = QHBoxLayout()
        leaf_hbox.addStretch(1)
        leaf_label = QLabel()
        leaf_pixmap = QPixmap('leaf.png').scaledToWidth(120)
        leaf_label.setPixmap(leaf_pixmap)
        leaf_hbox.addWidget(leaf_label)

        leaf_hbox.addStretch(1)
        layout.addLayout(leaf_hbox)
        layout.addStretch(1)

        label_wallet = QLabel("Wallet: ")
        label_wallet.setFont(QFont("Arial", 20))
        layout.addWidget(label_wallet)

        wallet_hbox = QHBoxLayout()

        self.wallet_file = QLineEdit()
        wallet_hbox.addWidget(self.wallet_file)

        wallet_load_button = QPushButton("Load Wallet")
        wallet_hbox.addWidget(wallet_load_button)
        wallet_load_button.clicked.connect(self.open_wallet_file)

        layout.addLayout(wallet_hbox)

        self.wallet_status_label = QLabel()
        self.wallet_status_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(self.wallet_status_label)

        layout.addStretch(1)

        label_issuance = QLabel("CO2 Token Issuance: ")
        label_issuance.setFont(QFont("Arial", 20))
        layout.addWidget(label_issuance)

        issue_asset_hbox = QHBoxLayout()

        issue_asset_label = QLabel("Asset name:")
        issue_asset_hbox.addWidget(issue_asset_label)

        self.asset_name_line = QLineEdit("A8295361410163036000")#("CARBONDIOXID")
        issue_asset_hbox.addWidget(self.asset_name_line)

        layout.addLayout(issue_asset_hbox)

        issue_token_button = QPushButton("Create Token on Bitcoin Blockchain")
        issue_token_button.clicked.connect(self.issue_token)
        layout.addWidget(issue_token_button)

        layout.addStretch(1)

        label_send = QLabel("CO2 Token Send: ")
        label_send.setFont(QFont("Arial", 20))
        layout.addWidget(label_send)

        send_asset_hbox = QHBoxLayout()

        send_asset_label = QLabel("Bitcoin Address:")
        send_asset_hbox.addWidget(send_asset_label)

        self.send_address_line = QLineEdit("mxJQUbCb2bsSKwwsnUsBW7PouTfnMsLxyt")
        send_asset_hbox.addWidget(self.send_address_line)

        layout.addLayout(send_asset_hbox)

        send_token_button = QPushButton("Send CO2 Token")
        send_token_button.clicked.connect(self.send_token)
        layout.addWidget(send_token_button)

        layout.addStretch(1)

    def send_token(self):
        url = "http://" + COUNTERPARTY_HOST + ":" + str(COUNTERPARTY_PORT) + "/api/"
        headers = {"content-type": "application/json"}
        auth = HTTPBasicAuth("rpc", "rpc")
        create_send_payload = {
            "method": "create_send",
            "params": {
                "source": self.address,
                "destination": "mxJQUbCb2bsSKwwsnUsBW7PouTfnMsLxyt",
                "asset": "A8295361010163036000",  # self.asset_name_line.text(),
                "quantity": 37777,
                "allow_unconfirmed_inputs": True
            },
            "jsonrpc": "2.0",
            "id": 0
        }
        response = requests.post(url, data=json.dumps(create_send_payload), headers=headers, auth=auth)
        unsigned_transaction = json.loads(response.text)["result"]
        signed_transaction = self.p.signrawtransactionwithkey(unsigned_transaction, [self.private_key])
        print(signed_transaction)


    def issue_token(self):
        print(self.address)
        print(self.asset_name_line.text())

        url = "http://" + COUNTERPARTY_HOST + ":" + str(COUNTERPARTY_PORT) + "/api/"
        headers = {"content-type": "application/json"}
        auth = HTTPBasicAuth("rpc", "rpc")

        issue_payload = {
            "method": "create_issuance",
            "params": {
                "source": self.address,
                "asset": "A8295361410163036000",# self.asset_name_line.text(),
                "quantity": 100000000,
                "allow_unconfirmed_inputs": True,
                "description": "represents 1 ton of CO2.",
                "divisible": True,
                "pubkey": self.public_key
            },
            "jsonrpc": "2.0",
            "id": 0
        }
        response = requests.post(url, data=json.dumps(issue_payload), headers=headers, auth=auth)
        unsigned_transaction = json.loads(response.text)["result"]

        signed_transaction = self.p.signrawtransactionwithkey(unsigned_transaction, [self.private_key])
        print(signed_transaction)

        # broadcast_payload = {
        #     "method": "create_broadcast",
        #     "params": {
        #         "source": self.address,
        #         "asset": "A8296361410163036000",  # self.asset_name_line.text(),
        #         "quantity": 100000000,
        #         "allow_unconfirmed_inputs": True,
        #         "description": "represents 1 ton of CO2.",
        #         "divisible": True,
        #         "pubkey": self.public_key
        #     },
        #     "jsonrpc": "2.0",
        #     "id": 0
        # }
        # response = requests.post(url, data=json.dumps(broadcast_payload), headers=headers, auth=auth)
        # print(self.p.sendrawtransaction(signed_transaction['hex']))



    def open_wallet_file(self):
        file_path = QFileDialog.getOpenFileNames(self, "", "", "Text files (*.txt)")
        self.wallet_file.setText(file_path[0][0])
        mnemonic_words = open(self.wallet_file.text(), "r").read()
        seed = mnemonic.Mnemonic.to_seed(mnemonic_words)
        key = BIP32Key.fromEntropy(seed)
        self.address = "mrBSAR1pw3BQzobjimoR8r8cXYm4KVmftD"
        self.public_key = "03a9fb3f0a6319f816f975adb6b7b1da464d7c76b2384307a3fe6cc467d235fc29"
        self.private_key = "cU5J2LRfSM1egfSn6jmhP7vGnUCFjAsHaQmubZ9bHqD89vd4xZRW"

        self.wallet_status_label.setText('<font color="green">Private Wallet Successfully Loaded! <br />Bitcoin Address: ' + self.address + '</font>')

def main():
    # Create Window Application
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
