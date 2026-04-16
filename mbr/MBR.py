'''
FAT32-py - A FAT32 toolset written in python

mbr/MBR.py - MorganPG1:
Master Boot Record decoder

Sources:
https://wiki.osdev.org/MBR_(x86)
'''
#Imports
from block.blockDev import BlockDev
from mbr.part_ids import PART_IDS

class PartEntry():
    def __init__(self, data:bytearray) -> None:
        '''
        MBR Partition entry decoder

        :param self: The PartEntry object
        :param data: The raw partition entry
        :type data: bytearray
        '''
        self.attributes = data[0]
        self.type = int.from_bytes(data[0x4:0x5], "little")
        self.size = int.from_bytes(data[0xC:0x10], "little") * 512
        self.start = int.from_bytes(data[0x8:0xC], "little") * 512
        self.end = self.start + self.size

        #Translate Partition ID into a string
        if self.type < len(PART_IDS):
            self.type_str = PART_IDS[self.type]
        else:
            self.type_str = ""

class Partition(BlockDev):
    def __init__(self, entry:PartEntry, blkDev:BlockDev) -> None:
        '''
        Block device for accessing partitions

        :param self: The Partition object
        :param entry: The PartEntry object
        :type entry: PartEntry
        :param blkDev: The block device containing the partitions
        :type blkDev: BlockDev
        '''
        self.entry = entry
        self.blk = blkDev
    def read(self, offset: int, count: int) -> bytearray:
        start = offset + self.entry.start  
        end = start + count
        
        if end <= self.entry.end:
            data = self.blk.read(start, count)
            return data
        else:
            raise IOError(f"{end} is bigger than the partition which ends at {self.entry.end}")
    def write(self, offset: int, data: bytes | bytearray) -> None:
        start = offset + self.entry.start  
        end = start + len(data)
        
        if end <= self.entry.end:
            self.blk.write(start, data)
        else:
            raise IOError(f"{end} is bigger than the partition which ends at {self.entry.end}")

class MBR_Decoder():
    def __init__(self, disk:BlockDev) -> None:
        '''
        MBR Decoder class

        :param self: The MBR_Decoder object
        :param disk: The block device to decode the MBR from
        :type disk: BlockDev
        '''
        self.disk = disk
        self.bootstrap = bytearray(disk.read(0x000, 440))
        self.diskId = bytearray(disk.read(0x1B8, 4))
        self.partitionEntries = [
            bytearray(disk.read(0x1BE,16)), 
            bytearray(disk.read(0x1CE,16)), 
            bytearray(disk.read(0x1DE,16)), 
            bytearray(disk.read(0x1EE,16))
        ]
        self.signature = bytearray(disk.read(0x1FE,2))
        
        self.partitions:list[PartEntry] = []
        for entry in self.partitionEntries:
            part = PartEntry(entry)
            if part.type != 0:
                self.partitions.append(part)
        pass

    def getPartition(self, index:int) -> Partition:
        '''
        Returns the partition block device for reading and writing to partitions

        :param self: The MBR_Decoder object
        :param index: The index of the partition (0-3)
        :type index: int
        :return: The partition block device
        :rtype: Partition
        '''
        if index < len(self.partitions):
            part = self.partitions[index]
            return Partition(part, self.disk)
        else:
            raise IndexError(f"Partition index {index} does not exist")