import sys

from parser import Parser, CommandType
from codewriter import CodeWriter


def main():

    input_file = sys.argv[1]

    output_file = input_file.replace(".vm", ".asm")

    parser = Parser(input_file)
    writer = CodeWriter(output_file)

    while parser.has_more_commands():

        parser.advance()

        ctype = parser.command_type()

        if ctype == CommandType.C_ARITHMETIC:
            writer.write_arithmetic(parser.arg1())

        elif ctype == CommandType.C_PUSH:
            writer.write_push(parser.arg1(), parser.arg2())

        elif ctype == CommandType.C_POP:
            writer.write_pop(parser.arg1(), parser.arg2())

    writer.close()
    print(f"Arquivo gerado com sucesso: {output_file}")


if __name__ == "__main__":
    main()