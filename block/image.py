'''
FAT32-py - A FAT32 toolset written in python

block/image.py - MorganPG1:
Implements a BlockDev that reads and writes to an image file
'''

#Imports
from block.blockDev import BlockDev

class ImageFile(BlockDev):
    def __init__(self, path:str) -> None:
        '''
        Image file block device

        :param self: The ImageFile object
        :param path: The file path to the image file (eg: ./disk.img)
        :type path: str
        '''
        self.file = open(path,"rb+")
    def read(self, offset: int, count: int) -> bytes:
        #Seeks to the offset
        self.file.seek(offset)

        #Reads and returns the data
        data = self.file.read(count)
        return data
    def write(self, offset: int, data: bytes) -> None:
        #Seeks to the offset
        self.file.seek(offset)

        #Writes the data
        self.file.write(data)

        #Flushes the changes to disk
        self.file.flush()