from pyteal import *

# Based on https://github.com/algorand/pyteal-utils/blob/main/pytealutils/strings/string.py


@Subroutine(TealType.bytes)
def int_to_ascii(arg: Expr) -> Expr:
    """int_to_ascii converts an integer to the ascii byte that represents it"""
    return Extract(Bytes("0123456789"), arg, Int(1))


@Subroutine(TealType.bytes)
def itoa(i: Expr) -> Expr:
    """itoa converts an integer to the ascii byte string it represents"""
    return If(
        i == Int(0),
        Bytes("0"),
        Concat(
            If(i / Int(10) > Int(0), itoa(i / Int(10)), Bytes("")),
            int_to_ascii(i % Int(10)),
        ),
    )


@Subroutine(TealType.none)
def print_int(label: Expr, i: Expr) -> Expr:
    return Log(Concat(label, Bytes(": "), itoa(i)))
