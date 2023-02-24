from web3 import Web3
import ipfsApi

# w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
#
# print(w3.isConnected())
# print(w3.eth.get_block('latest'))

api = ipfsApi.Client('127.0.0.1', 5001)
# print(api.add("dense3_split_1.json"))

print(api.cat("QmYr2Asusu1W6UjE9ot7khqfbVHiAtY8cwwmnwNx3popV8"))
