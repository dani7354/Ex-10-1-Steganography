#!/usr/local/bin/python3
# BMP file structure: https://en.wikipedia.org/wiki/BMP_file_format
import sys

HEADSIZE = 120 # Header of BMP image should not be longer

def encode(txt_in, bmp_in, bmp_out):
    with open(bmp_in, "rb") as bmp_in: 
        with open(bmp_out, "wb") as bmp_out:
            with open(txt_in, "rb") as txt_in:
                bmp_out.write(bmp_in.read(HEADSIZE)) # write out original header
                while msg_byte := txt_in.read(1):
                    for bit in range(7,-1,-1): # split the msg char bits as insert to last bit of 8 pixel bytes
                        bmp_byte = bmp_in.read(1)[0] & 0xFE # read in bmp byte and clear last bit 
                        bmp_byte = (bmp_byte | ((msg_byte[0] >> bit) & 0x01)) # insert msg bit to last bit in bmp byte
                        bmp_out.write(bytes([bmp_byte]))
                for byte in bmp_in.read(8): # set the LSB to 0 for 8 bytes after the message = the stop-byte
                    bmp_out.write(bytes([byte & 0xFE])) 
                bmp_out.write(bmp_in.read()) # write out the rest of the input bmp file
            
             
def decode(bmp_in, txt_out):
    with open(bmp_in, "rb") as bmp_in:
        bmp_in.read(HEADSIZE) # skip header
        with open(txt_out, "wb") as txt_out:
            while char_bytes := bmp_in.read(8): # read in the next 8 bytes from BMP file
                char = 0x00 # new char byte = all bits off
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