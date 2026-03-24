'''
FAT32-py - A FAT32 toolset written in python

mbr/MBR.py - MorganPG1:
Master Boot Record decoder

Sources:
https://wiki.osdev.org/MBR_(x86)
'''
#Imports
from block.blockDev import BlockDev

class MBR_Decoder():
    def __init__(self, disk:BlockDev) -> None:
        self.bootstrap = bytearray(disk.read(0x000, 440))
        self.diskId = bytearray(disk.read(0x1B8, 4))
        self.part1Entry = bytearray(disk.read(0x1BE,16))
        self.part2Entry = bytearray(disk.read(0x1CE,16))
        self.part3Entry = bytearray(disk.read(0x1DE,16))
        self.part4Entry = bytearray(disk.read(0x1EE,16))
        self.signature = bytearray(disk.read(0x1FE,2))
        
        pass