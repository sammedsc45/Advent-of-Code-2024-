import re

def read_input(file_path):
    """Reads the input file and extracts initial registers and the program."""
    with open(file_path, 'r') as file:
        data = file.read()
    a, b, c, *program = map(int, re.findall(r'\d+', data))
    return {'A': a, 'B': b, 'C': c}, program

class Computer:
    """Represents the 3-bit computer."""
    def __init__(self, program, registers):
        self.program = program
        self.registers = registers.copy()
        self.ip = 0  # Instruction pointer
        self.output = []

    def _opval(self, operand, is_combo):
        """Fetch operand value based on its type."""
        if is_combo:
            if operand in (4, 5, 6):
                return self.registers['ABC'[operand - 4]]
            return operand
        return operand

    def tick(self):
        """Executes a single instruction cycle."""
        if self.ip >= len(self.program):
            return False  # Halt

        opcode = self.program[self.ip]
        operand = self.program[self.ip + 1]
        jump = self.ip + 2
        is_combo = True  # Assume combo operand

        if opcode == 0:  # adv: A >>= 2^operand
            denom = 2 ** self._opval(operand, is_combo)
            self.registers['A'] //= denom
        elif opcode == 1:  # bxl: B ^= literal
            is_combo = False
            self.registers['B'] ^= operand
        elif opcode == 2:  # bst: B = operand % 8
            value = self._opval(operand, is_combo)
            self.registers['B'] = value % 8
        elif opcode == 3:  # jnz: Jump if A != 0
            is_combo = False
            if self.registers['A'] != 0:
                jump = operand
        elif opcode == 4:  # bxc: B ^= C
            self.registers['B'] ^= self.registers['C']
        elif opcode == 5:  # out: Output operand % 8
            value = self._opval(operand, is_combo)
            self.output.append(str(value % 8))
        elif opcode == 6:  # bdv: B = A >> 2^operand
            denom = 2 ** self._opval(operand, is_combo)
            self.registers['B'] = self.registers['A'] // denom
        elif opcode == 7:  # cdv: C = A >> 2^operand
            denom = 2 ** self._opval(operand, is_combo)
            self.registers['C'] = self.registers['A'] // denom
        else:
            raise ValueError(f"Invalid opcode: {opcode}")

        self.ip = jump
        return True

    def run(self):
        """Runs the program to completion and returns the output."""
        while self.tick():
            pass
        return ','.join(self.output)

    def reset(self, a, b, c):
        """Resets the computer's registers and output for reuse."""
        self.registers = {'A': a, 'B': b, 'C': c}
        self.ip = 0
        self.output = []


def part1(program, registers):
    """Solves Part 1: Executes the program and prints its output."""
    comp = Computer(program, registers)
    result = comp.run()
    print("Part 1 Output:", result)
    return result


def part2(program):
    """Solves Part 2: Finds the lowest value for register A that outputs a copy of the program."""
    def run_program(a, b, c):
        "Runs the program with the specified initial registers and returns the output."
        comp = Computer(program, {'A': a, 'B': b, 'C': c})
        comp.run()
        return list(map(int, comp.output))

    todo = [(1, 0)]
    for i, a in todo:
        for a in range(a, a + 8):
            if run_program(a, 0, 0) == program[-i:]:
                todo.append((i + 1, a * 8))
                if i == len(program):
                    print("Part 2 Result:", a)
                    return a


def main(file_path):
    registers, program = read_input(file_path)
    # Solve Part 1
    part1_output = part1(program, registers)
    # Solve Part 2
    part2_result = part2(program)

if __name__ == "__main__":
    main("input.txt")
