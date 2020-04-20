#!/usr/local/bin/python3
import sys

HEADSIZE = 120 # Header of BMP image should not be longer

def encode(message, bmp_in, bmp_out):
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
        
    
def run():
    try:
        if len(sys.argv) < 4:
            sys.exit(f"usage 1:  {sys.argv[0]} encode <secret-message-filename> <image-filename> <output-filename>\nusage 2:  {sys.argv[0]} decode <input-image-filename> <output-message-filename> ")
        elif len(sys.argv) < 5 and sys.argv[1].lower() == "encode":
            sys.exit(f"usage :   {sys.argv[0]} encode <secret-message-filename> <image-filename> <output-filename>")
        elif sys.argv[1].lower() == "encode":
            encode(sys.argv[2], sys.argv[3], sys.argv[4])
        elif sys.argv[1].lower() == "decode":
            decode(sys.argv[2], sys.argv[3])
    except IOError as err:
        sys.exit(f"I/O ERROR: Please check the filenames: {err}")
    except Exception as err:
        sys.exit(f"Something went wrong: {err}")


# Start
run()