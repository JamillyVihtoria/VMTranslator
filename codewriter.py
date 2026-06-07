class CodeWriter:
    SEGMENTS = {
        "local": "LCL",
        "argument": "ARG",
        "this": "THIS",
        "that": "THAT"
    }

    def __init__(self, filename):
        self.file = open(filename, "w")
        self.label_counter = 0
        import os
        self.filename = os.path.splitext(os.path.basename(filename))[0]

    def write_line(self, line):
        self.file.write(line + "\n")

    def close(self):
        self.file.close()

    def write_push(self, segment, index):

        # push constant x
        if segment == "constant":
            self.write_line(f"@{index}")
            self.write_line("D=A")

        # push local/argument/this/that
        elif segment in self.SEGMENTS:
            base = self.SEGMENTS[segment]

            self.write_line(f"@{base}")
            self.write_line("D=M")

            self.write_line(f"@{index}")
            self.write_line("A=D+A")

            self.write_line("D=M")

        # push temp x
        elif segment == "temp":
            self.write_line(f"@{5 + index}")
            self.write_line("D=M")

        # push pointer 0 → THIS, push pointer 1 → THAT
        elif segment == "pointer":
            reg = "THIS" if index == 0 else "THAT"
            self.write_line(f"@{reg}")
            self.write_line("D=M")

        # push static x → usa símbolo Filename.x
        elif segment == "static":
            self.write_line(f"@{self.filename}.{index}")
            self.write_line("D=M")

        else:
            raise ValueError(f"Segmento não suportado: {segment}")

        # empilha D na stack
        self.write_line("@SP")
        self.write_line("A=M")
        self.write_line("M=D")

        self.write_line("@SP")
        self.write_line("M=M+1")

    def write_pop(self, segment, index):

        # pop local/argument/this/that
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

        # pop temp x
        elif segment == "temp":

            self.write_line("@SP")
            self.write_line("AM=M-1")
            self.write_line("D=M")

            self.write_line(f"@{5 + index}")
            self.write_line("M=D")

        # pop pointer 0 → THIS, pop pointer 1 → THAT
        elif segment == "pointer":
            reg = "THIS" if index == 0 else "THAT"

            self.write_line("@SP")
            self.write_line("AM=M-1")
            self.write_line("D=M")

            self.write_line(f"@{reg}")
            self.write_line("M=D")

        # pop static x → usa símbolo Filename.x
        elif segment == "static":

            self.write_line("@SP")
            self.write_line("AM=M-1")
            self.write_line("D=M")

            self.write_line(f"@{self.filename}.{index}")
            self.write_line("M=D")

        else:
            raise ValueError(f"Segmento não suportado: {segment}")

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
            # Mapeia comando → instrução de salto
            jump = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}[command]
            label_true = f"TRUE_{self.label_counter}"
            label_end  = f"END_{self.label_counter}"
            self.label_counter += 1

            # D = topo - segundo topo
            self.write_line("@SP")
            self.write_line("AM=M-1")
            self.write_line("D=M")

            self.write_line("A=A-1")
            self.write_line("D=M-D")

            # Se condição verdadeira, pula para TRUE
            self.write_line(f"@{label_true}")
            self.write_line(f"D;{jump}")

            # Falso: coloca 0 (false) e pula pro fim
            self.write_line("@SP")
            self.write_line("A=M-1")
            self.write_line("M=0")
            self.write_line(f"@{label_end}")
            self.write_line("0;JMP")

            # Verdadeiro: coloca -1 (true em Hack)
            self.write_line(f"({label_true})")
            self.write_line("@SP")
            self.write_line("A=M-1")
            self.write_line("M=-1")

            self.write_line(f"({label_end})")

        else:
            raise ValueError(f"Comando aritmético não suportado: {command}")