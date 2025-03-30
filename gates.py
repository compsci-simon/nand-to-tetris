from ctypes import c_int16

def nand(a: int, b: int) -> int:
  return 0 if (a and b) else 1

def not_(a: int) -> int:
  return nand(a, a)

def and_(a: int, b: int) -> int:
  return not_(nand(a, b))

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
  return add16(a, int_to_stream(1))

# returns out, zr, ng
def ALU(x: list[int], y: list[int], zx: int, nx: int, zy: int, ny: int, f: int, no: int) -> tuple[int, int, int]:
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

class RAM8:
  def __init__(self):
    self.r0 = Register()
    self.r1 = Register()
    self.r2 = Register()
    self.r3 = Register()
    self.r4 = Register()
    self.r5 = Register()
    self.r6 = Register()
    self.r7 = Register()
  
  def update(self, in_: list[int], address: list[int], clock):
    return self.r0.update(in_, and3(address, int_to_stream3(0))),\
      self.r1.update(in_, and3(address, int_to_stream3(1))),\
      self.r2.update(in_, and3(address, int_to_stream3(2))),\
      self.r3.update(in_, and3(address, int_to_stream3(3))),\
      self.r4.update(in_, and3(address, int_to_stream3(4))),\
      self.r5.update(in_, and3(address, int_to_stream3(5))),\
      self.r6.update(in_, and3(address, int_to_stream3(6))),\
      self.r7.update(in_, and3(address, int_to_stream3(7)))


class RAM64:
  def __init__(self):
    self.ram_8_0 = RAM8()
    self.ram_8_1 = RAM8()
    self.ram_8_2 = RAM8()
    self.ram_8_3 = RAM8()
    self.ram_8_4 = RAM8()
    self.ram_8_5 = RAM8()
    self.ram_8_6 = RAM8()
    self.ram_8_7 = RAM8()

  def update(self, in_: list[int], address: list[int], clock):
    return self.ram_8_0.update(in_, address[-3:], and3(address[-6:-3], int_to_stream3(0))),\
      self.ram_8_1.update(in_, address[-3:], and3(address[-6:-3], int_to_stream3(1))),\
      self.ram_8_2.update(in_, address[-3:], and3(address[-6:-3], int_to_stream3(2))),\
      self.ram_8_3.update(in_, address[-3:], and3(address[-6:-3], int_to_stream3(3))),\
      self.ram_8_4.update(in_, address[-3:], and3(address[-6:-3], int_to_stream3(4))),\
      self.ram_8_5.update(in_, address[-3:], and3(address[-6:-3], int_to_stream3(5))),\
      self.ram_8_6.update(in_, address[-3:], and3(address[-6:-3], int_to_stream3(6))),\
      self.ram_8_7.update(in_, address[-3:], and3(address[-6:-3], int_to_stream3(7)))


class RAM512:
  def __init__(self):
    self.ram_64_0 = RAM64()
    self.ram_64_1 = RAM64()
    self.ram_64_2 = RAM64()
    self.ram_64_3 = RAM64()
    self.ram_64_4 = RAM64()
    self.ram_64_5 = RAM64()
    self.ram_64_6 = RAM64()
    self.ram_64_7 = RAM64()

  def update(self, in_: list[int], address: list[int], clock):
    return self.ram_64_0.update(in_, address[-6:], and3(address[-9:-6], int_to_stream3(0))),\
      self.ram_64_1.update(in_, address[-6:], and3(address[-9:-6], int_to_stream3(1))),\
      self.ram_64_2.update(in_, address[-6:], and3(address[-9:-6], int_to_stream3(2))),\
      self.ram_64_3.update(in_, address[-6:], and3(address[-9:-6], int_to_stream3(3))),\
      self.ram_64_4.update(in_, address[-6:], and3(address[-9:-6], int_to_stream3(4))),\
      self.ram_64_5.update(in_, address[-6:], and3(address[-9:-6], int_to_stream3(5))),\
      self.ram_64_6.update(in_, address[-6:], and3(address[-9:-6], int_to_stream3(6))),\
      self.ram_64_7.update(in_, address[-6:], and3(address[-9:-6], int_to_stream3(7)))


class RAM4K:
  def __init__(self):
    self.ram_512_0 = RAM512()
    self.ram_512_1 = RAM512()
    self.ram_512_2 = RAM512()
    self.ram_512_3 = RAM512()
    self.ram_512_4 = RAM512()
    self.ram_512_5 = RAM512()
    self.ram_512_6 = RAM512()
    self.ram_512_7 = RAM512()

  def update(self, in_: list[int], address: list[int], clock):
    return self.ram_64_0.update(in_, address[-9:], and3(address[:3], int_to_stream3(0))),\
      self.ram_64_1.update(in_, address[-9:], and3(address[:3], int_to_stream3(1))),\
      self.ram_64_2.update(in_, address[-9:], and3(address[:3], int_to_stream3(2))),\
      self.ram_64_3.update(in_, address[-9:], and3(address[:3], int_to_stream3(3))),\
      self.ram_64_4.update(in_, address[-9:], and3(address[:3], int_to_stream3(4))),\
      self.ram_64_5.update(in_, address[-9:], and3(address[:3], int_to_stream3(5))),\
      self.ram_64_6.update(in_, address[-9:], and3(address[:3], int_to_stream3(6))),\
      self.ram_64_7.update(in_, address[-9:], and3(address[:3], int_to_stream3(7)))


class PC:
  def __init__(self):
    count = 0
  
  def update(self, in_: list[int], inc: int, load: int, reset: int):
    temp = self.count
    if reset:
      self.count = 0
    elif load:
      self.count = in_
    elif inc:
      self.count += 1
    return temp

def int_to_stream3(a: int) -> list[int]:
  stream = [0 for _ in range(3)]
  for i in range(3):
    stream[2 - i] = 1 if a & 2**i > 0 else 0
  return stream


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

