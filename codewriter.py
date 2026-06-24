import os


class CodeWriter:
    SEGMENTS = {
        "local": "LCL",
        "argument": "ARG",
        "this": "THIS",
        "that": "THAT"
    }

    def __init__(self, filename, bootstrap=False):
        self.file = open(filename, "w")
        self.label_counter = 0
        self.return_counter = 0
        self.current_function = ""
        self.filename = os.path.splitext(os.path.basename(filename))[0]
        if bootstrap:
            self._write_bootstrap()

    def _write_bootstrap(self):
        """Bootstrap: SP=256 e call Sys.init 0."""
        self.write_line("// Bootstrap")
        self.write_line("@256")
        self.write_line("D=A")
        self.write_line("@SP")
        self.write_line("M=D")
        self.write_call("Sys.init", 0)

    def set_filename(self, filename):
        """Atualiza o prefixo usado para variáveis static."""
        self.filename = os.path.splitext(os.path.basename(filename))[0]

    def write_line(self, line):
        self.file.write(line + "\n")

    def close(self):
        self.file.close()

    # ── Push / Pop ────────────────────────────────────────────────────────────

    def write_push(self, segment, index):

        if segment == "constant":
            self.write_line(f"@{index}")
            self.write_line("D=A")

        elif segment in self.SEGMENTS:
            base = self.SEGMENTS[segment]
            self.write_line(f"@{base}")
            self.write_line("D=M")
            self.write_line(f"@{index}")
            self.write_line("A=D+A")
            self.write_line("D=M")

        elif segment == "temp":
            self.write_line(f"@{5 + index}")
            self.write_line("D=M")

        elif segment == "pointer":
            reg = "THIS" if index == 0 else "THAT"
            self.write_line(f"@{reg}")
            self.write_line("D=M")

        elif segment == "static":
            self.write_line(f"@{self.filename}.{index}")
            self.write_line("D=M")

        else:
            raise ValueError(f"Segmento não suportado: {segment}")

        self.write_line("@SP")
        self.write_line("A=M")
        self.write_line("M=D")
        self.write_line("@SP")
        self.write_line("M=M+1")

    def write_pop(self, segment, index):

        if segment in self.SEGMENTS:
            base = self.SEGMENTS[segment]
            self.write_line(f"@{base}")
            self.write_line("D=M")
            self.write_line(f"@{index}")
            self.write_line("D=D+A")
            self.write_line("@R13")
            self.write_line("M=D")
            self.write_line("@SP")
            self.write_line("AM=M-1")
            self.write_line("D=M")
            self.write_line("@R13")
            self.write_line("A=M")
            self.write_line("M=D")

        elif segment == "temp":
            self.write_line("@SP")
            self.write_line("AM=M-1")
            self.write_line("D=M")
            self.write_line(f"@{5 + index}")
            self.write_line("M=D")

        elif segment == "pointer":
            reg = "THIS" if index == 0 else "THAT"
            self.write_line("@SP")
            self.write_line("AM=M-1")
            self.write_line("D=M")
            self.write_line(f"@{reg}")
            self.write_line("M=D")

        elif segment == "static":
            self.write_line("@SP")
            self.write_line("AM=M-1")
            self.write_line("D=M")
            self.write_line(f"@{self.filename}.{index}")
            self.write_line("M=D")

        else:
            raise ValueError(f"Segmento não suportado: {segment}")

    # ── Aritmética ────────────────────────────────────────────────────────────

    def write_arithmetic(self, command):

        if command == "add":
            self.write_line("@SP")
            self.write_line("AM=M-1")
            self.write_line("D=M")
            self.write_line("A=A-1")
            self.write_line("M=M+D")

        elif command == "sub":
            self.write_line("@SP")
            self.write_line("AM=M-1")
            self.write_line("D=M")
            self.write_line("A=A-1")
            self.write_line("M=M-D")

        elif command == "neg":
            self.write_line("@SP")
            self.write_line("A=M-1")
            self.write_line("M=-M")

        elif command == "and":
            self.write_line("@SP")
            self.write_line("AM=M-1")
            self.write_line("D=M")
            self.write_line("A=A-1")
            self.write_line("M=D&M")

        elif command == "or":
            self.write_line("@SP")
            self.write_line("AM=M-1")
            self.write_line("D=M")
            self.write_line("A=A-1")
            self.write_line("M=D|M")

        elif command == "not":
            self.write_line("@SP")
            self.write_line("A=M-1")
            self.write_line("M=!M")

        elif command in ("eq", "gt", "lt"):
            jump = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}[command]
            label_true = f"TRUE_{self.label_counter}"
            label_end  = f"END_{self.label_counter}"
            self.label_counter += 1

            self.write_line("@SP")
            self.write_line("AM=M-1")
            self.write_line("D=M")
            self.write_line("A=A-1")
            self.write_line("D=M-D")

            self.write_line(f"@{label_true}")
            self.write_line(f"D;{jump}")

            self.write_line("@SP")
            self.write_line("A=M-1")
            self.write_line("M=0")
            self.write_line(f"@{label_end}")
            self.write_line("0;JMP")

            self.write_line(f"({label_true})")
            self.write_line("@SP")
            self.write_line("A=M-1")
            self.write_line("M=-1")

            self.write_line(f"({label_end})")

        else:
            raise ValueError(f"Comando aritmético não suportado: {command}")

    # ── Controle de Fluxo ─────────────────────────────────────────────────────

    def write_label(self, label):
        self.write_line(f"({self.current_function}${label})")

    def write_goto(self, label):
        self.write_line(f"@{self.current_function}${label}")
        self.write_line("0;JMP")

    def write_if(self, label):
        self.write_line("@SP")
        self.write_line("AM=M-1")
        self.write_line("D=M")
        self.write_line(f"@{self.current_function}${label}")
        self.write_line("D;JNE")

    # ── Funções ───────────────────────────────────────────────────────────────

    def write_function(self, function_name, n_locals):
        self.current_function = function_name
        self.write_line(f"({function_name})")
        for _ in range(n_locals):
            self.write_push("constant", 0)

    def write_call(self, function_name, n_args):
        ret_label = f"{function_name}$ret{self.return_counter}"
        self.return_counter += 1

        # 1. push return address
        self.write_line(f"@{ret_label}")
        self.write_line("D=A")
        self.write_line("@SP")
        self.write_line("A=M")
        self.write_line("M=D")
        self.write_line("@SP")
        self.write_line("M=M+1")

        # 2. push LCL, ARG, THIS, THAT
        for reg in ("LCL", "ARG", "THIS", "THAT"):
            self.write_line(f"@{reg}")
            self.write_line("D=M")
            self.write_line("@SP")
            self.write_line("A=M")
            self.write_line("M=D")
            self.write_line("@SP")
            self.write_line("M=M+1")

        # 3. ARG = SP - 5 - nArgs
        self.write_line("@SP")
        self.write_line("D=M")
        self.write_line(f"@{5 + n_args}")
        self.write_line("D=D-A")
        self.write_line("@ARG")
        self.write_line("M=D")

        # 4. LCL = SP
        self.write_line("@SP")
        self.write_line("D=M")
        self.write_line("@LCL")
        self.write_line("M=D")

        # 5. goto fname
        self.write_line(f"@{function_name}")
        self.write_line("0;JMP")

        # 6. return label
        self.write_line(f"({ret_label})")

    def write_return(self):
        # endFrame = LCL → R14
        self.write_line("@LCL")
        self.write_line("D=M")
        self.write_line("@R14")
        self.write_line("M=D")

        # retAddr = *(endFrame - 5) → R15
        self.write_line("@5")
        self.write_line("A=D-A")
        self.write_line("D=M")
        self.write_line("@R15")
        self.write_line("M=D")

        # *ARG = pop()
        self.write_line("@SP")
        self.write_line("AM=M-1")
        self.write_line("D=M")
        self.write_line("@ARG")
        self.write_line("A=M")
        self.write_line("M=D")

        # SP = ARG + 1
        self.write_line("@ARG")
        self.write_line("D=M+1")
        self.write_line("@SP")
        self.write_line("M=D")

        # Restaura THAT, THIS, ARG, LCL (endFrame-1, -2, -3, -4)
        for i, reg in enumerate(("THAT", "THIS", "ARG", "LCL"), start=1):
            self.write_line("@R14")
            self.write_line("D=M")
            self.write_line(f"@{i}")
            self.write_line("A=D-A")
            self.write_line("D=M")
            self.write_line(f"@{reg}")
            self.write_line("M=D")

        # goto retAddr
        self.write_line("@R15")
        self.write_line("A=M")
        self.write_line("0;JMP")
