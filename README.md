# 12-bit-Single-Cycle-CPU
This was built as a project, but I have done all the things, and it was pretty fun and an interesting project. The allocated task was given by Tnr (Dr Tanzilur Rahman)

# ISA Design - Project Milestone 01

**Course:** Computer Organization & Architecture (CSE332)  
**Faculty:** Tanzilur Rahman (Tnr)  
**Department:** Electrical and Computer Engineering (ECE)  

---

## Objective

- Design a new **12-bit single-cycle CPU** with separate Data and Instruction Memory.
- Develop an assembler to translate assembly language programs into machine code (binary) and generate an output file with machine instructions.

---

## Design Overview

Our CPU instruction word is **12 bits** wide, divided as follows:

| Bits   | Field            | Size (bits) |
|--------|------------------|-------------|
| 11 - 8 | Opcode           | 4           |
| 7 - 4  | Destination Reg  | 4           |
| 3 - 0  | Source Operand   | 4           |

---

## Operands

- We have **two individual registers** as operands.
- Each register file contains **16 registers**, each 16 bits wide.
- Operands are **register-based**:
  - Can load/store temporary or permanent values.
  - Support immediate values.
  - Access non-volatile memory.

---

## Operations and Instruction Set

- **4 bits opcode** allows for **16 instructions**.
- Instruction categories:
  - Arithmetic
  - Logical
  - Data Transfer
  - Conditional Branch
  - Unconditional Jump

| Category          | Instruction | Opcode (Binary) | Example Syntax     | Meaning/Operation                                  |
|-------------------|-------------|-----------------|--------------------|--------------------------------------------------|
| **Arithmetic**    | add         | 0000            | `add $s0, $s1`     | `$s0 = $s0 + $s1`                                |
|                   | addi        | 0001            | `addi $s0, 20`     | `$s0 = $s0 + 20`                                 |
|                   | sub         | 0010            | `sub $s0, $s1`     | `$s0 = $s0 - $s1`                                |
|                   | subi        | 0011            | `subi $s0, 5`      | `$s0 = $s0 - 5`                                  |
| **Logical**       | and         | 0100            | `and $s0, $s1`     | `$s0 = $s0 & $s1`                                |
|                   | sll         | 0101            | `sll $s0, 2`       | Shift left logical `$s0` by 2                     |
|                   | or          | 0110            | `or $s0, $s1`      | `$s0 = $s0 | $s1`                                |
|                   | xor         | 0111            | `xor $s0, $s1`     | `$s0 = $s0 ^ $s1`                                |
|                   | nand        | 1000            | `nand $s0, $s1`    | `$s0 = !($s0 & $s1)`                             |
| **Data Transfer** | lw          | 1001            | `lw $s0, 2`        | Load word: `$s0 = mem[$t0 + offset]`             |
|                   | sw          | 1010            | `sw $s0, 2`        | Store word: `mem[$t0 + offset] = $s0`            |
| **Conditional**   | beq         | 1011            | `beq $s0, 4`       | If `$s0 == $t0` then jump to address 4            |
|                   | bne         | 1100            | `bne $s0, 4`       | If `$s0 != $t0` then jump to address 4            |
|                   | slt         | 1101            | `slt $s0, $s1`     | `$t0 = 1` if `$s0 < $s1`, else `$t0 = 0`          |
|                   | slti        | 1110            | `slti $s0, 2`      | `$t0 = 1` if `$s0 < 2`, else `$t0 = 0`             |
| **Unconditional** | j           | 1111            | `j 20`             | Jump to address 20                                 |

---

## Instruction Formats

| Format  | Field Breakdown                         | Bit Width (bits) |
|---------|---------------------------------------|------------------|
| **R-Type** | Opcode (11-8) | Destination (7-4) | Source (3-0)     | 4 | 4 | 4            |
| **I-Type** | Opcode (11-8) | Destination (7-4) | Immediate (3-0)  | 4 | 4 | 4            |
| **J-Type** | Opcode (11-8) | Target Address (7-0)               | 4 | 8            |

---

## Register File

| Register Number | Register Name | Binary Code | Description             |
|-----------------|---------------|-------------|-------------------------|
| 0               | `$zero`       | 0000        | Constant zero           |
| 1 - 7           | `$s0` - `$s6` | 0001-0111   | Saved registers         |
| 8 - 15          | `$t0` - `$t7` | 1000-1111   | Temporary registers     |

---

## Addressing Modes

- **Register Addressing:**  
  Example: `add $s1, $s2`  
  Operation: `$s1 = $s1 + $s2`

- **Immediate Addressing:**  
  Example: `addi $s4, 11`  
  Operation: `$s4 = $s4 + 11`

- **Base Addressing:**  
  Example: `lw $s0, 2($s1)`  
  Operation: `$s0 = mem[$s1 + offset]`

---

## Sample Programs

### Simple Arithmetic
```asm
add $s0, $s1       # $s0 = $s0 + $s1

### Logical Operation
and $s0, $s1       # $s0 = $s0 & $s1

###Condition Check
addi $t0, 10       # $t0 = 10
beq $s2, L         # if ($s2 == $t0) jump to L
addi $s2, -4       # else $s2 = $s2 - 4
j Exit             # jump to Exit

L: addi $s2, 4     # $s2 = $s2 + 4
Exit:

###Loop
sub $s2, $s2       # initialize i = 0
sub $t0, $t0       # clear temporary register
sub $s0, $s0       # clear a

L1: slti $t0, $s2, 5     # if i < 5 then $t0=1 else 0
    beq $t0, $zero, Exit # if $t0 == 0, exit loop
    addi $s0, 4          # a = a + 4
    addi $s2, 1          # i++
    j L1                 # jump to L1

Exit:



