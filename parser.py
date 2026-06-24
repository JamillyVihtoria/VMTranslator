from enum import Enum


class CommandType(Enum):
    C_ARITHMETIC = 1
    C_PUSH = 2
    C_POP = 3
    C_LABEL = 4
    C_GOTO = 5
    C_IF = 6
    C_FUNCTION = 7
    C_CALL = 8
    C_RETURN = 9


class Parser:
    def __init__(self, filename):
        self.commands = []

        with open(filename, "r") as f:
            for line in f:
                line = line.split("//")[0].strip()

                if line:
                    self.commands.append(line)

        self.current = None
        self.index = 0

    def has_more_commands(self):
        return self.index < len(self.commands)

    def advance(self):
        self.current = self.commands[self.index]
        self.index += 1

    def command_type(self):
        cmd = self.current.split()[0]

        if cmd == "push":
            return CommandType.C_PUSH
        if cmd == "pop":
            return CommandType.C_POP
        if cmd == "label":
            return CommandType.C_LABEL
        if cmd == "goto":
            return CommandType.C_GOTO
        if cmd == "if-goto":
            return CommandType.C_IF
        if cmd == "function":
            return CommandType.C_FUNCTION
        if cmd == "call":
            return CommandType.C_CALL
        if cmd == "return":
            return CommandType.C_RETURN

        return CommandType.C_ARITHMETIC

    def arg1(self):
        parts = self.current.split()

        if self.command_type() == CommandType.C_ARITHMETIC:
            return parts[0]

        return parts[1]

    def arg2(self):
        return int(self.current.split()[2])
