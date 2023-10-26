print(bytes(str(1), "utf-8"))
print(bytes(str(2), "utf-8"))
print(bytes(str(3), "utf-8"))

byte_1 = (1).to_bytes(1, 'little')
byte_2 = (2).to_bytes(1, 'little')
byte_3 = (3).to_bytes(1, 'little')

print(byte_1)
print(byte_2)
print(byte_3)

result1 = str(byte_1, 'utf-8')
result2 = str(byte_2, 'utf-8')
result3 = str(byte_3, 'utf-8')

print(result1)
print(result2)
print(result3)