#!/usr/bin/env python3

import os, sys

sys.path.append(os.path.dirname(__file__).split('/transactions')[0])

from lib.encoder import encode_tx
from lib.helper  import decode_address
from lib.hash    import hash256
from lib.sign    import sign_tx
from lib.rpc     import RpcSocket

## Setup our RPC socket.
rpc = RpcSocket({ 'wallet': 'regtest' })
assert rpc.check()

## Get a utxo for Alice.
alice_utxo = rpc.get_utxo(0)

## Get a change address for Alice.
alice_change_txout = rpc.get_recv(fmt='base58')
alice_pubkey_hash  = decode_address(alice_change_txout['address'])

## Get a payment address for Bob.
bob_payment_txout = rpc.get_recv(fmt='base58')
bob_pubkey_hash   = decode_address(bob_payment_txout['address'])

## Calculate our output amounts.
fee = 1000
bob_recv_value = alice_utxo['value'] // 2
alice_change_value = alice_utxo['value'] // 2 - fee

## The spending transaction.
atob_tx = {
    'version': 1,
    'vin': [{
        # We are unlocking the utxo from Alice.
        'txid': alice_utxo['txid'],
        'vout': alice_utxo['vout'],
        'script_sig': [],
        'sequence': 0xFFFFFFFF
    }],
    'vout': [
        {
            'value': bob_recv_value,
            'script_pubkey': ['OP_1', bob_pubkey_hash, 'OP_3', 'OP_CHECKMULTISIG']
        },
        {
            'value': alice_change_value,
            'script_pubkey': ['OP_1', alice_pubkey_hash, 'OP_3', 'OP_CHECKMULTISIG']
        }
    ],
    'locktime': 0
}

## Serialize the transaction and calculate the TXID.
atob_hex  = encode_tx(atob_tx)
atob_txid = hash256(bytes.fromhex(atob_hex))[::-1].hex()

## The redeem script is a basic Pay-to-Pubkey-Hash template.
redeem_script = f"76a914{alice_utxo['pubkey_hash']}88ac"

## We are signing Alice's UTXO using BIP143 standard.
alice_signature = sign_tx(
    atob_tx,                # The transaction.
    0,                      # The input being signed.
    alice_utxo['value'],    # The value of the utxo being spent.
    redeem_script,          # The redeem script to unlock the utxo. 
    alice_utxo['priv_key']  # The private key to the utxo pubkey hash.
)

## Include the arguments needed to unlock the redeem script.
atob_tx['vin'][0]['witness'] = [ alice_signature, alice_utxo['pub_key'] ]

print(f'''
## Pay-to-Pubkey-Hash Example ##

-- Transaction Id --
{atob_txid}

-- Alice UTXO --
     Txid : {alice_utxo['txid']}
     Vout : {alice_utxo['vout']}
    Value : {alice_utxo['value']}
     Hash : {alice_utxo['pubkey_hash']}

-- Sending to Bob --
  Address : {bob_payment_txout['address']}
    Coins : {bob_recv_value}

-- Change --
  Address : {alice_change_txout['address']}
      Fee : {fee}
    Coins : {alice_change_value}

-- Hex --
{encode_tx(atob_tx)}
''')