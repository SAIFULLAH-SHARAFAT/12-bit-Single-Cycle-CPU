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
# Architecture Design

**Logisim Simulator**  
The Logisim circuit design file **`ISA_12_Bit.circ`** is included in the root folder.  
Use _Logisim 3.8.0_ to open, simulate, and modify the CPU. (Fully my design)

---
## Design Overview

Our CPU instruction word is **12 bits** wide, divided as follows:

| Bits   | Field            | Size (bits) |
|--------|------------------|-------------|
| 11 - 8 | Opcode           | 4           |
| 7 - 4  | Source/Base Reg  | 4           |
| 3 - 0  | Destination Reg  | 4           |

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

## Instruction Set Architecture (16 Instructions)

| Opcode (4 bits) | Instruction | Syntax                     | Operation                              | Encoding (12 bits)                  |
|-----------------|-------------|----------------------------|--------------------------------------|-----------------------------------|
| 0000            | add         | `add $d, $s`               | `$d = $d + $s`                       | `0000 | d(4) | s(4) | 0000`        |
| 0001            | addi        | `addi $d, imm`             | `$d = $d + imm`                      | `0001 | d(4) | imm(4) | ----`       |
| 0010            | sub         | `sub $d, $s`               | `$d = $d - $s`                       | `0010 | d(4) | s(4) | 0000`        |
| 0011            | subi        | `subi $d, imm`             | `$d = $d - imm`                      | `0011 | d(4) | imm(4) | ----`       |
| 0100            | and         | `and $d, $s`               | `$d = $d & $s`                       | `0100 | d(4) | s(4) | 0000`        |
| 0101            | sll         | `sll $d, imm`              | Shift `$d` left by `imm` bits        | `0101 | d(4) | imm(4) | ----`       |
| 0110            | or          | `or $d, $s`                | `$d = $d | $s`                       | `0110 | d(4) | s(4) | 0000`        |
| 0111            | xor         | `xor $d, $s`               | `$d = $d ^ $s`                       | `0111 | d(4) | s(4) | 0000`        |
| 1000            | nand        | `nand $d, $s`              | `$d = !($d & $s)`                    | `1000 | d(4) | s(4) | 0000`        |
| 1001            | lw          | `lw $d, imm`               | `$d = mem[imm]`                      | `1001 | d(4) | imm(8)`             |
| 1010            | sw          | `sw $s, imm`               | `mem[imm] = $s`                      | `1010 | s(4) | imm(8)`             |
| 1011            | beq         | `beq $s1, $s2, offset`     | If `$s1 == $s2`, branch PC + offset  | `1011 | s1(4) | s2(4) | offset(4)`|
| 1100            | bne         | `bne $s1, $s2, offset`     | If `$s1 != $s2`, branch PC + offset  | `1100 | s1(4) | s2(4) | offset(4)`|
| 1101            | slt         | `slt $d, $s`               | `$d = 1` if `$d < $s`, else 0       | `1101 | d(4) | s(4) | 0000`        |
| 1110            | slti        | `slti $d, imm`             | `$d = 1` if `$d < imm`, else 0      | `1110 | d(4) | imm(4) | ----`       |
| 1111            | j           | `j target`                 | Jump to absolute address `target`    | `1111 | target(8) | ----`          |

---

## Instruction Formats

| Format  | Field Breakdown                         | Bit Width (bits) |
|---------|---------------------------------------|------------------|
| **R-Type** | Opcode (11-8) | Destination (7-4) | Source (3-0)     | 4 | 4 | 4            |
| **I-Type** | Opcode (11-8) | Destination (7-4) | Immediate (3-0)  | 4 | 4 | 4            |
| **J-Type** | Opcode (11-8) | Target Address (7-0)               | 4 | 8            |

---

## Register File

| Register | Name      | Binary | Description          |
|----------|-----------|--------|----------------------|
| 0        | `$zero`   | 0000   | Hardwired zero       |
| 1–7      | `$s0–$s6` | 0001–0111 | Saved registers    |
| 8–15     | `$t0–$t7` | 1000–1111 | Temporary registers |

---

## Addressing Modes

- **Register Addressing:**  
  Example: `add $s1, $s2`  
  Operation: `$s1 = $s1 + $s2`

- **Immediate Addressing:**  
  Example: `addi $s4, 11`  
  Operation: `$s4 = $s4 + 11`

- **Base Addressing:**  
  Example: `lw $s0, $t1, 12`    
  Operation: `$s0 = mem[$t1 + 12]
---


## Program of simple Arithmetic  
add $s0, $s1       # $s0 = $s0 + $s1  

## Logical Operation  
and $s0, $s1       # $s0 = $s0 & $s1  

## Condition Check  
addi $t0, 10       # $t0 = $t0 + 10 (uses immediate addressing)  
beq $s2, $t0, L    # If $s2 == $t0, branch to L (offset must be 4-bit)  
addi $s2, -4       # Else, $s2 = $s2 - 4  
j Exit             # Jump to Exit (absolute address)  

L: addi $s2, 4     # $s2 = $s2 + 4  
Exit:  

## Loop example with 4-bit branch offset limitation  
sub $s2, $s2          # i = 0  

L1: slti $t0, $s2, 5   # $t0 = 1 if i < 5  
    beq $t0, $zero, Exit  # If $t0 == 0, branch to Exit (offset = -2)  
    addi $s0, $s0, 4      # a += 4  
    addi $s2, $s2, 1      # i++  
    j L1                  # Jump to L1 (absolute address)  

Exit:  



