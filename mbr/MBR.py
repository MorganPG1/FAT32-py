'''
FAT32-py - A FAT32 toolset written in python

mbr/MBR.py - MorganPG1:
Master Boot Record decoder

Sources:
https://wiki.osdev.org/MBR_(x86)
'''
#Imports
from block.blockDev import BlockDev

class MBR_Partition():
    def __init__(self, data:bytearray) -> None:
        self.attributes = data[0]
        self.type = int.from_bytes(data[0x4:0x5], "little")
        self.start = int.from_bytes(data[0x8:0xC], "little") * 512
        self.size = int.from_bytes(data[0xC:0x10], "little") * 512
class MBR_Decoder():
    def __init__(self, disk:BlockDev) -> None:
        self.bootstrap = bytearray(disk.read(0x000, 440))
        self.diskId = bytearray(disk.read(0x1B8, 4))
        self.partitionEntries = [bytearray(disk.read(0x1BE,16)), bytearray(disk.read(0x1CE,16)), bytearray(disk.read(0x1DE,16)), bytearray(disk.read(0x1EE,16))]
        self.signature = bytearray(disk.read(0x1FE,2))
        
        self.partitions:list[MBR_Partition] = []
        for entry in self.partitionEntries:
            part = MBR_Partition(entry)
            if part.type != 0:
                self.partitions.append(part)
        pass