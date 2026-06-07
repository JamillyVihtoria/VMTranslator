import unittest
import os
import tempfile

from parser import Parser, CommandType
from codewriter import CodeWriter


# ── Helpers ──────────────────────────────────────────────────────────────────

def make_vm_file(lines):
    """Cria um arquivo .vm temporário com as linhas fornecidas."""
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".vm", delete=False)
    f.write("\n".join(lines))
    f.close()
    return f.name


def make_asm_file():
    """Cria um arquivo .asm temporário vazio para o CodeWriter escrever."""
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".asm", delete=False)
    f.close()
    return f.name


# ── Testes do Parser ─────────────────────────────────────────────────────────

class TestParser(unittest.TestCase):

    def test_ignora_comentarios_e_linhas_vazias(self):
        path = make_vm_file([
            "// comentário",
            "",
            "push constant 7  // inline comment",
            "add",
        ])
        p = Parser(path)
        self.assertEqual(len(p.commands), 2)
        os.unlink(path)

    def test_command_type_push(self):
        path = make_vm_file(["push constant 3"])
        p = Parser(path)
        p.advance()
        self.assertEqual(p.command_type(), CommandType.C_PUSH)
        os.unlink(path)

    def test_command_type_pop(self):
        path = make_vm_file(["pop local 0"])
        p = Parser(path)
        p.advance()
        self.assertEqual(p.command_type(), CommandType.C_POP)
        os.unlink(path)

    def test_command_type_arithmetic(self):
        for cmd in ("add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"):
            path = make_vm_file([cmd])
            p = Parser(path)
            p.advance()
            self.assertEqual(p.command_type(), CommandType.C_ARITHMETIC, msg=cmd)
            os.unlink(path)

    def test_arg1_push(self):
        path = make_vm_file(["push local 2"])
        p = Parser(path)
        p.advance()
        self.assertEqual(p.arg1(), "local")
        os.unlink(path)

    def test_arg2_push(self):
        path = make_vm_file(["push constant 99"])
        p = Parser(path)
        p.advance()
        self.assertEqual(p.arg2(), 99)
        os.unlink(path)

    def test_arg1_arithmetic(self):
        path = make_vm_file(["add"])
        p = Parser(path)
        p.advance()
        self.assertEqual(p.arg1(), "add")
        os.unlink(path)

    def test_has_more_commands(self):
        path = make_vm_file(["push constant 1", "push constant 2", "add"])
        p = Parser(path)
        count = 0
        while p.has_more_commands():
            p.advance()
            count += 1
        self.assertEqual(count, 3)
        os.unlink(path)


# ── Testes do CodeWriter ──────────────────────────────────────────────────────

class TestCodeWriter(unittest.TestCase):

    def _get_asm(self, fn):
        """Executa fn(writer) e retorna as linhas geradas no .asm."""
        path = make_asm_file()
        writer = CodeWriter(path)
        fn(writer)
        writer.close()
        with open(path) as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
        os.unlink(path)
        return lines

    def test_push_constant(self):
        lines = self._get_asm(lambda w: w.write_push("constant", 7))
        self.assertIn("@7", lines)
        self.assertIn("D=A", lines)
        self.assertIn("@SP", lines)
        self.assertIn("M=M+1", lines)

    def test_push_local(self):
        lines = self._get_asm(lambda w: w.write_push("local", 2))
        self.assertIn("@LCL", lines)
        self.assertIn("@2", lines)
        self.assertIn("D=M", lines)

    def test_push_temp(self):
        lines = self._get_asm(lambda w: w.write_push("temp", 3))
        self.assertIn("@8", lines)  # 5 + 3

    def test_push_pointer_0(self):
        lines = self._get_asm(lambda w: w.write_push("pointer", 0))
        self.assertIn("@THIS", lines)

    def test_push_pointer_1(self):
        lines = self._get_asm(lambda w: w.write_push("pointer", 1))
        self.assertIn("@THAT", lines)

    def test_pop_local(self):
        lines = self._get_asm(lambda w: w.write_pop("local", 0))
        self.assertIn("@LCL", lines)
        self.assertIn("@R13", lines)

    def test_pop_temp(self):
        lines = self._get_asm(lambda w: w.write_pop("temp", 0))
        self.assertIn("@5", lines)

    def test_pop_pointer_0(self):
        lines = self._get_asm(lambda w: w.write_pop("pointer", 0))
        self.assertIn("@THIS", lines)

    def test_arithmetic_add(self):
        lines = self._get_asm(lambda w: w.write_arithmetic("add"))
        self.assertIn("M=M+D", lines)

    def test_arithmetic_sub(self):
        lines = self._get_asm(lambda w: w.write_arithmetic("sub"))
        self.assertIn("M=M-D", lines)

    def test_arithmetic_neg(self):
        lines = self._get_asm(lambda w: w.write_arithmetic("neg"))
        self.assertIn("M=-M", lines)

    def test_arithmetic_and(self):
        lines = self._get_asm(lambda w: w.write_arithmetic("and"))
        self.assertIn("M=D&M", lines)

    def test_arithmetic_or(self):
        lines = self._get_asm(lambda w: w.write_arithmetic("or"))
        self.assertIn("M=D|M", lines)

    def test_arithmetic_not(self):
        lines = self._get_asm(lambda w: w.write_arithmetic("not"))
        self.assertIn("M=!M", lines)

    def test_arithmetic_eq_gera_labels_unicos(self):
        path = make_asm_file()
        writer = CodeWriter(path)
        writer.write_arithmetic("eq")
        writer.write_arithmetic("eq")
        writer.close()
        with open(path) as f:
            content = f.read()
        self.assertIn("TRUE_0", content)
        self.assertIn("TRUE_1", content)
        os.unlink(path)

    def test_arithmetic_gt(self):
        lines = self._get_asm(lambda w: w.write_arithmetic("gt"))
        self.assertIn("D;JGT", lines)

    def test_arithmetic_lt(self):
        lines = self._get_asm(lambda w: w.write_arithmetic("lt"))
        self.assertIn("D;JLT", lines)


if __name__ == "__main__":
    unittest.main()
