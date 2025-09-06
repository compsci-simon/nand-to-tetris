import unittest
from gates import (nand, not_, and_, or_, xor, mux, expand_1_to_16, and16, or16, not16, mux16, 
                   Register, RAM8, RAM64, half_adder, full_adder, add16, demux, int_to_stream3, 
                   int_to_stream16, iszero16, DFF, ALU)
import os

class TestGates(unittest.TestCase):
    def test_nand(self):
        self.assertEqual(nand(0, 0), 1)
        self.assertEqual(nand(0, 1), 1)
        self.assertEqual(nand(1, 0), 1)
        self.assertEqual(nand(1, 1), 0)

    def test_not(self):
        self.assertEqual(not_(0), 1)
        self.assertEqual(not_(1), 0)

    def test_and(self):
        self.assertEqual(and_(0, 0), 0)
        self.assertEqual(and_(0, 1), 0)
        self.assertEqual(and_(1, 0), 0)
        self.assertEqual(and_(1, 1), 1)

    def test_or(self):
        self.assertEqual(or_(0, 0), 0)
        self.assertEqual(or_(0, 1), 1)
        self.assertEqual(or_(1, 0), 1)
        self.assertEqual(or_(1, 1), 1)

    def test_xor(self):
        self.assertEqual(xor(0, 0), 0)
        self.assertEqual(xor(0, 1), 1)
        self.assertEqual(xor(1, 0), 1)
        self.assertEqual(xor(1, 1), 0)

    def test_mux(self):
        self.assertEqual(mux(0, 1, 0), 0)
        self.assertEqual(mux(0, 1, 1), 1)
        self.assertEqual(mux(1, 0, 0), 1)
        self.assertEqual(mux(1, 0, 1), 0)

    def test_expand_1_to_16(self):
        self.assertEqual(expand_1_to_16(0), [0]*16)
        self.assertEqual(expand_1_to_16(1), [1]*16)

    def test_and16(self):
        a = [1]*16
        b = [0]*16
        self.assertEqual(and16(a, b), [0]*16)
        self.assertEqual(and16(a, a), [1]*16)

    def test_or16(self):
        a = [1]*16
        b = [0]*16
        self.assertEqual(or16(a, b), [1]*16)
        self.assertEqual(or16(b, b), [0]*16)

    def test_not16(self):
        a = [1]*16
        b = [0]*16
        self.assertEqual(not16(a), [0]*16)
        self.assertEqual(not16(b), [1]*16)

    def test_mux16(self):
        a = [0]*16
        b = [1]*16
        # When sel=0, should return a (all zeros)
        self.assertEqual(mux16(a, b, 0), [0]*16)
        # When sel=1, should return b (all ones)
        self.assertEqual(mux16(a, b, 1), [1]*16)
        
        # Test with mixed values
        c = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        d = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        # When sel=0, should return c
        self.assertEqual(mux16(c, d, 0), c)
        # When sel=1, should return d
        self.assertEqual(mux16(c, d, 1), d)

class TestRegister(unittest.TestCase):
    def test_register_initialization(self):
        reg = Register()
        # Test that all 16 registers are initialized
        self.assertIsNotNone(reg.b0)
        self.assertIsNotNone(reg.b15)

    def test_register_update_no_load(self):
        reg = Register()
        test_input = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        
        # When load=0, should not store the input
        result = reg.update(test_input, 0)
        # Result should be all zeros (initial state)
        expected = tuple([0] * 16)
        self.assertEqual(result, expected)

    def test_register_update_with_load(self):
        reg = Register()
        test_input = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        
        # When load=1, should store the input
        result = reg.update(test_input, 1)
        expected = tuple(test_input)
        self.assertEqual(result, expected)


class TestArithmetic(unittest.TestCase):
    def test_half_adder(self):
        # Test all combinations
        self.assertEqual(half_adder(0, 0), (0, 0))  # sum=0, carry=0
        self.assertEqual(half_adder(0, 1), (1, 0))  # sum=1, carry=0
        self.assertEqual(half_adder(1, 0), (1, 0))  # sum=1, carry=0
        self.assertEqual(half_adder(1, 1), (0, 1))  # sum=0, carry=1
    
    def test_full_adder(self):
        # Test all combinations
        self.assertEqual(full_adder(0, 0, 0), (0, 0))  # sum=0, carry=0
        self.assertEqual(full_adder(0, 0, 1), (1, 0))  # sum=1, carry=0
        self.assertEqual(full_adder(0, 1, 0), (1, 0))  # sum=1, carry=0
        self.assertEqual(full_adder(0, 1, 1), (0, 1))  # sum=0, carry=1
        self.assertEqual(full_adder(1, 0, 0), (1, 0))  # sum=1, carry=0
        self.assertEqual(full_adder(1, 0, 1), (0, 1))  # sum=0, carry=1
        self.assertEqual(full_adder(1, 1, 0), (0, 1))  # sum=0, carry=1
        self.assertEqual(full_adder(1, 1, 1), (1, 1))  # sum=1, carry=1
    
    def test_add16_simple(self):
        # Test adding zero
        zero = [0] * 16
        one = [0] * 15 + [1]
        self.assertEqual(add16(zero, zero), zero)
        self.assertEqual(add16(zero, one), one)
        self.assertEqual(add16(one, zero), one)
        
        # Test 1 + 1 = 2
        two = [0] * 14 + [1, 0]
        self.assertEqual(add16(one, one), two)
    
    def test_add16_larger_numbers(self):
        # Test 5 + 3 = 8
        five = int_to_stream16(5)   # [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1]
        three = int_to_stream16(3)  # [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1]
        eight = int_to_stream16(8)  # [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0]
        self.assertEqual(add16(five, three), eight)


class TestUtilityFunctions(unittest.TestCase):
    def test_demux(self):
        # Test demux function
        self.assertEqual(demux(1, 0), (1, 0))  # sel=0 -> first output gets input
        self.assertEqual(demux(1, 1), (0, 1))  # sel=1 -> second output gets input
        self.assertEqual(demux(0, 0), (0, 0))  # input=0 -> both outputs are 0
        self.assertEqual(demux(0, 1), (0, 0))  # input=0 -> both outputs are 0
    
    def test_iszero16(self):
        zero = [0] * 16
        not_zero1 = [0] * 15 + [1]
        not_zero2 = [1] + [0] * 15
        mixed = [1, 0, 1, 0] * 4
        
        self.assertEqual(iszero16(zero), 1)
        self.assertEqual(iszero16(not_zero1), 0)
        self.assertEqual(iszero16(not_zero2), 0)
        self.assertEqual(iszero16(mixed), 0)
    
    def test_int_to_stream3(self):
        self.assertEqual(int_to_stream3(0), [0, 0, 0])
        self.assertEqual(int_to_stream3(1), [0, 0, 1])
        self.assertEqual(int_to_stream3(2), [0, 1, 0])
        self.assertEqual(int_to_stream3(3), [0, 1, 1])
        self.assertEqual(int_to_stream3(4), [1, 0, 0])
        self.assertEqual(int_to_stream3(5), [1, 0, 1])
        self.assertEqual(int_to_stream3(6), [1, 1, 0])
        self.assertEqual(int_to_stream3(7), [1, 1, 1])
    
    def test_int_to_stream16(self):
        # Test some basic values
        self.assertEqual(int_to_stream16(0), [0] * 16)
        self.assertEqual(int_to_stream16(1), [0] * 15 + [1])
        self.assertEqual(int_to_stream16(2), [0] * 14 + [1, 0])
        self.assertEqual(int_to_stream16(4), [0] * 13 + [1, 0, 0])
        
        # Test max 16-bit value (65535 = 2^16 - 1)
        max_16_bit = [1] * 16
        self.assertEqual(int_to_stream16(65535), max_16_bit)


class TestDFF(unittest.TestCase):
    def test_dff_initialization(self):
        dff = DFF()
        self.assertEqual(dff.out, 0)
    
    def test_dff_no_load(self):
        dff = DFF()
        result = dff.update(1, 0)  # input=1, load=0
        self.assertEqual(result, 0)  # Should remain 0
        self.assertEqual(dff.out, 0)
    
    def test_dff_with_load(self):
        dff = DFF()
        result = dff.update(1, 1)  # input=1, load=1
        self.assertEqual(result, 1)  # Should store 1
        self.assertEqual(dff.out, 1)
        
        # Test it holds the value
        result = dff.update(0, 0)  # input=0, load=0
        self.assertEqual(result, 1)  # Should still be 1


class TestRAM8(unittest.TestCase):
    def test_ram8_initialization(self):
        ram = RAM8()
        self.assertIsNotNone(ram.register0)
        self.assertIsNotNone(ram.register7)
    
    def test_ram8_store_and_read(self):
        ram = RAM8()
        test_data = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        
        # Store data at address 0 (000)
        address_0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        result = ram.update(test_data, address_0, 1)  # load=1
        self.assertEqual(list(result), test_data)
        
        # Read from address 0 (should return stored data)
        result = ram.update([0]*16, address_0, 0)  # load=0
        self.assertEqual(list(result), test_data)
        
        # Store different data at address 1 (001)
        address_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        different_data = [0, 1, 0, 1] * 4
        result = ram.update(different_data, address_1, 1)  # load=1
        self.assertEqual(list(result), different_data)
        
        # Verify address 0 still has original data
        result = ram.update([0]*16, address_0, 0)  # load=0
        self.assertEqual(list(result), test_data)


class TestRAM64(unittest.TestCase):
    def test_ram64_initialization(self):
        ram = RAM64()
        self.assertIsNotNone(ram.ram8_0)
        self.assertIsNotNone(ram.ram8_7)
    
    def test_ram64_address_decoding(self):
        ram = RAM64()
        test_data = [1] * 16
        
        # Test address 0 (000000)
        address_0 = [0] * 16
        result = ram.update(test_data, address_0, 1)
        self.assertEqual(result, test_data)
        
        # Test address 7 (000111) - last register in first RAM8
        address_7 = [0] * 13 + [1, 1, 1]
        result = ram.update(test_data, address_7, 1)
        self.assertEqual(result, test_data)
        
        # Test address 8 (001000) - first register in second RAM8  
        address_8 = [0] * 12 + [1, 0, 0, 0]
        result = ram.update(test_data, address_8, 1)
        self.assertEqual(result, test_data)


class TestALU(unittest.TestCase):
    def test_alu_zero_x(self):
        x = [1] * 16
        y = [0, 1] * 8
        # zx=1, nx=0, zy=0, ny=0, f=0, no=0 -> should zero x and do x&y
        result = ALU(x, y, 1, 0, 0, 0, 0, 0)
        expected_out = [0] * 16  # 0 & y = 0
        self.assertEqual(result[0], expected_out)
        self.assertEqual(result[1], 1)  # zr should be 1 (result is zero)
        self.assertEqual(result[2], 0)  # ng should be 0 (result not negative)
    
    def test_alu_add(self):
        x = int_to_stream16(5)
        y = int_to_stream16(3)
        # zx=0, nx=0, zy=0, ny=0, f=1, no=0 -> should do x+y
        result = ALU(x, y, 0, 0, 0, 0, 1, 0)
        expected_out = int_to_stream16(8)
        self.assertEqual(result[0], expected_out)
        self.assertEqual(result[1], 0)  # zr should be 0 (result not zero)
        self.assertEqual(result[2], 0)  # ng should be 0 (result not negative)
    
    def test_alu_and_operation(self):
        x = int_to_stream16(12)  # 1100 in binary
        y = int_to_stream16(10)  # 1010 in binary
        # zx=0, nx=0, zy=0, ny=0, f=0, no=0 -> should do x&y
        result = ALU(x, y, 0, 0, 0, 0, 0, 0)
        expected_out = int_to_stream16(8)  # 1000 in binary = 8
        self.assertEqual(result[0], expected_out)
        self.assertEqual(result[1], 0)  # zr should be 0 (result not zero)
        self.assertEqual(result[2], 0)  # ng should be 0 (result not negative)
    
    def test_alu_negate_x(self):
        x = int_to_stream16(5)
        y = int_to_stream16(0)
        # zx=0, nx=1, zy=1, ny=0, f=0, no=0 -> should do (!x) & 0 = 0
        result = ALU(x, y, 0, 1, 1, 0, 0, 0)
        expected_out = [0] * 16
        self.assertEqual(result[0], expected_out)
        self.assertEqual(result[1], 1)  # zr should be 1 (result is zero)
        self.assertEqual(result[2], 0)  # ng should be 0 (result not negative)
    
    def test_alu_negate_output(self):
        x = int_to_stream16(0)
        y = int_to_stream16(0)
        # zx=0, nx=0, zy=0, ny=0, f=0, no=1 -> should do !(x&y) = !0 = all 1s
        result = ALU(x, y, 0, 0, 0, 0, 0, 1)
        expected_out = [1] * 16  # All 1s (represents -1 in 2's complement)
        self.assertEqual(result[0], expected_out)
        self.assertEqual(result[1], 0)  # zr should be 0 (result not zero)
        self.assertEqual(result[2], 1)  # ng should be 1 (result is negative)
    
    def test_alu_subtract_y_from_x(self):
        # The ALU can compute x + (!y) which gives x - y - 1
        # To get true x - y, we would need x + (!y + 1), but ALU can't add the +1
        x = int_to_stream16(10)
        y = int_to_stream16(3)
        # zx=0, nx=0, zy=0, ny=1, f=1, no=0 -> should do x + (!y)
        result = ALU(x, y, 0, 0, 0, 1, 1, 0)
        
        # x + (!y) = 10 + (!3) = 10 + (65535-3) = 10 + 65532 = 65542
        # In 16-bit: 65542 = 6 (with overflow), so result should be 6
        expected_out = int_to_stream16(6)  # 10 - 3 - 1 = 6
        self.assertEqual(result[0], expected_out)
        self.assertEqual(result[1], 0)  # Should not be zero
        self.assertEqual(result[2], 0)  # Should not be negative
    
    def test_alu_compute_x_minus_1(self):
        # To compute x - 1, we can use: zx=0, nx=0, zy=1, ny=1, f=1, no=0
        # This gives x + (!0) = x + (-1) = x - 1
        x = int_to_stream16(5)
        y = int_to_stream16(0)  # y value doesn't matter since zy=1
        result = ALU(x, y, 0, 0, 1, 1, 1, 0)
        
        expected_out = int_to_stream16(4)  # 5 - 1 = 4
        self.assertEqual(result[0], expected_out)
        self.assertEqual(result[1], 0)  # Should not be zero
        self.assertEqual(result[2], 0)  # Should not be negative
    
    def test_alu_compute_negative_x(self):
        # To compute -x, we can use: zx=0, nx=1, zy=1, ny=0, f=1, no=1
        # This gives !(!x + 0) = !(!x) = x, but let's try a different approach
        # Actually: zx=0, nx=1, zy=1, ny=1, f=1, no=0 gives !x + !0 = !x + (-1) = !x - 1
        # Better: zx=1, nx=0, zy=0, ny=0, f=1, no=0 gives 0 + y, then subtract x from 0
        # Let's use: zx=1, nx=0, zy=0, ny=1, f=1, no=0 -> 0 + !y = -y-1
        x = int_to_stream16(5)
        y = int_to_stream16(5)  # Use same value for y
        result = ALU(x, y, 1, 0, 0, 1, 1, 0)
        
        # 0 + (!5) = 0 + (65535-5) = 65530 = -6 in two's complement
        expected_out = int_to_stream16(65530)  # This represents -6
        self.assertEqual(result[0], expected_out)
        self.assertEqual(result[1], 0)  # Should not be zero
        self.assertEqual(result[2], 1)  # Should be negative (MSB=1)


class TestMoreArithmetic(unittest.TestCase):
    def test_add16_carry_propagation(self):
        # Test carry propagation: 255 + 1 = 256
        val_255 = int_to_stream16(255)  # 00000000 11111111
        val_1 = int_to_stream16(1)      # 00000000 00000001
        val_256 = int_to_stream16(256)  # 00000001 00000000
        result = add16(val_255, val_1)
        self.assertEqual(result, val_256)
    
    def test_add16_overflow(self):
        # Test 16-bit overflow: 65535 + 1 = 0 (with overflow)
        max_val = int_to_stream16(65535)  # All 1s
        one = int_to_stream16(1)
        zero = int_to_stream16(0)
        result = add16(max_val, one)
        self.assertEqual(result, zero)


class TestMoreMemory(unittest.TestCase):
    def test_register_persistence(self):
        reg = Register()
        data1 = [1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1]
        data2 = [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]
        
        # Store first data
        result1 = reg.update(data1, 1)
        self.assertEqual(list(result1), data1)
        
        # Try to overwrite with load=0 (should fail)
        result2 = reg.update(data2, 0)
        self.assertEqual(list(result2), data1)  # Should still have data1
        
        # Actually overwrite with load=1
        result3 = reg.update(data2, 1)
        self.assertEqual(list(result3), data2)
    
    def test_ram8_different_addresses(self):
        ram = RAM8()
        
        # Store different values at different addresses
        for addr in range(8):
            data = [addr % 2] * 16  # Alternating pattern based on address
            address = int_to_stream16(addr)
            result = ram.update(data, address, 1)
            self.assertEqual(result, data)
        
        # Verify all addresses still have correct data
        for addr in range(8):
            expected_data = [addr % 2] * 16
            address = int_to_stream16(addr)
            result = ram.update([0]*16, address, 0)  # load=0 for read
            self.assertEqual(list(result), expected_data)


class TestEdgeCases(unittest.TestCase):
    def test_mux16_edge_cases(self):
        # Test with alternating bits
        a = [1, 0] * 8
        b = [0, 1] * 8
        
        result_a = mux16(a, b, 0)
        result_b = mux16(a, b, 1)
        
        self.assertEqual(result_a, a)
        self.assertEqual(result_b, b)
    
    def test_and16_or16_mixed(self):
        pattern1 = [1, 1, 0, 0] * 4
        pattern2 = [1, 0, 1, 0] * 4
        
        and_result = and16(pattern1, pattern2)
        or_result = or16(pattern1, pattern2)
        
        expected_and = [1, 0, 0, 0] * 4
        expected_or = [1, 1, 1, 0] * 4
        
        self.assertEqual(and_result, expected_and)
        self.assertEqual(or_result, expected_or)
    
    def test_int_to_stream16_edge_values(self):
        # Test power of 2 values
        self.assertEqual(int_to_stream16(1), [0]*15 + [1])
        self.assertEqual(int_to_stream16(2), [0]*14 + [1, 0])
        self.assertEqual(int_to_stream16(4), [0]*13 + [1, 0, 0])
        self.assertEqual(int_to_stream16(8), [0]*12 + [1, 0, 0, 0])
        self.assertEqual(int_to_stream16(256), [0]*7 + [1] + [0]*8)
        self.assertEqual(int_to_stream16(32768), [1] + [0]*15)


if __name__ == "__main__":
    unittest.main()
