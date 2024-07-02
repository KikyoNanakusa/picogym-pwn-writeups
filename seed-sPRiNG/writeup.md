# seed sPRiNG
## checksec
```
Canary                        : ✘
NX                            : ✓
PIE                           : ✓
Fortify                       : ✘
RelRO                         : Full
```
カナリアのみ無し

## main
main関数をディスアセンブルする
```
~~~略~~~
   0x0000088f <+304>:   push   0x0
   0x00000891 <+306>:   call   0x530 <time@plt>
   0x00000896 <+311>:   add    esp,0x10
   0x00000899 <+314>:   mov    DWORD PTR [ebp-0x10],eax
   0x0000089c <+317>:   mov    eax,DWORD PTR [ebp-0x10]
   0x0000089f <+320>:   sub    esp,0xc
   0x000008a2 <+323>:   push   eax
   0x000008a3 <+324>:   call   0x570 <srand@plt>
   0x000008a8 <+329>:   add    esp,0x10
   0x000008ab <+332>:   mov    DWORD PTR [ebp-0xc],0x1
   0x000008b2 <+339>:   jmp    0x975 <main+534>
   0x000008b7 <+344>:   sub    esp,0x8
   0x000008ba <+347>:   push   DWORD PTR [ebp-0xc]
   0x000008bd <+350>:   lea    eax,[ebx-0x1328]
   0x000008c3 <+356>:   push   eax
   0x000008c4 <+357>:   call   0x510 <printf@plt>
   0x000008c9 <+362>:   add    esp,0x10
   0x000008cc <+365>:   sub    esp,0xc
   0x000008cf <+368>:   lea    eax,[ebx-0x1560]
   0x000008d5 <+374>:   push   eax
   0x000008d6 <+375>:   call   0x540 <puts@plt>
   0x000008db <+380>:   add    esp,0x10
   0x000008de <+383>:   call   0x590 <rand@plt>
   0x000008e3 <+388>:   and    eax,0xf
```
`time`関数で現在時刻を取得
それをシード値にして乱数を生成
生成した乱数と`0xf`のandを取って比較に使用

以上の流れが読み取れる。
シードがプロセスを実行した時間なので問題サーバーに接続した時間をシードにして乱数を生成。それをもとに入力する。以下のようなコードで乱数を生成
```c
#include <stdio.h>

int main(void) {
  int seed = 1719894805;
  srand(seed);
  for (int i = 0; i < 0x1e; i++) {
    int random = rand();
    printf("%d\n", random & 0xf);
  }

  return 0;
}
```
時間はエポック秒で指定することに注意する
これを実行して得られた乱数を順に入力することでフラグを入手できた
