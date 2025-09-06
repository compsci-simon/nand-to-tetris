
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
  return or16(and16(expand_1_to_16(not_(sel)), a), and16(expand_1_to_16(sel), b))

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
  r1 = full_adder(a[0], b[0], r2[1])
  return [
    r1[0], r2[0], r3[0], r4[0], r5[0], r6[0], r7[0],
    r8[0], r9[0], r10[0], r11[0], r12[0], r13[0], r14[0], r15[0], r16[0]
  ]

def inc16(a: int) -> int:
  return add16(a, int_to_stream16(1))

def ALU(x: list[int], y: list[int], zx: int, nx: int, zy: int, ny: int, f: int, no: int) -> tuple[list[int], int, int]:
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
  # Step 1: Handle zx (zero x)
  if zx:
    ox = [0] * 16
  else:
    ox = x[:]
  
  # Step 2: Handle nx (negate x)
  if nx:
    ox = not16(ox)
  
  # Step 3: Handle zy (zero y)
  if zy:
    oy = [0] * 16
  else:
    oy = y[:]
  
  # Step 4: Handle ny (negate y)
  if ny:
    oy = not16(oy)
  
  # Step 5: Handle f (function select)
  if f:
    # f=1: addition
    out = add16(ox, oy)
  else:
    # f=0: bitwise AND
    out = and16(ox, oy)
  
  # Step 6: Handle no (negate output)
  if no:
    out = not16(out)
  
  # Step 7: Calculate status flags
  zr = iszero16(out)  # zr=1 if out is zero
  ng = out[0]         # ng=1 if out is negative (MSB=1 in 2's complement)
  
  return (out, zr, ng)

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

  def update(self, in_, load) -> int:
    if load == 1:
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
    self.b8 = DFF()
    self.b9 = DFF()
    self.b10 = DFF()
    self.b11 = DFF()
    self.b12 = DFF()
    self.b13 = DFF()
    self.b14 = DFF()
    self.b15 = DFF()
 
  def update(self, in_: list[int], load: int):
    # Only update if load is enabled
    return self.b0.update(in_[0], load),\
      self.b1.update(in_[1], load),\
      self.b2.update(in_[2], load),\
      self.b3.update(in_[3], load),\
      self.b4.update(in_[4], load),\
      self.b5.update(in_[5], load),\
      self.b6.update(in_[6], load),\
      self.b7.update(in_[7], load),\
      self.b8.update(in_[8], load),\
      self.b9.update(in_[9], load),\
      self.b10.update(in_[10], load),\
      self.b11.update(in_[11], load),\
      self.b12.update(in_[12], load),\
      self.b13.update(in_[13], load),\
      self.b14.update(in_[14], load),\
      self.b15.update(in_[15], load)

class RAM8:
  def __init__(self):
    self.register0 = Register()
    self.register1 = Register()
    self.register2 = Register()
    self.register3 = Register()
    self.register4 = Register()
    self.register5 = Register()
    self.register6 = Register()
    self.register7 = Register()
  
  def update(self, in_: list[int], address: list[int], load: int) -> list[int]:
    # Use last 3 bits of address to select register (0-7)
    addr_bits = address[-3:]  # Get last 3 bits
    
    # Decode address to select which register to enable
    sel0 = and_(and_(not_(addr_bits[0]), not_(addr_bits[1])), not_(addr_bits[2]))  # 000
    sel1 = and_(and_(not_(addr_bits[0]), not_(addr_bits[1])), addr_bits[2])        # 001
    sel2 = and_(and_(not_(addr_bits[0]), addr_bits[1]), not_(addr_bits[2]))        # 010
    sel3 = and_(and_(not_(addr_bits[0]), addr_bits[1]), addr_bits[2])              # 011
    sel4 = and_(and_(addr_bits[0], not_(addr_bits[1])), not_(addr_bits[2]))        # 100
    sel5 = and_(and_(addr_bits[0], not_(addr_bits[1])), addr_bits[2])              # 101
    sel6 = and_(and_(addr_bits[0], addr_bits[1]), not_(addr_bits[2]))              # 110
    sel7 = and_(and_(addr_bits[0], addr_bits[1]), addr_bits[2])                    # 111
    
    # Update each register with load signal only if selected
    out0 = self.register0.update(in_, and_(sel0, load))
    out1 = self.register1.update(in_, and_(sel1, load))
    out2 = self.register2.update(in_, and_(sel2, load))
    out3 = self.register3.update(in_, and_(sel3, load))
    out4 = self.register4.update(in_, and_(sel4, load))
    out5 = self.register5.update(in_, and_(sel5, load))
    out6 = self.register6.update(in_, and_(sel6, load))
    out7 = self.register7.update(in_, and_(sel7, load))
    
    # Convert tuples to lists for the mux operations
    out0_list = list(out0)
    out1_list = list(out1)
    out2_list = list(out2)
    out3_list = list(out3)
    out4_list = list(out4)
    out5_list = list(out5)
    out6_list = list(out6)
    out7_list = list(out7)
    
    # Mux the outputs based on address
    temp1 = mux16(out0_list, out1_list, addr_bits[2])
    temp2 = mux16(out2_list, out3_list, addr_bits[2])
    temp3 = mux16(out4_list, out5_list, addr_bits[2])
    temp4 = mux16(out6_list, out7_list, addr_bits[2])
    temp5 = mux16(temp1, temp2, addr_bits[1])
    temp6 = mux16(temp3, temp4, addr_bits[1])
    
    return mux16(temp5, temp6, addr_bits[0])

class RAM64:
  def __init__(self):
    self.ram8_0 = RAM8()
    self.ram8_1 = RAM8()
    self.ram8_2 = RAM8()
    self.ram8_3 = RAM8()
    self.ram8_4 = RAM8()
    self.ram8_5 = RAM8()
    self.ram8_6 = RAM8()
    self.ram8_7 = RAM8()
  
  def update(self, in_: list[int], address: list[int], load: int) -> list[int]:
    # Use bits [5:3] to select which RAM8 unit (0-7)
    # Use bits [2:0] to select register within that RAM8 unit
    ram8_select_bits = address[-6:-3]  # Bits 5,4,3 select RAM8 unit
    
    # Decode which RAM8 to enable
    sel0 = and_(and_(not_(ram8_select_bits[0]), not_(ram8_select_bits[1])), not_(ram8_select_bits[2]))  # 000
    sel1 = and_(and_(not_(ram8_select_bits[0]), not_(ram8_select_bits[1])), ram8_select_bits[2])        # 001
    sel2 = and_(and_(not_(ram8_select_bits[0]), ram8_select_bits[1]), not_(ram8_select_bits[2]))        # 010
    sel3 = and_(and_(not_(ram8_select_bits[0]), ram8_select_bits[1]), ram8_select_bits[2])              # 011
    sel4 = and_(and_(ram8_select_bits[0], not_(ram8_select_bits[1])), not_(ram8_select_bits[2]))        # 100
    sel5 = and_(and_(ram8_select_bits[0], not_(ram8_select_bits[1])), ram8_select_bits[2])              # 101
    sel6 = and_(and_(ram8_select_bits[0], ram8_select_bits[1]), not_(ram8_select_bits[2]))              # 110
    sel7 = and_(and_(ram8_select_bits[0], ram8_select_bits[1]), ram8_select_bits[2])                    # 111
    
    # Update each RAM8 with load signal only if selected
    out0 = self.ram8_0.update(in_, address, and_(sel0, load))
    out1 = self.ram8_1.update(in_, address, and_(sel1, load))
    out2 = self.ram8_2.update(in_, address, and_(sel2, load))
    out3 = self.ram8_3.update(in_, address, and_(sel3, load))
    out4 = self.ram8_4.update(in_, address, and_(sel4, load))
    out5 = self.ram8_5.update(in_, address, and_(sel5, load))
    out6 = self.ram8_6.update(in_, address, and_(sel6, load))
    out7 = self.ram8_7.update(in_, address, and_(sel7, load))
    
    # Mux the outputs based on RAM8 selection bits
    temp1 = mux16(out0, out1, ram8_select_bits[2])
    temp2 = mux16(out2, out3, ram8_select_bits[2])
    temp3 = mux16(out4, out5, ram8_select_bits[2])
    temp4 = mux16(out6, out7, ram8_select_bits[2])
    
    temp5 = mux16(temp1, temp2, ram8_select_bits[1])
    temp6 = mux16(temp3, temp4, ram8_select_bits[1])
    
    return mux16(temp5, temp6, ram8_select_bits[0])

class RAM512:
  def __init__(self):
    self.ram64_0 = RAM64()
    self.ram64_1 = RAM64()
    self.ram64_2 = RAM64()
    self.ram64_3 = RAM64()
    self.ram64_4 = RAM64()
    self.ram64_5 = RAM64()
    self.ram64_6 = RAM64()
    self.ram64_7 = RAM64()
  
  def update(self, in_: list[int], address: list[int], load: int) -> list[int]:
    # Use bits [8:6] to select which RAM64 unit (0-7)
    # Use bits [5:0] to select location within that RAM64 unit
    ram64_select_bits = address[-9:-6]  # Bits 8,7,6 select RAM64 unit
    
    # Decode which RAM64 to enable
    sel0 = and_(and_(not_(ram64_select_bits[0]), not_(ram64_select_bits[1])), not_(ram64_select_bits[2]))  # 000
    sel1 = and_(and_(not_(ram64_select_bits[0]), not_(ram64_select_bits[1])), ram64_select_bits[2])        # 001
    sel2 = and_(and_(not_(ram64_select_bits[0]), ram64_select_bits[1]), not_(ram64_select_bits[2]))        # 010
    sel3 = and_(and_(not_(ram64_select_bits[0]), ram64_select_bits[1]), ram64_select_bits[2])              # 011
    sel4 = and_(and_(ram64_select_bits[0], not_(ram64_select_bits[1])), not_(ram64_select_bits[2]))        # 100
    sel5 = and_(and_(ram64_select_bits[0], not_(ram64_select_bits[1])), ram64_select_bits[2])              # 101
    sel6 = and_(and_(ram64_select_bits[0], ram64_select_bits[1]), not_(ram64_select_bits[2]))              # 110
    sel7 = and_(and_(ram64_select_bits[0], ram64_select_bits[1]), ram64_select_bits[2])                    # 111
    
    # Update each RAM64 with load signal only if selected
    out0 = self.ram64_0.update(in_, address, and_(sel0, load))
    out1 = self.ram64_1.update(in_, address, and_(sel1, load))
    out2 = self.ram64_2.update(in_, address, and_(sel2, load))
    out3 = self.ram64_3.update(in_, address, and_(sel3, load))
    out4 = self.ram64_4.update(in_, address, and_(sel4, load))
    out5 = self.ram64_5.update(in_, address, and_(sel5, load))
    out6 = self.ram64_6.update(in_, address, and_(sel6, load))
    out7 = self.ram64_7.update(in_, address, and_(sel7, load))
    
    # Mux the outputs based on RAM64 selection bits
    temp1 = mux16(out0, out1, ram64_select_bits[2])
    temp2 = mux16(out2, out3, ram64_select_bits[2])
    temp3 = mux16(out4, out5, ram64_select_bits[2])
    temp4 = mux16(out6, out7, ram64_select_bits[2])
    
    temp5 = mux16(temp1, temp2, ram64_select_bits[1])
    temp6 = mux16(temp3, temp4, ram64_select_bits[1])
    
    return mux16(temp5, temp6, ram64_select_bits[0])

class RAM4K:
  def __init__(self):
    self.ram512_0 = RAM512()
    self.ram512_1 = RAM512()
    self.ram512_2 = RAM512()
    self.ram512_3 = RAM512()
    self.ram512_4 = RAM512()
    self.ram512_5 = RAM512()
    self.ram512_6 = RAM512()
    self.ram512_7 = RAM512()
  
  def update(self, in_: list[int], address: list[int], load: int) -> list[int]:
    # Use bits [11:9] to select which RAM512 unit (0-7)
    # Use bits [8:0] to select location within that RAM512 unit
    ram512_select_bits = address[-12:-9]  # Bits 11,10,9 select RAM512 unit
    
    # Decode which RAM512 to enable
    sel0 = and_(and_(not_(ram512_select_bits[0]), not_(ram512_select_bits[1])), not_(ram512_select_bits[2]))  # 000
    sel1 = and_(and_(not_(ram512_select_bits[0]), not_(ram512_select_bits[1])), ram512_select_bits[2])        # 001
    sel2 = and_(and_(not_(ram512_select_bits[0]), ram512_select_bits[1]), not_(ram512_select_bits[2]))        # 010
    sel3 = and_(and_(not_(ram512_select_bits[0]), ram512_select_bits[1]), ram512_select_bits[2])              # 011
    sel4 = and_(and_(ram512_select_bits[0], not_(ram512_select_bits[1])), not_(ram512_select_bits[2]))        # 100
    sel5 = and_(and_(ram512_select_bits[0], not_(ram512_select_bits[1])), ram512_select_bits[2])              # 101
    sel6 = and_(and_(ram512_select_bits[0], ram512_select_bits[1]), not_(ram512_select_bits[2]))              # 110
    sel7 = and_(and_(ram512_select_bits[0], ram512_select_bits[1]), ram512_select_bits[2])                    # 111
    
    # Update each RAM512 with load signal only if selected
    out0 = self.ram512_0.update(in_, address, and_(sel0, load))
    out1 = self.ram512_1.update(in_, address, and_(sel1, load))
    out2 = self.ram512_2.update(in_, address, and_(sel2, load))
    out3 = self.ram512_3.update(in_, address, and_(sel3, load))
    out4 = self.ram512_4.update(in_, address, and_(sel4, load))
    out5 = self.ram512_5.update(in_, address, and_(sel5, load))
    out6 = self.ram512_6.update(in_, address, and_(sel6, load))
    out7 = self.ram512_7.update(in_, address, and_(sel7, load))
    
    # Mux the outputs based on RAM512 selection bits
    temp1 = mux16(out0, out1, ram512_select_bits[2])
    temp2 = mux16(out2, out3, ram512_select_bits[2])
    temp3 = mux16(out4, out5, ram512_select_bits[2])
    temp4 = mux16(out6, out7, ram512_select_bits[2])
    
    temp5 = mux16(temp1, temp2, ram512_select_bits[1])
    temp6 = mux16(temp3, temp4, ram512_select_bits[1])
    
    return mux16(temp5, temp6, ram512_select_bits[0])

class RAM16K:
  def __init__(self):
    self.ram4k_0 = RAM4K()
    self.ram4k_1 = RAM4K()
    self.ram4k_2 = RAM4K()
    self.ram4k_3 = RAM4K()
  
  def update(self, in_: list[int], address: list[int], load: int) -> list[int]:
    # Use bits [13:12] to select which RAM4K unit (0-3)
    # Use bits [11:0] to select location within that RAM4K unit
    ram4k_select_bits = address[-14:-12]  # Bits 13,12 select RAM4K unit
    
    # Decode which RAM4K to enable (only need 2 bits for 4 units)
    sel0 = and_(not_(ram4k_select_bits[0]), not_(ram4k_select_bits[1]))  # 00
    sel1 = and_(not_(ram4k_select_bits[0]), ram4k_select_bits[1])        # 01
    sel2 = and_(ram4k_select_bits[0], not_(ram4k_select_bits[1]))        # 10
    sel3 = and_(ram4k_select_bits[0], ram4k_select_bits[1])              # 11
    
    # Update each RAM4K with load signal only if selected
    out0 = self.ram4k_0.update(in_, address, and_(sel0, load))
    out1 = self.ram4k_1.update(in_, address, and_(sel1, load))
    out2 = self.ram4k_2.update(in_, address, and_(sel2, load))
    out3 = self.ram4k_3.update(in_, address, and_(sel3, load))
    
    # Mux the outputs based on RAM4K selection bits
    temp1 = mux16(out0, out1, ram4k_select_bits[1])
    temp2 = mux16(out2, out3, ram4k_select_bits[1])
    
    return mux16(temp1, temp2, ram4k_select_bits[0])

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
    self.regA = Register()
    self.regD = Register()
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
      self.chip = RAM16K()

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


class ROM16K:
  def __init__(self):
    self.chip = RAM16K()
  
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
    self.rom = ROM16K()
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
      for line in f.read().split('\n'):
        self.rom.write(list(map(lambda x: int(x), list(line))), int_to_stream16(addr))
        addr += 1

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

