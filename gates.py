from ctypes import c_int16

def nand(a: int, b: int) -> int:
  return 0 if (a and b) else 1

def not_(a: int) -> int:
  return nand(a, a)

def and_(a: int, b: int) -> int:
  return not_(nand(a, b))

def and3_to_1(a: list[int]) -> int:
  return and_(a[0], and_(a[1], a[2]))

def or3_to_1(a: list[int]) -> int:
  return or_(a[0], or_(a[1], a[2]))

def expand_1_to_16(a: int) -> list[int]:
  return [a for _ in range(16)]

def and3(a: list[int], b: list[int]) -> list[int]:
  return [
    and_(a[0], b[0]),
    and_(a[1], b[1]),
    and_(a[2], b[2])
  ]

def and8(a: list[int], b: list[int]) -> list[int]:
  return [
    and_(a[0], b[0]), and_(a[1], b[1]), and_(a[2], b[2]), and_(a[3], b[3]),
    and_(a[4], b[4]), and_(a[5], b[5]), and_(a[6], b[6]), and_(a[7], b[7]),
    and_(a[8], b[8])
  ]

def and16(a: list[int], b: list[int]):
  return [
    and_(a[0], b[0]), and_(a[1], b[1]), and_(a[2], b[2]), and_(a[3], b[3]),
    and_(a[4], b[4]), and_(a[5], b[5]), and_(a[6], b[6]), and_(a[7], b[7]),
    and_(a[8], b[8]), and_(a[9], b[9]), and_(a[10], b[10]), and_(a[11], b[11]),
    and_(a[12], b[12]), and_(a[13], b[13]), and_(a[14], b[14]), and_(a[15], b[15])
  ]

def or16(a: list[int], b: list[int]):
  return [
    or_(a[0], b[0]), or_(a[1], b[1]), or_(a[2], b[2]), or_(a[3], b[3]),
    or_(a[4], b[4]), or_(a[5], b[5]), or_(a[6], b[6]), or_(a[7], b[7]),
    or_(a[8], b[8]), or_(a[9], b[9]), or_(a[10], b[10]), or_(a[11], b[11]),
    or_(a[12], b[12]), or_(a[13], b[13]), or_(a[14], b[14]), or_(a[15], b[15])
  ]

def not16(a: list[int]):
  return [
    not_(a[0]), not_(a[1]), not_(a[2]), not_(a[3]),
    not_(a[4]), not_(a[5]), not_(a[6]), not_(a[7]),
    not_(a[8]), not_(a[9]), not_(a[10]), not_(a[11]),
    not_(a[12]), not_(a[13]), not_(a[14]), not_(a[15])
  ]

def or_(a: int, b: int) -> int:
  return nand(not_(a), not_(b))

def xor(a: int, b: int) -> int:
  return and_(nand(a, b), or_(a, b))

def mux(a: int, b: int, sel: int) -> int:
  return or_(and_(a, not_(sel)), and_(b, sel))

def mux16(a: list[int], b: list[int], sel: int) -> list[int]:
  return or16(and16(expand_1_to_16(sel), a), and16(expand_1_to_16(not_(sel)), b))

def demux(in_: int, sel: int) -> tuple[int, int]:
  return and_(not_(sel), in_), and_(sel, in_)

def half_adder(a: int, b: int) -> tuple[int, int]:
  return xor(a, b), and_(a, b)

def full_adder(a: int, b: int, c: int) -> tuple[int, int]:
  r1 = half_adder(a, b)
  r2 = half_adder(r1[0], c)
  return r2[0], or_(r1[1], r2[1])

def add16(a: list[int], b: list[int]) -> list[int]:
  r16 = full_adder(a[15], b[15], 0)
  r15 = full_adder(a[14], b[14], r16[1])
  r14 = full_adder(a[13], b[13], r15[1])
  r13 = full_adder(a[12], b[12], r14[1])
  r12 = full_adder(a[11], b[11], r13[1])
  r11 = full_adder(a[10], b[10], r12[1])
  r10 = full_adder(a[9], b[9], r11[1])
  r9 = full_adder(a[8], b[8], r10[1])
  r8 = full_adder(a[7], b[7], r9[1])
  r7 = full_adder(a[6], b[6], r8[1])
  r6 = full_adder(a[5], b[5], r7[1])
  r5 = full_adder(a[4], b[4], r6[1])
  r4 = full_adder(a[3], b[3], r5[1])
  r3 = full_adder(a[2], b[2], r4[1])
  r2 = full_adder(a[1], b[1], r3[1])
  r1 = full_adder(a[0], b[0], r2[0])
  return [
    r1[0], r2[0], r3[0], r4[0], r5[0], r6[0], r7[0],
    r8[0], r9[0], r10[0], r11[0], r12[0], r13[0], r14[0], r15[0], r16[0]
  ]

def inc16(a: int) -> int:
  return add16(a, int_to_stream16(1))

def ALU(x: list[int], y: list[int], zx: int, nx: int, zy: int, ny: int, f: int, no: int) -> tuple[int, int, int]:
  '''
  Chip name: ALU
  Inputs: x[16], y[16], // Two 16-bit data inputs
  zx, // Zero the x input
  nx, // Negate the x input
  zy, // Zero the y input
  ny, // Negate the y input
  f, // Function code: 1 for Add, 0 for And
  no // Negate the out output
  Outputs: out[16], // 16-bit output
  zr, // True iff out=0
  ng // True iff out<0
  Function: if zx then x = 0 // 16-bit zero constant
  if nx then x = !x // Bit-wise negation
  if zy then y = 0 // 16-bit zero constant
  if ny then y = !y // Bit-wise negation
  if f then out = x + y // Integer 2's complement addition
  else out = x & y // Bit-wise And
  if no then out = !out // Bit-wise negation
  if out=0 then zr = 1 else zr = 0 // 16-bit eq. comparison
  if out<0 then ng = 1 else ng = 0 // 16-bit neg. comparison
  Comment: Overflow is neither detected nor handled.
'''
  ox = or16(
    and16(x, [zx for _ in range(16)]),
    and16(not16(x), [nx for _ in range(16)])
  )
  oy = or16(
    and16(y, [zy for _ in range(16)]),
    and16(not16(y), [ny for _ in range(16)])
  )
  out = or16(
    and16(add16(ox, oy), [f for _ in range(16)]),
    and16(and16(ox, oy), [not_(f) for _ in range(16)])
  )
  new_out = and16(
    and16(out, [no for _ in range(16)]),
    and16(not16(out), [no for _ in range(16)]),
  )
  ng = new_out[15]
  zr = iszero16(new_out)
  return [new_out, zr, ng]

def iszero16(a: list[int]) -> int:
  return not_(
    or_(
      or_(
        or_(
          or_(
            or_(
              or_(
                or_(
                  or_(
                    or_(
                      or_(
                        or_(
                          or_(
                            or_(
                              or_(
                                or_(
                                  a[15],
                                  a[14]
                                ),
                                a[13]),
                              a[12]),
                            a[11]),
                          a[10]),
                        a[9]),
                      a[8]),
                    a[7]),
                  a[6]),
                a[5]),
              a[4]),
            a[3]),
          a[2]),
        a[1]),
      a[0])
    )


def iszero8(a: list[int]) -> int:
  return not_(
    or_(
      or_(
        or_(
          or_(
            or_(
              or_(
                or_(
                  or_(
                    a[8],
                    a[7]),
                a[6]),
              a[5]),
            a[4]),
          a[3]),
        a[2]),
      a[1]),
    a[0])
  )

class DFF:
  def __init__(self):
    self.out = 0

  def udpate(self, in_, clock) -> None:
    if clock == 1:
      self.out = in_
    
    return self.out


class Register:
  def __init__(self):
    self.b0 = DFF()
    self.b1 = DFF()
    self.b2 = DFF()
    self.b3 = DFF()
    self.b4 = DFF()
    self.b5 = DFF()
    self.b6 = DFF()
    self.b7 = DFF()
  
  def update(self, in_: list[int], clock: int):
    return self.b0.update(in_[0], clock),\
      self.b1.update(in_[1], clock),\
      self.b2.update(in_[2], clock),\
      self.b3.update(in_[3], clock),\
      self.b4.update(in_[4], clock),\
      self.b5.update(in_[5], clock),\
      self.b6.update(in_[6], clock),\
      self.b7.update(in_[7], clock)

class MemoryWord:
  def __init__(self):
    self.r0 = Register()
    self.r1 = Register()
    self.r2 = Register()
    self.r3 = Register()
    self.r4 = Register()
    self.r5 = Register()
    self.r6 = Register()
    self.r7 = Register()
    self.r8 = Register()
    self.r9 = Register()
    self.r10 = Register()
    self.r11 = Register()
    self.r12 = Register()
    self.r13 = Register()
    self.r14 = Register()
    self.r15 = Register()
  
  def update(self, in_: list[int], load: int):
    return self.r0.update(in_, load),\
      self.r1.update(in_, load),\
      self.r2.update(in_, load),\
      self.r3.update(in_, load),\
      self.r4.update(in_, load),\
      self.r5.update(in_, load),\
      self.r6.update(in_, load),\
      self.r7.update(in_, load),\
      self.r8.update(in_, load),\
      self.r9.update(in_, load),\
      self.r10.update(in_, load),\
      self.r11.update(in_, load),\
      self.r12.update(in_, load),\
      self.r13.update(in_, load),\
      self.r14.update(in_, load),\
      self.r15.update(in_, load)


class Chip_128:
  def __init__(self):
    self.word_0 = MemoryWord()
    self.word_1 = MemoryWord()
    self.word_2 = MemoryWord()
    self.word_3 = MemoryWord()
    self.word_4 = MemoryWord()
    self.word_5 = MemoryWord()
    self.word_6 = MemoryWord()
    self.word_7 = MemoryWord()

  def update(self, in_: list[int], address: list[int], load: int) -> list[int]:
    selector = address[-3:]
    select_0 = and3_to_1(and3(selector, int_to_stream3(0)))
    select_1 = and3_to_1(and3(selector, int_to_stream3(1)))
    select_2 = and3_to_1(and3(selector, int_to_stream3(2)))
    select_3 = and3_to_1(and3(selector, int_to_stream3(3)))
    select_4 = and3_to_1(and3(selector, int_to_stream3(4)))
    select_5 = and3_to_1(and3(selector, int_to_stream3(5)))
    select_6 = and3_to_1(and3(selector, int_to_stream3(6)))
    select_7 = and3_to_1(and3(selector, int_to_stream3(7)))
    word_0_out = self.word_0.update(in_, and_(select_0, load))
    word_1_out = self.word_0.update(in_, and_(select_1, load))
    word_2_out = self.word_0.update(in_, and_(select_2, load))
    word_3_out = self.word_0.update(in_, and_(select_3, load))
    word_4_out = self.word_0.update(in_, and_(select_4, load))
    word_5_out = self.word_0.update(in_, and_(select_5, load))
    word_6_out = self.word_0.update(in_, and_(select_6, load))
    word_7_out = self.word_0.update(in_, and_(select_7, load))
    return or16(and16(expand_1_to_16(select_0), word_0_out), or16(and16(expand_1_to_16(select_1), word_1_out), or16(and16(expand_1_to_16(select_2), word_2_out), or16(and16(expand_1_to_16(select_3), word_3_out), or16(and16(expand_1_to_16(select_4), word_4_out), or16(and16(expand_1_to_16(select_5), word_5_out), or16(and16(expand_1_to_16(select_6), word_6_out), and16(expand_1_to_16(select_7), word_7_out))))))))


class Chip_1024:
  def __init__(self):
    self.chip_0 = Chip_128()
    self.chip_1 = Chip_128()
    self.chip_2 = Chip_128()
    self.chip_3 = Chip_128()
    self.chip_4 = Chip_128()
    self.chip_5 = Chip_128()
    self.chip_6 = Chip_128()
    self.chip_7 = Chip_128()

  def update(self, in_: list[int], address: list[int], load):
    selector = address[-6:-3]
    select_0 = and3_to_1(and3(selector, int_to_stream3(0)))
    select_1 = and3_to_1(and3(selector, int_to_stream3(1)))
    select_2 = and3_to_1(and3(selector, int_to_stream3(2)))
    select_3 = and3_to_1(and3(selector, int_to_stream3(3)))
    select_4 = and3_to_1(and3(selector, int_to_stream3(4)))
    select_5 = and3_to_1(and3(selector, int_to_stream3(5)))
    select_6 = and3_to_1(and3(selector, int_to_stream3(6)))
    select_7 = and3_to_1(and3(selector, int_to_stream3(7)))
    chip_0_out = self.chip_0.update(in_, and_(select_0, load))
    chip_1_out = self.chip_0.update(in_, and_(select_1, load))
    chip_2_out = self.chip_0.update(in_, and_(select_2, load))
    chip_3_out = self.chip_0.update(in_, and_(select_3, load))
    chip_4_out = self.chip_0.update(in_, and_(select_4, load))
    chip_5_out = self.chip_0.update(in_, and_(select_5, load))
    chip_6_out = self.chip_0.update(in_, and_(select_6, load))
    chip_7_out = self.chip_0.update(in_, and_(select_7, load))
    return or16(and16(expand_1_to_16(select_0), chip_0_out), or16(and16(expand_1_to_16(select_1), chip_1_out), or16(and16(expand_1_to_16(select_2), chip_2_out), or16(and16(expand_1_to_16(select_3), chip_3_out), or16(and16(expand_1_to_16(select_4), chip_4_out), or16(and16(expand_1_to_16(select_5), chip_5_out), or16(and16(expand_1_to_16(select_6), chip_6_out), and16(expand_1_to_16(select_7), chip_7_out))))))))


class Chip_8192:
  def __init__(self):
    self.chip_0 = Chip_1024()
    self.chip_1 = Chip_1024()
    self.chip_2 = Chip_1024()
    self.chip_3 = Chip_1024()
    self.chip_4 = Chip_1024()
    self.chip_5 = Chip_1024()
    self.chip_6 = Chip_1024()
    self.chip_7 = Chip_1024()

  def update(self, in_: list[int], address: list[int], load: int) -> list[int]:
    selector = address[-9:-6]
    select_0 = and3_to_1(and3(selector, int_to_stream3(0)))
    select_1 = and3_to_1(and3(selector, int_to_stream3(1)))
    select_2 = and3_to_1(and3(selector, int_to_stream3(2)))
    select_3 = and3_to_1(and3(selector, int_to_stream3(3)))
    select_4 = and3_to_1(and3(selector, int_to_stream3(4)))
    select_5 = and3_to_1(and3(selector, int_to_stream3(5)))
    select_6 = and3_to_1(and3(selector, int_to_stream3(6)))
    select_7 = and3_to_1(and3(selector, int_to_stream3(7)))
    chip_0_out = self.chip_0.update(in_, and_(select_0, load))
    chip_1_out = self.chip_0.update(in_, and_(select_1, load))
    chip_2_out = self.chip_0.update(in_, and_(select_2, load))
    chip_3_out = self.chip_0.update(in_, and_(select_3, load))
    chip_4_out = self.chip_0.update(in_, and_(select_4, load))
    chip_5_out = self.chip_0.update(in_, and_(select_5, load))
    chip_6_out = self.chip_0.update(in_, and_(select_6, load))
    chip_7_out = self.chip_0.update(in_, and_(select_7, load))
    return or16(and16(expand_1_to_16(select_0), chip_0_out), or16(and16(expand_1_to_16(select_1), chip_1_out), or16(and16(expand_1_to_16(select_2), chip_2_out), or16(and16(expand_1_to_16(select_3), chip_3_out), or16(and16(expand_1_to_16(select_4), chip_4_out), or16(and16(expand_1_to_16(select_5), chip_5_out), or16(and16(expand_1_to_16(select_6), chip_6_out), and16(expand_1_to_16(select_7), chip_7_out))))))))
    

class Chip_32768:
  def __init__(self):
    self.chip_0 = Chip_8192()
    self.chip_1 = Chip_8192()
    self.chip_2 = Chip_8192()
    self.chip_3 = Chip_8192()

  def update(self, in_: list[int], address: list[int], load: int) -> list[int]:
    selector = address[-12:-9]
    select_0 = and3_to_1(and3(selector, int_to_stream3(0)))
    select_1 = and3_to_1(and3(selector, int_to_stream3(1)))
    select_2 = and3_to_1(and3(selector, int_to_stream3(2)))
    select_3 = and3_to_1(and3(selector, int_to_stream3(3)))
    select_4 = and3_to_1(and3(selector, int_to_stream3(4)))
    select_5 = and3_to_1(and3(selector, int_to_stream3(5)))
    select_6 = and3_to_1(and3(selector, int_to_stream3(6)))
    select_7 = and3_to_1(and3(selector, int_to_stream3(7)))
    chip_0_out = self.chip_0.update(in_, and_(select_0, load))
    chip_1_out = self.chip_0.update(in_, and_(select_1, load))
    chip_2_out = self.chip_0.update(in_, and_(select_2, load))
    chip_3_out = self.chip_0.update(in_, and_(select_3, load))
    chip_4_out = self.chip_0.update(in_, and_(select_4, load))
    chip_5_out = self.chip_0.update(in_, and_(select_5, load))
    chip_6_out = self.chip_0.update(in_, and_(select_6, load))
    chip_7_out = self.chip_0.update(in_, and_(select_7, load))
    return or16(and16(expand_1_to_16(select_0), chip_0_out), or16(and16(expand_1_to_16(select_1), chip_1_out), or16(and16(expand_1_to_16(select_2), chip_2_out), or16(and16(expand_1_to_16(select_3), chip_3_out), or16(and16(expand_1_to_16(select_4), chip_4_out), or16(and16(expand_1_to_16(select_5), chip_5_out), or16(and16(expand_1_to_16(select_6), chip_6_out), and16(expand_1_to_16(select_7), chip_7_out))))))))

class PC:
  def __init__(self):
    self.count = 0
  
  def update(self, in_: list[int], inc: int, load: int, reset: int):
    temp = self.count
    if reset:
      self.count = 0
    elif load:
      self.count = in_
    elif inc:
      self.count += 1
    return temp

class CPU:
  def __init__(self):
    self.pc = PC()
    self.regA = MemoryWord()
    self.regD = MemoryWord()
    self.ALUOutput = [0 for _ in range(16)]
  
  def update(self, inM: list[int], instruction: list[int], reset: int):
    '''
    inM: 16 bit input from memory
    instruction: 16 bit input instruction
    reset: Set pc to 0 if set
    '''
    i, a, c, d, j = instruction[0], instruction[3], instruction[4:10], instruction[10:13], instruction[13:16]
    outM, writeM, addressM, pc = 0, 0, 0, 0
    mux0Out = mux16(self.ALUOutput, instruction, i)
    regAOut = self.regA.update(mux0Out, d[0])
    addressM = regAOut
    
    regDOut = self.regD.update(self.ALUOutput, d[1])
    mux1Out = mux16(regAOut, inM, i)
    
    [self.ALUOutput, zr, ng] = ALU(regDOut, mux1Out, *c)
    
    outM = self.ALUOutput
    writeM = d[2]

    inc = and_(not_(j[0]), and_(not_(j[1]), not_(j[2])))
    load = or3_to_1(and3(j, [ng, zr, not_(ng)]))
    
    pc = self.pc.update(regAOut, inc, load, reset)
    
    return outM, writeM, addressM, pc

class MemoryChip:
    def __init__(self):
      self.chip = Chip_32768()

    def update(self, in_: list[int], address: list[int], load: int) -> list[int]:
        '''
        in_: the input to store if load is set - 16 bits
        address: The address to store or read from - 15 bits
        load: whether or not to store in_ - 1 bit
        '''
        return self.chip.update(in_, address, load)

def int_to_stream3(a: int) -> list[int]:
  stream = [0 for _ in range(3)]
  for i in range(3):
    stream[2 - i] = 1 if a & 2**i > 0 else 0
  return stream


class ROM32K:
  def __init__(self):
    self.chip = Chip_32768()
  
  def update(self, address: list[int]) -> list[int]:
    '''
    address: 15 bit input address
    returns a 16 bit memory word
    '''
    return self.chip.update([0 for _ in range(16)], address, 0)
  
  def write(self, in_: list[int], address: list[int]) -> None:
    self.chip.update(in_, address, 1)
class Computer:
  def __init__(self):
    self.rom = ROM32K()
    self.mem = MemoryChip()
    self.cpu = CPU()
    
  def run(self):
    outM, writeM, addressM, pc = self.cpu.update(int_to_stream16(0), int_to_stream16(0), 1)
    inM = int_to_stream16(0)
    while True:
      instruction = self.rom.update(pc)
      outM, writeM, addressM, pc = self.cpu.update(inM, instruction, 0)
      inM = self.mem.update(outM, addressM, writeM)
  
  def load_instructions(self, filename: str):
    addr = 0
    with open(filename, 'r') as f:
      for line in f.readlines():
        self.rom.write(list(line), int_to_stream16(addr))

def int_to_stream8(a: int) -> list[int]:
  stream = [0 for _ in range(8)]
  for i in range(8):
    stream[7 - i] = 1 if a & 2**i > 0 else 0
  return stream

def int_to_stream16(a: int) -> list[int]:
  stream = [0 for _ in range(16)]
  for i in range(16):
    stream[15 - i] = 1 if a & 2**i > 0 else 0
  return stream

