# Int packing
r = 255
g = 128
b = 100

r
g<<=8
b<<=16

packed = r + g + b
print(packed)

r = packed & 255
g = packed >> 8 & 255
b = packed >> 16 & 255

print(str(r) + " " + str(g) + " " + str(b))