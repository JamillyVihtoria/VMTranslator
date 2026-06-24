import sys
import os

from parser import Parser, CommandType
from codewriter import CodeWriter


def translate(parser, writer):
    while parser.has_more_commands():
        parser.advance()
        ctype = parser.command_type()

        if ctype == CommandType.C_ARITHMETIC:
            writer.write_arithmetic(parser.arg1())
        elif ctype == CommandType.C_PUSH:
            writer.write_push(parser.arg1(), parser.arg2())
        elif ctype == CommandType.C_POP:
            writer.write_pop(parser.arg1(), parser.arg2())
        elif ctype == CommandType.C_LABEL:
            writer.write_label(parser.arg1())
        elif ctype == CommandType.C_GOTO:
            writer.write_goto(parser.arg1())
        elif ctype == CommandType.C_IF:
            writer.write_if(parser.arg1())
        elif ctype == CommandType.C_FUNCTION:
            writer.write_function(parser.arg1(), parser.arg2())
        elif ctype == CommandType.C_CALL:
            writer.write_call(parser.arg1(), parser.arg2())
        elif ctype == CommandType.C_RETURN:
            writer.write_return()


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo.vm | diretório>")
        sys.exit(1)

    input_path = sys.argv[1]

    if os.path.isdir(input_path):
        # Modo diretório: bootstrap ativado, gera NomeDir.asm
        dir_name = os.path.basename(os.path.abspath(input_path))
        output_file = os.path.join(input_path, dir_name + ".asm")

        vm_files = sorted([f for f in os.listdir(input_path) if f.endswith(".vm")])

        if not vm_files:
            print(f"Nenhum arquivo .vm encontrado em: {input_path}")
            sys.exit(1)

        writer = CodeWriter(output_file, bootstrap=True)

        for vm_file in vm_files:
            full_path = os.path.join(input_path, vm_file)
            writer.set_filename(vm_file)
            parser = Parser(full_path)
            translate(parser, writer)

        writer.close()
        print(f"Arquivo gerado: {output_file}")

    else:
        # Modo arquivo único: sem bootstrap
        if not input_path.endswith(".vm"):
            print("Erro: o arquivo de entrada deve ter extensão .vm")
            sys.exit(1)

        output_file = input_path.replace(".vm", ".asm")
        writer = CodeWriter(output_file, bootstrap=False)
        writer.set_filename(input_path)

        parser = Parser(input_path)
        translate(parser, writer)

        writer.close()
        print(f"Arquivo gerado: {output_file}")


if __name__ == "__main__":
    main()