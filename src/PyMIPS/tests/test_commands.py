try:
    from src.PyMIPS.Datastructure.memory import Memory
    from src.PyMIPS.Datastructure.instruction_types import (
        IType,
        JType,
        RType,
        BaseCommand,
        DataStack,
        DataHeap,
    )

    from src.PyMIPS.Datastructure.data_model import RegisterPool, ProgramStack
except:
    from PyMIPS.Datastructure.memory import Memory
    from PyMIPS.Datastructure.data_model import (
        RegisterPool,
        ProgramStack,
        DataStack,
        DataHeap,
    )
    from PyMIPS.Datastructure.instruction_types import IType, JType, RType, BaseCommand

import unittest

"""
sll, srl, and sra are treated as I Types
"""


class TestRTypes(unittest.TestCase):
    def test_sllv(self):
        # TODO: sllv
        return

    def test_srlv(self):
        # TODO: srlv
        return

    def test_srav(self):
        # TODO: srav
        return

    def test_jr(self):
        pass

    def test_jalr(self):
        pass

    def test_jalr_2_r(self):
        pass

    def test_syscall(self):
        pass

    def test_mfhi(self):
        pass

    def test_mthi(self):
        pass

    def test_mflo(self):
        pass

    def test_mtlo(self):
        pass

    def test_mult(self):
        pass

    def test_multu(self):
        pass

    def test_div(self):
        # r = RType("div", "$t0", "$t1")
        # t0 = RegisterPool.get_register("$t0")
        # t1 = RegisterPool.get_register("$t1")
        # t0.set_contents_from_int(651)
        # t1.set_contents_from_int(213)
        # r()
        # quo = RegisterPool.get_register("mflo")
        # rem = RegisterPool.get_register("mfhi")
        # self.assertEqual(quo, 3)
        # self.assertEqual(rem, 12)
        pass

    def test_divu(self):
        pass

    def test_add(self):
        r = RType("add", "$t0", "$t1", "$t3")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t3 = RegisterPool.get_register("$t3")
        t1.set_contents_from_int(4)
        t3.set_contents_from_int(6)
        r()
        self.assertEqual(t0.get_contents_as_int(), 10)

    def test_addu(self):
        pass

    def test_sub(self):
        r = RType("sub", "$t0", "$t1", "$t3")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t3 = RegisterPool.get_register("$t3")
        t1.set_contents_from_int(1000)
        t3.set_contents_from_int(654)
        r()
        self.assertEqual(t0.get_contents_as_int(), 346)

    def test_subu(self):
        pass

    def test_and(self):
        r = RType("and", "$t0", "$s0", "$s1")
        t0 = RegisterPool.get_register("$t0")
        s0 = RegisterPool.get_register("$s0")
        s1 = RegisterPool.get_register("$s1")
        s0.set_contents_from_int(60)
        s1.set_contents_from_int(13)
        r()
        self.assertEqual(t0.get_contents_as_int(), 12)

    def test_or(self):
        r = RType("or", "$t0", "$s0", "$s1")
        t0 = RegisterPool.get_register("$t0")
        s0 = RegisterPool.get_register("$s0")
        s1 = RegisterPool.get_register("$s1")
        s0.set_contents_from_int(312)
        s1.set_contents_from_int(456)
        r()
        self.assertEqual(t0.get_contents_as_int(), 504)

    def test_xor(self):
        r = RType("xor", "$t0", "$s0", "$s1")
        t0 = RegisterPool.get_register("$t0")
        s0 = RegisterPool.get_register("$s0")
        s1 = RegisterPool.get_register("$s1")
        s0.set_contents_from_int(4651)
        s1.set_contents_from_int(65)
        r()
        self.assertEqual(t0.get_contents_as_int(), 4714)

    def test_nor(self):
        r = RType("nor", "$t1", "$s1", "$s2")
        t1 = RegisterPool.get_register("$t1")
        s1 = RegisterPool.get_register("$s1")
        s2 = RegisterPool.get_register("$s2")
        s1.set_contents_from_int(314)
        s2.set_contents_from_int(789)
        r()
        self.assertEqual(t1.get_contents_as_int(), 192)

    def test_slt(self):
        pass

    def test_sltu(self):
        pass


class TestJTypes(unittest.TestCase):
    pass


class TestITypes(unittest.TestCase):
    def test_sll(self):
        # TODO: sll
        i = IType("sll", "$t0", 2, "$t1")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t1.set_contents_from_int(4)
        i()
        # changed from 16 to 20 to test i-types that I am doing
        self.assertEqual(t0.get_contents_as_int(), 16)

    def test_srl(self):
        # TODO: srl
        return

    def test_sra(self):
        # TODO: sra
        return

    def test_beq(self):
        # TODO: ashton
        return

    def test_bne(self):
        pass

    def test_blez(self):
        pass

    def test_bgtz(self):
        pass

    def test_addi(self):
        i = IType("addi", "$t0", immediate=10, source="$t1")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t1.set_contents_from_int(10)
        i()
        self.assertEqual(t0.get_contents_as_int(), 20)

    def test_addiu(self):
        pass

    def test_slti(self):
        pass

    def test_sltiu(self):
        pass

    def test_andi(self):
        # i = IType("andi", "t0", 1, "$t1")
        # t0 = RegisterPool.get_register("t0")
        # t1 = RegisterPool.get_register("$t1")
        # t1.set_contents_from_bytes(1)
        pass

    def test_ori(self):
        i = IType("ori", "$t0", immediate=645, source="$s1")
        t0 = RegisterPool.get_register("$t0")
        s1 = RegisterPool.get_register("$s1")
        s1.set_contents_from_int(123)
        i()
        self.assertEqual(t0.get_contents_as_int(), 767)

    def test_xori(self):
        pass

    def test_lui(self):
        pass

    def test_lb(self):
        Memory.reset()
        DataStack.alloc(1024)
        i = IType("lb", "$t0", 10, "$t1")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t1.set_contents_from_int(123)
        res = Memory.get_byte(123)
        i()
        self.assertEqual(t0.get_contents_as_int(), res)

    def test_lh(self):
        pass

    def test_lw(self):
        Memory.reset()
        DataStack.alloc(1024)
        DataStack.store_word(4, 1203)
        i = IType("lw", "$t0", 4, source="$sp")
        t0 = RegisterPool.get_register("$t0")
        i()
        self.assertEqual(t0.get_contents_as_int(), 1203)

    def test_lbu(self):
        pass

    def test_sb(self):
        pass

    def test_sh(self):
        pass

    def test_sw_stack(self):
        Memory.reset()
        # sw $t0, 4($sp)
        DataStack.alloc(1024)
        i = IType("sw", "$t0", 4, "$sp")
        t0 = RegisterPool.get_register("$t0")
        t0.set_contents_from_int(673)
        i()
        self.assertEqual(DataStack.load_word(4, "$sp"), 673)

    def test_sw_heap(self):
        Memory.reset()
        DataHeap.reset()
        DataHeap.alloc(1024)
        DataHeap.store_word(218, "data")
        i = IType("sw", "$t0", "data")
        t0 = RegisterPool.get_register("$t0")
        t0.set_contents_from_int(1999)
        i()
        self.assertEqual(DataHeap.get_value_as_int("data"), 1999)
