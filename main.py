from block.image import ImageFile
from mbr.MBR import MBR_Decoder

img = ImageFile("./disk.img")
mbr = MBR_Decoder(img)

signature = mbr.signature.hex()
print(f"MBR Signature is: {signature}")
if signature.lower() == "55aa":
    print("Valid signature!")
else:
    print("Error: Signature is invalid, does this image have an MBR?")
    exit()

partitions = mbr.partitions
print(f"This disk has {len(partitions)} partition(s)\n")

for i, part in enumerate(partitions):
    print(f"Partition {i+1}: ")
    print(f"Size: {part.size} bytes")
    print(f"Start position: {hex(part.start)}")
    if part.type_str != "":
        print(f"Type: {hex(part.type)} ({part.type_str})")
    else:
        print(f"Type: {hex(part.type)}")
    print(f"Attributes: {hex(part.attributes)}")
    print()