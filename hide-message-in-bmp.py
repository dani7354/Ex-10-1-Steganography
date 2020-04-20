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
    return



encode("picture1.bmp", "message.txt", "out0.bmp")
 





exit(0)