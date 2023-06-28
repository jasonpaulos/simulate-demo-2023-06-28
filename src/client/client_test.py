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

    assert app.array_contains([1, 2, 3, 4, 5], 4) == True
    assert app.array_contains([1, 2, 3, 4, 5], 100) == False

    random_list = random_sorted_list(min_value=1, max_value=2**16, length=998)
    print("random list:", random_list)

    assert app.array_contains(random_list, 0, extra_budget=3000, more_logs=True) == False


def random_sorted_list(min_value: int, max_value: int, length: int) -> list[int]:
    import random

    return sorted(random.sample(range(min_value, max_value), length))
