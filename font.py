
GLYFS = {
    
    "0":"0xeccdc0",
    "1":"0x8ffc00",
    "2":"0x199dfa0",
    "3":"0x11afdc0",
    "4":"0x1e13c40",
    "5":"0x1dedee0",
    "7":"0x119db80",
    "6":"0x1ffd6e0",
    "8":"0x1fad5e0",
    "9":"0x1ca5de0",
    
    " ":"0x0",
    ".":"0x318000",
    ",":"0x110000",
    "!":"0xef7a0",
    "-":"0x421080",
    
    "a":"0xfde9e0",
    "b":"0x1ffd540",
    "c":"0xefc540",
    "d":"0x1ffc5c0",
    "e":"0x1ffd620",
    "f":"0x1ffd200",
    "g":"0xe8dcc0",
    "h":"0x1ff93e0",
    "i":"0xffc00",
    "j":"0x30ffc0",
    "k":"0x1f3ea60",
    "l":"0xff8440",
    "m":"0x1fe3b9f",
    "n":"0x1f61be0",
    "o":"0xefc5c0",
    "p":"0xffd180",
    "q":"0xdf45c0",
    "r":"0xffd9a0",
    "s":"0x1ded6e0",
    "t":"0x10ffe00",
    "u":"0x1ef87e0",
    "v":"0x1ef9b80",
    "w":"0x1f1907f",
    "x":"0x1bf93e0",
    "y":"0x18f9f00",
    "z":"0x13bf720",
    
}

BITMAP_SIZE = 25

class Font():
    def __init__(self):
        return

    def get_glyf_bitmap(self,glyf):
        return self.hex_to_bitmap(GLYFS[glyf])

    def hex_to_bitmap(self,hex_string):
        binary_string = bin(int(hex_string, 16))[2:]
        binary_string =  '0' * (BITMAP_SIZE - len(binary_string)) + binary_string
        binary_array = [int(bit) for bit in binary_string]
        return binary_array

    def bitmap_to_hex(self,bitmap):
        binary_string = ''.join(str(bit) for bit in bitmap )
        hex_value = hex(int(binary_string, 2))
        print(hex_value)
