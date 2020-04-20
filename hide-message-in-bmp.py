#!/usr/local/bin/python3
import argparse

HEADSIZE = 120 # Header of BMP image should not be longer

def encode(bmp_in, message, bmp_out):
    with open(bmp_in, "rb") as bmp_in: 
        with open(bmp_out, "wb") as bmp_out:
            with open(message, "rb") as message:
                bmp_out.write(bmp_in.read(HEADSIZE))
                while mb := message.read(1):
                    for bit in range(7,-1,-1):
                        c = bmp_in.read(1)[0] & 0xFE
                        c = (c | ((mb[0] >> bit) & 0x01))
                        bmp_out.write(bytes([c]))
                for i in range(7,-1,-1):
                    c = bmp_in.read(1)[0] & 0xFE
                    bmp_out.write(bytes([c]))
                bmp_out.write(bmp_in.read())
            
             
def decode(bmp_in, txt_out):
    with open(bmp_in, "rb") as bmp_in:
        bmp_in.read(HEADSIZE) # skip header
        with open(txt_out, "wb") as txt_out:
            while char_bytes := bmp_in.read(8): # read in the next 8 bytes from BMP file
                char = 0x00 # char byte = all bits off
                for byte in char_bytes:
                    char = (char << 1) | (byte & 0x01) # move all bits one pos to the left and add one bit to the right (a new least significant bit)
                if char == 0x00: # Stop-byte is reached?
                    break
                txt_out.write(bytes([char])) # write out the char to the output text file
        
        
    



encode("picture1.bmp", "message.txt", "out0.bmp")
decode("out0.bmp", "out.txt")
 





exit(0)