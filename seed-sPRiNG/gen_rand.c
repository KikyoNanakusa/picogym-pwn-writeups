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
