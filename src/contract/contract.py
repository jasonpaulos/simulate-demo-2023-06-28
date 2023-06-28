from pyteal import *
from .utils import print_int

pragma(compiler_version="0.25.0")

router = Router(name="Example")


@router.method(no_op=CallConfig.ALL, delete_application=CallConfig.CREATE)
def array_contains(
    array: abi.DynamicArray[abi.Uint16], target: abi.Uint16, *, output: abi.Bool
) -> Expr:
    """Returns true if the target element is in the array, otherwise returns false."""
    return (
        If(array.length() == Int(0))
        .Then(output.set(False))
        .Else(output.set(binary_search(array, target.get()) < array.length()))
    )


@Subroutine(TealType.uint64)
def binary_search(array: abi.DynamicArray[abi.Uint16], target: Expr) -> Expr:
    """Uses binary search to find the index of the target element in the array.
    Returns the index if found, otherwise returns the length of the array.
    """
    low = ScratchVar(TealType.uint64)
    high = ScratchVar(TealType.uint64)
    mid = ScratchVar(TealType.uint64)
    guess = abi.Uint16()
    return Seq(
        low.store(Int(0)),
        high.store(array.length() - Int(1)),
        While(low.load() <= high.load()).Do(
            print_int(Bytes("low"), low.load()),
            print_int(Bytes("high"), high.load()),

            mid.store((low.load() + high.load()) / Int(2)),
            print_int(Bytes("mid"), mid.load()),
            
            array[mid.load()].store_into(guess),
            print_int(Bytes("guess"), guess.get()),
            
            If(guess.get() == target)
            .Then(Return(mid.load()))
            .ElseIf(guess.get() < target)
            .Then(low.store(mid.load() + Int(1)))
            .ElseIf(mid.load() == Int(0))
            .Then(Break())
            .Else(high.store(mid.load() - Int(1))),
        ),
        Return(array.length()),
    )


approval_program, clear_state_program, contract = router.compile_program(
    version=9,
)

if __name__ == "__main__":
    from pathlib import Path
    import json

    current_dir = Path(__file__).parent

    with open(Path(current_dir, "approval.teal"), "w") as f:
        f.write(approval_program)

    with open(Path(current_dir, "clear_state.teal"), "w") as f:
        f.write(clear_state_program)

    with open(Path(current_dir, "contract.json"), "w") as f:
        f.write(json.dumps(contract.dictify(), indent=4))
