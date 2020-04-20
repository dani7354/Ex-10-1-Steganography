#!/usr/local/bin/python3
import argparse

HEADSIZE = 120 # Header of BMP image should not be longer

def encode(bmp_in, message, bmp_out):
    with open(bmp_in, "rb") as bmp_in: 
        with open(bmp_out, "wb") as bmp_out:
            with open(message, "rb") as message:
                for i in range(HEADSIZE):
                    bmp_out.write(bmp_in.read(1))

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
        for i in range(HEADSIZE): # skip header
            bmp_in.read(1)
        msg_done = False
        with open(txt_out, "wb") as txt_out:
            while msg_done != True:
                c_bytes = bmp_in.read(8)
                char = 0x00
                for b in c_bytes:
                    char = (char << 1) | (b & 0x01)
                if char == 0x00:
                    msg_done = True
                    continue
                txt_out.write(bytes([char]))
        
        
    



encode("picture1.bmp", "message.txt", "out0.bmp")
decode("out0.bmp", "out.txt")
 





exit(0)