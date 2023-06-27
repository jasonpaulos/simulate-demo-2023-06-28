import os

from algosdk import mnemonic, account
from algosdk.v2client.algod import AlgodClient
from algosdk.atomic_transaction_composer import AccountTransactionSigner

from .client import AppClient


def test_client():
    algod = AlgodClient(
        os.environ["ALGOD_TOKEN"],
        os.environ["ALGOD_ADDRESS"],
    )

    sk = mnemonic.to_private_key(os.environ["ACCOUNT_MNEMONIC"])
    addr = account.address_from_private_key(sk)

    app = AppClient(algod, addr, AccountTransactionSigner(sk))

    assert app.array_contains([1, 2, 3, 4, 5], 3) == True
    assert app.array_contains([1, 2, 3, 4, 5], 100) == False

    random_list = random_sorted_list(900)
    print("random list:", random_list)
    not_in_list = 0
    while not_in_list in random_list:
        not_in_list += 1

    assert app.array_contains(random_list, not_in_list, extra_budget=3000) == False


def random_sorted_list(length: int) -> list[int]:
    import random

    return sorted(random.sample(range(0, 2**16), length))
