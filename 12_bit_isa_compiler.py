import sys
#opcode map (4 bit)
OPCODES = {
    'add':  '0000',
    'addi': '0001',
    'sub':  '0010',
    'subi': '0011',
    'and':  '0100',
    'sll':  '0101',
    'or':   '0110',
    'xor':  '0111',
    'nand': '1000',
    'lw':   '1001',
    'sw':   '1010',
    'beq':  '1011',
    'bne':  '1100',
    'slt':  '1101',
    'slti': '1110',
    'j':    '1111',
}

# Register map (4 bits)
REGISTERS = {
    '$zero': '0000',
    '$s0':   '0001',
    '$s1':   '0010',
    '$s2':   '0011',
    '$s3':   '0100',
    '$s4':   '0101',
    '$s5':   '0110',
    '$s6':   '0111',
    '$t0':   '1000',
    '$t1':   '1001',
    '$t2':   '1010',
    '$t3':   '1011',
    '$t4':   '1100',
    '$t5':   '1101',
    '$t6':   '1110',
    '$t7':   '1111',
}

def to_bin(value, bits, signed=False):
    """Convert integer to binary string, handling signed values."""
    if signed:
        min_val, max_val = -(1 << (bits-1)), (1 << (bits-1)) - 1
        if not (min_val <= value <= max_val):
            raise ValueError(f"Value {value} out of {bits}-bit signed range")
        if value < 0:
            value = (1 << bits) + value
    else:
        if value < 0 or value >= (1 << bits):
            raise ValueError(f"Value {value} out of {bits}-bit unsigned range")
    return format(value, f'0{bits}b')

def parse_register(reg):
    reg = reg.strip().lower()
    if reg not in REGISTERS:
        raise ValueError(f"Unknown register: {reg}")
    return REGISTERS[reg]

def assemble_line(line, labels=None, pc=0):
    line = line.strip()
    if not line or line.startswith('#') or line.endswith(':'):
        return None

    line = line.split('#')[0].strip()
    parts = line.replace(',', ' ').split()
    if not parts:
        return None

    instr = parts[0].lower()
    if instr not in OPCODES:
        raise ValueError(f"Invalid instruction: {instr}")

    opcode = OPCODES[instr]

    # J-Type: j target
    if instr == 'j':
        if len(parts) != 2:
            raise ValueError(f"Invalid syntax for 'j': {line}")
        target = parts[1]
        if labels and target in labels:
            addr = labels[target]
        else:
            try:
                addr = int(target)
            except ValueError:
                raise ValueError(f"Invalid target address: {target}")
        return opcode + to_bin(addr, 8)

    # R-Type: add, sub, and, or, xor, nand, slt
    if instr in ['add', 'sub', 'and', 'or', 'xor', 'nand', 'slt']:
        if len(parts) != 3:
            raise ValueError(f"Invalid syntax for '{instr}': {line}")
        dest = parse_register(parts[1])
        src = parse_register(parts[2])
        return opcode + dest + src + to_bin(0, 4)  # Padding

    # I-Type: addi, subi, sll, slti
    if instr in ['addi', 'subi', 'sll', 'slti']:
        if len(parts) != 3:
            raise ValueError(f"Invalid syntax for '{instr}': {line}")
        dest = parse_register(parts[1])
        imm = int(parts[2])
        imm_bin = to_bin(imm, 4, signed=(instr in ['addi', 'subi', 'slti']))
        return opcode + dest + imm_bin

    # Memory Instructions: lw/sw $reg, $base, offset
    if instr in ['lw', 'sw']:
        if len(parts) != 4:
            raise ValueError(f"Invalid syntax for '{instr}': {line}")
        reg = parse_register(parts[1])
        base = parse_register(parts[2])
        offset = int(parts[3])
        offset_bin = to_bin(offset, 4, signed=True)
        return opcode + reg + base + offset_bin

    # Branch Instructions: beq/bne $s1, $s2, offset
    if instr in ['beq', 'bne']:
        if len(parts) != 4:
            raise ValueError(f"Invalid syntax for '{instr}': {line}")
        s1 = parse_register(parts[1])
        s2 = parse_register(parts[2])
        label = parts[3]

        if labels and label in labels:
            offset_val = labels[label] - (pc + 1)  # PC-relative
        else:
            try:
                offset_val = int(label)
            except ValueError:
                raise ValueError(f"Undefined label: {label}")

        # Validate 4-bit signed offset
        if not (-8 <= offset_val <= 7):
            raise ValueError(f"Branch offset {offset_val} out of range (-8 to +7)")
        offset_bin = to_bin(offset_val, 4, signed=True)
        return opcode + s1 + s2 + offset_bin

    raise ValueError(f"Unsupported instruction: {instr}")

def first_pass(lines):
    """Collect labels and their addresses."""
    labels = {}
    pc = 0
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.endswith(':'):
            label = line[:-1].strip()
            if not label:
                raise ValueError(f"Empty label at line: {line}")
            if label in labels:
                raise ValueError(f"Duplicate label: {label}")
            labels[label] = pc
        else:
            pc += 1
    return labels

def assemble(lines):
    labels = first_pass(lines)
    machine_code = []
    pc = 0
    for line in lines:
        try:
            code = assemble_line(line, labels, pc)
        except ValueError as e:
            raise ValueError(f"Line {pc+1}: {e}")
        if code:
            if len(code) != 12:
                raise ValueError(f"Line {pc+1}: Invalid instruction length: {len(code)} bits")
            machine_code.append(code)
            pc += 1
    return machine_code

def main():
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <input.asm>")
        sys.exit(1)

    try:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{sys.argv[1]}' not found")
        sys.exit(1)

    try:
        binary = assemble(lines)
    except ValueError as e:
        print(f"Assembly failed: {e}")
        sys.exit(1)

    for instruction in binary:
        print(instruction)

if __name__ == '__main__':
    main()
