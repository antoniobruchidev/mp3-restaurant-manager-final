import json
import os
from flask.cli import load_dotenv
from web3 import Web3
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3.middleware import construct_sign_and_send_raw_middleware
load_dotenv()

# create an instance of the web3 provider
w3 = Web3(Web3.HTTPProvider(os.environ.get("ALCHEMY_KEY")))

# check the connection
print('Web3 connection: ', w3.is_connected())

# check for a valid private_key
private_key = os.environ.get("PRIVATE_KEY")
assert private_key is not None, "You must set PRIVATE_KEY environment variable"
assert private_key.startswith(
    "0x"), "Private key must start with 0x hex prefix"

# access a local account with the private_key
account: LocalAccount = Account.from_key(private_key)
w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))

# access the smart contract ABI
with open('restaurantmanager/AccessManager.json') as f:
    abi=json.load(f)

# create an instance of the contract
accessmanager = w3.eth.contract(address=os.environ.get("CONTRACT_ADDRESS"), abi=abi)

# defining the functions we are going to call
has_role_func = accessmanager.get_function_by_signature(
    'hasRole(bytes32,address)')
grant_role_func = accessmanager.get_function_by_signature(
    'grantRole(bytes32,address)')
get_role_admin = accessmanager.get_function_by_signature(
    'getRoleAdmin(bytes32)')

# function to check a given role for a given address
def check_role(role, address):
    # convert the address to a checksum address
    cs_address = w3.to_checksum_address(address)
    result = has_role_func(role,cs_address).call()
    return result


# function to grant a given role to a given address
def grant_role(role, granting_address, granted_address):
    # get the Admin role for the given role
    roleAdmin = get_role_admin(role)
    # convert addresses to checksum addresses
    cs_granting_address = w3.to_checksum_address(granting_address)
    cs_granted_address = w3.to_checksum_address(granted_address)
    # check if the sender has an Admin role for the given role
    isAdmin = has_role_func(roleAdmin, cs_granting_address)
    if isAdmin:
        # initialize the chain id, we need it to build the transaction for replay protection
        Chain_id = w3.eth.chain_id
        # call the function
        nonce = w3.eth.get_transaction_count(account.address)
        call_function = grant_role_func(
            role,cs_granted_address
            ).build_transaction({"chainId": Chain_id, "from": account.address, "nonce": nonce})
        # Sign transaction
        signed_tx = w3.eth.account.sign_transaction(call_function, private_key=private_key)
        # Send transaction
        send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
        # convert the transaction hash to hexadecimal
        tx_hash = w3.to_hex(tx_receipt.transactionHash)
        print(tx_hash)
        if tx_receipt.status == 1:
            return {"success": True, "tx_hash": tx_hash}
        else:
            return {"success": False, "tx_receipt": tx_receipt}
    else:
        return {"success": False, "error": 403}
    

def role_hash(role):
    match role:
        case "owner":
            return "0xb19546dff01e856fb3f010c267a7b1c60363cf8a4664e21cc89c26224620214e"
        case "manager":
            return "0x241ecf16d79d0f8dbfb92cbc07fe17840425976cf0667f022fe9877caa831b08"
        case "chef":
            return "0xbb95cca64affbe55a6a6f6b690ae1c8525d24dc953087f6db9a21e7cb374b385"
        case "waiter":
            return "0xcb57d3fb43d2386a5b9956d50e3893564d63703e540d4377ea7d0ea153e406d8"
        case "user":
            return "0x14823911f2da1b49f045a0929a60b8c1f2a7fc8c06c7284ca3e8ab4e193a08c8"
        case _:
            return False
