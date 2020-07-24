"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0] * 256
        self.flag = 0b00000000

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
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001

            if self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100

            if self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010
        elif op == 'MOD':
            # self.reg[reg_a] = self.reg[reg_a] 
            pass
        elif op == 'OR':
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == 'XOR':
            pass
        elif op == 'SHL':
            pass
        elif op == 'SHR':
            pass
        elif op == 'AND':
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        elif op == 'NOT':
            self.reg[reg_a] = ~self.reg[reg_a]
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
        HALT = 0b00000001
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        SAVE = 0b00000100
        PUSH = 0b01000101
        JEQ = 0b01010101
        JMP = 0b01010100
        JNE = 0b01010110

        #Math Ops
        OR = 0b10101010
        MUL = 0b10100010
        ADD = 0b10100000
        CMP = 0b10100111
        XOR = 0b10101011
        SHL = 0b10101100
        SHR = 0b10101101
        MOD = 0b10100100
        AND = 0b10101000
        NOT = 0b01101001

        # PRINT_REG = 0b101
        # PRINT_NUM = 0b00000011

        self.reg[7] = 0xF4

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
                
                pc += 3

            if command == PRN:
                # print('ran')
                reg = self.ram[pc + 1]
                print(self.reg[reg])

                pc += 2

            if command == JEQ:
                reg = self.ram[pc + 1]
                address = self.reg[reg]

                if self.flag == 0b00000001:
                    pc = address
                else:
                    pc += 2

            if command == JMP:
                reg = self.ram[pc + 1]
                address = self.reg[reg]
                # print('Jump')
                pc = address

            if command == CMP:
                regA = self.ram[pc + 1]
                regB = self.ram[pc + 2]

                self.alu('CMP', regA, regB)

                pc += 3

            if command == JNE:
                reg = self.ram[pc + 1]
                address = self.reg[reg]

                if self.flag == 0b00000100 or self.flag == 0b00000010:
                    pc = address
                else:
                    pc += 2

            if command == SAVE:
                reg = self.ram[pc + 1]
                num_to_save = self.ram[pc + 2]
                self.reg[reg] = num_to_save

                pc += 3

            if command == CALL:
                reg = self.ram[pc + 1]
                address = self.reg[reg]
                return_address = pc + 2
                self.reg[7] -= 1
                sp = self.reg[7]

                self.ram[sp] = return_address

                pc = address

            if command == RET:
                sp = self.reg[7]
                return_address = self.ram[sp]
                self.reg[7] += 1

                pc = return_address

            # if command == PRINT_REG:
            #     reg_index = self.ram[pc + 1]
            #     print(self.reg[reg_index])
            #     pc += 1

            if command == MUL:
                regA = self.ram[pc + 1]
                regB = self.ram[pc + 2]
                self.alu('MUL', regA, regB)

                pc += 3


            if command == ADD:
                regA = self.ram[pc + 1]
                regB = self.ram[pc + 2]

                self.alu('ADD', regA, regB)
                # print(self.reg[regA])

                pc += 3

            if command == PUSH:
                # print('ran push')
                self.reg[7] -= 1
                reg = self.ram[pc + 1]
                value = self.reg[reg]
                sp = self.reg[7]
                self.ram[sp] = value

                pc += 2

            if command == POP:
                sp = self.reg[7]

                reg = self.ram[pc + 1]
                value = self.ram[sp]
                self.reg[reg] = value
                self.reg[7] += 1

                pc += 2

            if command == HALT:
                running = False

            # pc += 1

        # for x in self.reg:
        #     # if x != 0:
        #     print(x)



    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
        return f'Value stored.'
