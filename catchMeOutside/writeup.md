# catch me outside
## ローカルで動かない
[pwninit](https://github.com/io12/pwninit/releases/download/3.3.1/pwninit )を使用して解決
```bash 
wget https://github.com/io12/pwninit/releases/download/3.3.1/pwninit 
chmod +x pwninit
./pwninit
```

## checksec
```
Canary                        : ✓
NX                            : ✓
PIE                           : ✘
Fortify                       : ✘
RelRO                         : Partial
```

## デコンパイル
main関数のアセンブラがやたら長いのでデコンパイル。
以下のようになった。
```c

undefined8 main(void)

{
  long in_FS_OFFSET;
  undefined value_input;
  int address_input;
  int i;
  undefined8 *local_a0;
  undefined8 *correct_str;
  FILE *flag_fd;
  undefined8 *fail_str;
  void *local_80;
  undefined8 local_78;
  undefined8 local_70;
  undefined8 local_68;
  undefined local_60;
  char flag_txt [72];
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  setbuf(stdout,(char *)0x0);
  flag_fd = fopen("flag.txt","r");
  fgets(flag_txt,0x40,flag_fd);
  local_78 = 0x2073692073696874;
  local_70 = 0x6d6f646e61722061;
  local_68 = 0x2e676e6972747320;
  local_60 = 0;
  local_a0 = (undefined8 *)0x0;
  for (i = 0; i < 7; i = i + 1) {
    correct_str = (undefined8 *)malloc(0x80);
    if (local_a0 == (undefined8 *)0x0) {
      local_a0 = correct_str;
    }
    *correct_str = 0x73746172676e6f43;
    correct_str[1] = 0x662072756f592021;
    correct_str[2] = 0x203a73692067616c;
    *(undefined *)(correct_str + 3) = 0;
    strcat((char *)correct_str,flag_txt);
  }
  fail_str = (undefined8 *)malloc(0x80);
  *fail_str = 0x5420217972726f53;
  fail_str[1] = 0x276e6f7720736968;
  fail_str[2] = 0x7920706c65682074;
  *(undefined4 *)(fail_str + 3) = 0x203a756f;
  *(undefined *)((long)fail_str + 0x1c) = 0;
  strcat((char *)fail_str,(char *)&local_78);
  free(correct_str);
  free(fail_str);
  address_input = 0;
  value_input = 0;
  puts("You may edit one byte in the program.");
  printf("Address: ");
  __isoc99_scanf(&DAT_00400b48,&address_input);
  printf("Value: ");
  __isoc99_scanf(&DAT_00400b53,&value_input);
  *(undefined *)((long)address_input + (long)local_a0) = value_input;
  local_80 = malloc(0x80);
  puts((char *)((long)local_80 + 0x10));
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

途中に出てくる長いhexは文字。  
`scanf`のフォーマットは`d`と`c`  

- `local_aO` = 0x6034a0
- 1つ目のtcache bin `0x603890` = 0x602088
- 2つ目のfreed chunk = `0x603800`

## 参考文献
https://sh0ebill.hatenablog.com/entry/2022/09/28/215346
