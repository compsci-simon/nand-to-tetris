
#!/usr/bin/env python3
"""
Hack Assembler - Converts Hack assembly language to machine code
Usage: python assembler.py <filename.asm>
Output: Creates <filename.hack> with binary machine code
"""

import sys
import os
from pathlib import Path
from typing import Literal



class Parser:
    
    
    def __init__(self, input_file: str):
        self.symbol_table = {
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4,
            'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15,
            'SCREEN': 0x4000,
            'KBD': 0x6000
        }
        self.current_command = None
        self.line_index = 0
        self.instruction_count = 0
        self.lines = input_file.split('\n')
        self.last_var = 16
        while self.has_more_commands():
            self.advance()
            if self.command_type() == 'L_COMMAND':
                label = self.current_command.split('//')[0].strip()
                if label[1:-1] in self.symbol_table:
                    pass
                self.symbol_table[label[1:-1]] = self.instruction_count
            elif self.command_type() == 'A_COMMAND':
                value = self.current_command.split('//')[0].strip()
                if not value[1:].isdigit() and value[1:] not in self.symbol_table:
                    self.symbol_table[value[1:]] = self.last_var
                    self.last_var += 1
        self.line_index = 0
        self.instruction_count = 0

      
    def has_more_commands(self) -> bool:
        return self.line_index < len(self.lines)
    
    def advance(self) -> None:
        self.current_command = self.lines[self.line_index]
        if self.command_type() in ['A_COMMAND', 'C_COMMAND']:
            self.instruction_count += 1
        self.line_index += 1
    
    def command_type(self) -> Literal['A_COMMAND', 'C_COMMAND', 'L_COMMAND', None]:
        command = self.current_command.split('//')[0].replace(' ', '')
        command_list = list(command)
        if len(command_list) == 0:
            return None
        if command_list[0] == '@':
            return 'A_COMMAND'
        elif command_list[0] == '(' and command_list[-1] == ')':
            return 'L_COMMAND'
        return 'C_COMMAND'
    
    def symbol(self) -> str:
        if self.command_type() == 'A_COMMAND':
            return self.symbol_table[self.current_command[1:]]
        else:
            return self.symbol_table[self.current_command[1:-1]]
    
    def dest(self) -> str:
        split_instr = self.current_command.split('//')[0].split('=')
        if len(split_instr) == 1:
            return ''
        return split_instr[0]
    
    def comp(self) -> str:
        split_instr = self.current_command.split('//')[0].split('=')
        if len(split_instr) == 1:
            return split_instr[0].split(';')[0]
        else:
            return split_instr[1].split(';')[0]
            
    
    def jump(self) -> str:
        split_instr = self.current_command.split('//')[0].split(';')
        if len(split_instr) == 1:
            return ''
        return split_instr[1]

class Code:
    def dest(mnemonic: str) -> tuple[int, int, int]:
        return {
            'null': tuple(0,0,0),
            'M': tuple(0,0,1),
            'D': tuple(0,1,0),
            'MD': tuple(0,1,1),
            'A': tuple(1,0,0),
            'AM': tuple(1,0,1),
            'AD': tuple(1,1,0),
            'AMD': tuple(1,1,1)
        }[mnemonic]

    def comp(mnemonic: str) -> tuple[int, int, int, int, int, int, int]:
        return {
            '0': tuple(0, 1, 0, 1, 0, 1, 0),
            '1': tuple(0, 1, 1, 1, 1, 1, 1),
            '-1': tuple(0, 1, 1, 1, 0, 1, 0),
            'D': tuple(0, 0, 0, 1, 1, 0, 0),
            'A': tuple(0, 1, 1, 0, 0, 0, 0),
            '!D': tuple(0, 0, 0, 1, 1, 0, 1),
            '!A': tuple(0, 1, 1, 0, 0, 0, 1),
            '-D': tuple(0, 0, 0, 1, 1, 1, 1),
            '-A': tuple(0, 1, 1, 0, 0, 1, 1),
            'D+1': tuple(0, 0, 1, 1, 1, 1, 1),
            'A+1': tuple(0, 1, 1, 0, 1, 1, 1),
            'D-1': tuple(0, 0, 0, 1, 1, 1, 0),
            'A-1': tuple(0, 1, 1, 0, 0, 1, 0),
            'D+A': tuple(0, 0, 0, 0, 0, 1, 0),
            'D-A': tuple(0, 0, 1, 0, 0, 1, 1),
            'A-D': tuple(0, 0, 0, 0, 1, 1, 1),
            'D&A': tuple(0, 0, 0, 0, 0, 0, 0),
            'D|A': tuple(0, 0, 1, 0, 1, 0, 1),
            'M': tuple(1, 1, 1, 0, 0, 0, 0),
            '!M': tuple(1, 1, 1, 0, 0, 0, 1),
            '-M': tuple(1, 1, 1, 0, 0, 1, 1),
            'M+1': tuple(1, 1, 1, 0, 1, 1, 1),
            'M-1': tuple(1, 1, 1, 0, 0, 1, 0),
            'D+M': tuple(1, 0, 0, 0, 0, 1, 0),
            'D-M': tuple(1, 0, 1, 0, 0, 1, 1),
            'M-D': tuple(1, 0, 0, 0, 1, 1, 1),
            'D&M': tuple(1, 0, 0, 0, 0, 0, 0),
            'D|M': tuple(1, 0, 1, 0, 1, 0, 1),
        }[mnemonic]

    def jump(mnemonic: str) -> tuple[int, int, int]:
        return {
            'null': tuple(0,0,0),
            'JGT': tuple(0,0,1),
            'JEQ': tuple(0,1,0),
            'JGE': tuple(0,1,1),
            'JLT': tuple(1,0,0),
            'JNE': tuple(1,0,1),
            'JLE': tuple(1,1,0),
            'JMP': tuple(1,1,1),
        }[mnemonic]

class Assembler:
    

    def assemble_file(self, input_file: str) -> str:
        """Assembles the given .asm file into a .hack file"""
        parser = Parser(input_file)
        output_binary = ""
        while parser.has_more_commands():
            parser.advance()
            c_type = parser.command_type()
            if c_type == 'A_COMMAND':
                pass
            elif c_type == 'C_COMMAND':
                pass
            elif c_type == 'L_COMMAND':
                pass
            else:
                raise Exception(f"We should not get a type of {c_type}")
        
    def get_output_filename(self, input_filename: str):
        """Generates the output filename by replacing .asm extension with .hack"""
        path = Path(input_filename)
        if path.suffix == '.asm':
            return str(path.with_suffix('.hack'))
        else:
            raise Exception("Input file must have .asm extension")
                
                    


def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <filename.asm>")
        print("Example: python assembler.py Add.asm")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' does not exist")
        sys.exit(1)
    
    # Check if file has .asm extension
    if not input_file.endswith('.asm'):
        print("Warning: Input file should have .asm extension")
    
    # Create assembler and process file
    assembler = Assembler()
    assembler.assemble_file(input_file)


if __name__ == "__main__":
    main()