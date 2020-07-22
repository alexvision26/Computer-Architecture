"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0] * 256

    def load(self, file_name):
        """Load a program into memory."""

        try:
            address = 0
            with open(file_name) as program:
                for line in program:
                    split_line = line.split('#')[0]
                    command = split_line.strip()

                    if command == '':
                        continue

                    instruction = int(command, 2)
                    self.ram[address] = instruction

                    address += 1

        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
            sys.exit()

        # for x in self.ram:
        #     print(bin(x))


        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        HALT = 0b00000001
        POP = 0b01000110
        # SAVE = 0b100
        PUSH = 0b01000101
        # ADD = 0b110
        # PRINT_REG = 0b101
        # PRINT_NUM = 0b00000011

        self.reg[7] = 0xA

        pc = 0
        running = True
        while running:
            command = self.ram[pc]

            # print(command)

            # print("Command: ", bin(command))

            if command == LDI:
                reg = self.ram[pc + 1]
                num_to_save = self.ram[pc + 2]
                self.reg[reg] = num_to_save
                # print('ran')
                
                pc += 2

            if command == PRN:
                # print('ran')
                reg = self.ram[pc + 1]
                print(self.reg[reg])

                pc += 1

            # if command == PRINT_NUM:
            #     num_to_print = self.ram[pc + 1]
            #     print(num_to_print)
            #     pc += 1

            # if command == SAVE:
            #     reg = self.ram[pc + 1]
            #     num_to_save = self.ram[pc + 2]
            #     self.reg[reg] = num_to_save

            #     pc += 2

            # if command == PRINT_REG:
            #     reg_index = self.ram[pc + 1]
            #     print(self.reg[reg_index])
            #     pc += 1

            if command == MUL:
                regA = self.ram[pc + 1]
                regB = self.ram[pc + 2]
                self.alu('MUL', regA, regB)

                pc += 2


            # if command == ADD:
            #     regA = self.ram[pc + 1]
            #     regB = self.ram[pc + 2]

            #     self.alu('ADD', regA, regB)
            #     # print(self.reg[regA])

            if command == PUSH:
                # print('ran push')
                self.reg[7] -= 1
                reg = self.ram[pc + 1]
                value = self.reg[reg]
                sp = self.reg[7]
                self.ram[sp] = value

                pc += 1

            if command == POP:
                sp = self.reg[7]

                reg = self.ram[pc + 1]
                value = self.ram[sp]
                self.reg[reg] = value
                self.reg[7] += 1

                pc += 1

            if command == HALT:
                running = False

            pc += 1

        # for x in self.reg:
        #     # if x != 0:
        #     print(x)



    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
        return f'Value stored.'
