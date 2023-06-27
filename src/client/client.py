from base64 import b64decode
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.models import SimulateRequest
from algosdk import abi, transaction
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
    TransactionSigner,
    ABI_RETURN_HASH,
)

from ..contract import approval_program, clear_state_program


class AppClient:
    def __init__(
        self, algod: AlgodClient, sender: str, signer: TransactionSigner
    ) -> None:
        self.algod = algod
        self.sender = sender
        self.signer = signer
        self.approval_program = compile_contract(algod, approval_program)
        self.clear_state_program = compile_contract(algod, clear_state_program)

    def array_contains(
        self,
        array: list[int],
        target: int,
        *,
        extra_budget: int = 0,
        more_logs: bool = False
    ) -> bool:
        composer = AtomicTransactionComposer()
        composer.add_method_call(
            sender=self.sender,
            signer=self.signer,
            app_id=0,  # Create app
            on_complete=transaction.OnComplete.DeleteApplicationOC,  # Delete after call
            method=abi.Method.from_signature("array_contains(uint16[],uint16)bool"),
            method_args=[array, target],
            approval_program=self.approval_program,
            clear_program=self.clear_state_program,
            sp=self.algod.suggested_params(),
        )
        request = SimulateRequest(
            txn_groups=[], allow_more_logs=more_logs, extra_opcode_budget=extra_budget
        )
        response = composer.simulate(self.algod, request)

        if "logs" in response.abi_results[0].tx_info:
            logs = [b64decode(log) for log in response.abi_results[0].tx_info["logs"]]
            print([log.decode() for log in logs if not log.startswith(ABI_RETURN_HASH)])

        if response.failure_message != "":
            raise Exception("Simulation failed: " + response.failure_message)
        return response.abi_results[0].return_value


def compile_contract(client: AlgodClient, src: str) -> bytes:
    response = client.compile(src)
    return b64decode(response["result"])
