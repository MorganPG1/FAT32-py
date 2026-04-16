'''
FAT32-py - A FAT32 toolset written in python

block/blockDev.py - MorganPG1:
Generic block device class and methods
'''

class BlockDev():
    def __init__(self) -> None:
        '''
        Generic block device class, inherit this in a block device implementation
        
        :param self: The BlockDev object
        '''
        pass
    def read(self, offset:int, count:int) -> bytearray:
        '''
        Reads data from the block device

        :param self: The BlockDev object
        :param offset: The offset to begin reading from
        :type offset: int
        :param count: The number of bytes to read
        :type count: int
        :return: The bytes read
        :rtype: bytearray
        '''
        return bytearray(count)
    def write(self, offset:int, data:bytes|bytearray) -> None:
        '''
        Writes data to the block device

        :param self: The BlockDev object
        :param offset: The offset to begin writing from
        :type offset: int
        :param data: The bytes to write
        :type data: bytes|bytearray
        '''
        pass