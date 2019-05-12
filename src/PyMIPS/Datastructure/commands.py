import sys

from PyMIPS.Datastructure.data_model import (
    ProgramStack,
    RegisterPool,
    DataHeap,
    DataStack,
)
from PyMIPS.Datastructure.memory import Memory


def get_command(ast_class):
    return {
        "li": li_command,
        "lw": lw_command,
        "sw": sw_command,
        "add": add_command,
        "sub": sub_command,
        "syscall": syscall_command,
        "mflo": mflo_command,
        "mfhi": mfhi_command,
        "div": div_command,
        "move": move_command,
        "addi": addi_command,
        "la": la_command,
        "beq": beq_command,
        "j": j_command,
        "jal": jal_command,
        "mul": mul_command,
        "jr": jr_command,
        "lb": lb_command,
        "addu": addu_command,
        "xor": xor_command,
        "and": and_command,
        "bltz": bltz_command,
        "subu": subu_command,
        "not": not_command,
        "mult": mult_command,
        "beqz": beqz_command,
        "bne": bne_command,
        "bnez": bnez_command,
        "or": or_command,
        # Unimplemented r-types
        "nor": unimplemented,
        "sll": unimplemented,
        "slt": unimplemented,
        "sltu": unimplemented,
        "sra": unimplemented,
        "srav": unimplemented,
        "divu": unimplemented,
        "jalr": unimplemented,
        "multu": unimplemented,
        "mthi": unimplemented,
        "mtlo": unimplemented,
        "madd": unimplemented,
        "maddu": unimplemented,
        "msub": unimplemented,
        "msubu": unimplemented,
        "nop": unimplemented,
        # Unimplemented i-types
        "addiu": unimplemented,
        "andi": andi_command,
        "bgez": unimplemented,
        "blez": unimplemented,
        "lbu": unimplemented,
        "lh": unimplemented,
        "lhu": unimplemented,
        "lui": unimplemented,
        "ori": ori_command,
        "sb": unimplemented,
        "slti": unimplemented,
        "sltiu": unimplemented,
        "sh": unimplemented,
        "xori": unimplemented,
        "ll": unimplemented,
        "sc": unimplemented,
        "swl": unimplemented,
        "tgei": unimplemented,
        "teqi": unimplemented,
        "tgeiu": unimplemented,
        "tlti": unimplemented,
        "tltiu": unimplemented,
        "tnei": unimplemented,
    }[ast_class.command](ast_class)


def not_command(command):
    def exe():
        destination = command.destination_register
        source = command.source_register.get_contents_as_int()
        res = ~source
        destination.set_contents_from_int(res)

    return exe


def lb_command(command):
    def exe():
        destination = command.destination_register
        address = command.source_register.get_contents_as_int()
        res = Memory.get_byte(address)
        destination.set_contents_from_int(res)

    return exe


def xor_command(command):
    def exe():
        destination = command.destination_register
        source = command.source_register.get_contents_as_bytes()
        target = command.target_register.get_contents_as_bytes()
        res = [a ^ b for (a, b) in zip(source, target)]
        destination.set_contents_from_bytes(res)

    return exe


def and_command(command):
    def exe():
        destination = command.destination_register
        source = command.source_register.get_contents_as_bytes()
        target = command.target_register.get_contents_as_bytes()
        res = [a & b for (a, b) in zip(source, target)]
        destination.set_contents_from_bytes(res)

    return exe


def andi_command(command):
    def exe():
        destination = command.destination_register
        source = command.source_register.get_contents_as_bytes()
        immediate = command.immediate().to_bytes(5, "big", signed=True)
        res = [a & b for (a, b) in zip(source, immediate[-4:])]
        destination.set_contents_from_bytes(res)

    return exe


def or_command(command):
    def exe():
        destination = command.destination_register
        source = command.source_register.get_contents_as_bytes()
        target = command.target_register.get_contents_as_bytes()
        res = [a | b for (a, b) in zip(source, target)]
        destination.set_contents_from_bytes(res)

    return exe


def ori_command(command):
    def exe():
        destination = command.destination_register
        source = command.source_register.get_contents_as_bytes()
        immediate = command.immediate().to_bytes(5, "big", signed=True)
        res = [a | b for (a, b) in zip(source, immediate[-4:])]
        destination.set_contents_from_bytes(res)

    return exe


def addi_command(command):
    def exe():
        source = command.source_register.get_contents_as_int()
        imm = command.immediate()
        res = source + imm
        command.destination_register.set_contents_from_int(res)

    return exe


def mul_command(command):
    def exe():
        mfhi = RegisterPool.get_register("mfhi")
        mflo = RegisterPool.get_register("mflo")
        dest = command.destination_register
        source = command.source_register
        target = command.target_register

        result = source.get_contents_as_int() * target.get_contents_as_int()
        r = result.to_bytes(12, "big")
        hi = r[-8:-4]
        low = r[-4:]
        assert len(hi) == len(low)
        mfhi.set_contents_from_bytes(hi)
        mflo.set_contents_from_bytes(low)
        dest.set_contents_from_bytes(low)

    return exe


def mult_command(command):
    def exe():
        mfhi = RegisterPool.get_register("$mfhi")
        mflo = RegisterPool.get_register("$mflo")
        dest = command.destination_register
        source = command.source_register

        result = source.get_contents_as_int() * dest.get_contents_as_int()
        r = result.to_bytes(12, "big", signed=True)
        hi = r[-8:-4]
        low = r[-4:]
        assert len(hi) == len(low)
        mfhi.set_contents_from_bytes(hi)
        mflo.set_contents_from_bytes(low)
        print(mflo, mfhi)

    return exe


def j_command(command):
    def exe():
        ProgramStack.jump_label(command.address)
        ProgramStack.move_pc(-4)

    return exe


def jr_command(command):
    def exe():
        dest = command.destination_register.get_contents_as_int()
        pc = RegisterPool.get_register("$pc")
        pc.set_contents_from_int(dest - 4)

    return exe


def jal_command(command):
    def exe():
        pc = RegisterPool.get_register("$pc").get_contents_as_int()
        ra = RegisterPool.get_register("$ra")
        ra.set_contents_from_int(pc + 4)
        ProgramStack.jump_label(command.address)
        ProgramStack.move_pc(-4)

    return exe


def addu_command(command):
    def exe():
        dest = command.destination_register
        source = command.source_register.get_contents_as_bytes()
        target = command.target_register.get_contents_as_bytes()
        s = int.from_bytes(source, "big", signed=False)
        t = int.from_bytes(target, "big", signed=False)
        res = s + t
        dest.set_contents_from_int(res)

    return exe


def subu_command(command):
    def exe():
        dest = command.destination_register
        source = command.source_register.get_contents_as_bytes()
        target = command.target_register.get_contents_as_bytes()
        s = int.from_bytes(source, "big", signed=False)
        t = int.from_bytes(target, "big", signed=False)
        res = s - t
        dest.set_contents_from_int(res)

    return exe


def beq_command(command):
    def exe():
        dest = command.destination_register.get_contents_as_int()
        source = command.source_register.get_contents_as_int()
        if dest == source:
            ProgramStack.jump_label(command.immediate._value)
            ProgramStack.move_pc(-4)

    return exe


def bne_command(command):
    def exe():
        dest = command.destination_register.get_contents_as_int()
        source = command.source_register.get_contents_as_int()
        if dest != source:
            ProgramStack.jump_label(command.immediate._value)
            ProgramStack.move_pc(-4)

    return exe


def bnez_command(command):
    def exe():
        dest = command.destination_register.get_contents_as_int()
        if dest != 0:
            ProgramStack.jump_label(command.immediate._value)
            ProgramStack.move_pc(-4)

    return exe


def bltz_command(command):
    def exe():
        dest = command.destination_register.get_contents_as_int()
        if dest < 0:
            ProgramStack.jump_label(command.immediate._value)
            ProgramStack.move_pc(-4)

    return exe


def beqz_command(command):
    def exe():
        dest = command.destination_register.get_contents_as_int()
        if dest == 0:
            ProgramStack.jump_label(command.immediate._value)
            ProgramStack.move_pc(-4)

    return exe


def la_command(command):
    def exe():
        dest = command.destination_register
        if type(command.immediate._value) == str:
            address = DataHeap.get_address(command.immediate._value)
        else:
            address = command.immediate()
        dest.set_contents_from_int(address)

    return exe


def unimplemented(command):
    def exe():
        print(f"UNIMPLEMENTED {command}")

    return exe


def move_command(command):
    def exe():
        source = command.source_register.get_contents_as_int()
        command.destination_register.set_contents_from_int(source)

    return exe


def li_command(command):
    def exe():
        command.destination_register.set_contents_from_int(command.immediate())

    return exe


def lw_command(command):
    def exe():
        if command.source_register is None:
            imm = command.immediate()
            if type(imm) == int:
                command.destination_register.set_contents_from_int(imm)
            else:
                command.destination_register.set_contents_from_bytes(imm)
        else:
            dest = command.destination_register
            offset = command.immediate()
            register = command.source_register.name
            value = DataStack.load_word(offset, register=register)
            dest.set_contents_from_int(value)

    return exe


def mflo_command(command):
    def exe():
        mflo = RegisterPool.get_register("$mflo")
        command.destination_register.set_contents_from_bytes(
            mflo.get_contents_as_bytes()
        )

    return exe


def mfhi_command(command):
    def exe():
        mfhi = RegisterPool.get_register("$mfhi")
        command.destination_register.set_contents_from_bytes(
            mfhi.get_contents_as_bytes()
        )

    return exe


def div_command(command):
    def exe():
        quotient_res = (
            command.source_register.get_contents_as_int()
            // command.destination_register.get_contents_as_int()
        )
        remainder_res = (
            command.source_register.get_contents_as_int()
            % command.destination_register.get_contents_as_int()
        )
        mfhi = RegisterPool.get_register("$mfhi")
        mflo = RegisterPool.get_register("$mflo")
        mfhi.set_contents_from_int(lambda: remainder_res)
        mflo.set_contents_from_int(lambda: quotient_res)

    return exe


def add_command(command):
    def exe():
        dest = command.destination_register
        res = (
            command.source_register.get_contents_as_int()
            + command.target_register.get_contents_as_int()
        )
        dest.set_contents_from_int(res)

    return exe


def sub_command(command):
    def exe():
        dest = command.destination_register
        res = (
            command.source_register.get_contents_as_int()
            - command.target_register.get_contents_as_int()
        )
        dest.set_contents_from_int(res)

    return exe


def sw_command(command):
    def store_into_label():
        contents = command.destination_register.get_contents_as_int()
        DataHeap.store_word(contents, command.immediate._value)

    def store_on_stack():
        value = command.destination_register.get_contents_as_int()
        offset = command.immediate()
        register = command.source_register.name
        DataStack.store_word(offset, value, register=register)

    if command.source_register:
        return store_on_stack
    else:
        return store_into_label


def syscall_command(command):
    rp = RegisterPool
    v0 = rp.get_register("$v0")
    a0 = rp.get_register("$a0")
    a1 = rp.get_register("$a1")

    def print_int():
        num = a0.get_contents_as_int()
        print(num, end="")

    def print_float():
        pass

    def print_double():
        pass

    def print_string():
        address = a0.get_contents_as_int()
        s = Memory.load_asciiz(address)
        print(s, end="")

    def read_int():
        i = input()
        v0.set_contents_from_int(int(i))

    def end():
        print("\nEND OF PROGRAM")
        sys.exit()

    def read_string():
        size = a1.get_contents_as_int()
        address = a0.get_contents_as_int()
        contents = input()
        Memory.store_asciiz(contents[:size], address)

    def print_char():
        char = a0.get_contents_as_bytes()
        print(char.decode("ascii"), end="")

    def exe():
        return {
            1: print_int,
            2: print_float,
            3: print_double,
            4: print_string,
            5: read_int,
            8: read_string,
            10: end,
            11: print_char,
        }[v0.get_contents_as_int()]()

    return exe

