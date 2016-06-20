#include "GlamourPrint.h"
#include "LL.h"

void print_me(void *item);
void free_me(void *item);
char *test_string(unsigned int length);

int main(int argc, char **argv) {
    DLL *test_DLL = get_new_list();
    DLL *test_DLL_two = get_new_list();
    // Populate Lists
    unsigned int i;
    char *new_test;
    for (i = 0; i < 10000; i++) {
      new_test = test_string(random() % 100 + 1);
      append(test_DLL, new_test);
      new_test = test_string(random() % 100 + 1);
      append(test_DLL_two, new_test);
    }
  
    printf("List One\n");
    print_list(test_DLL, print_me);
    
    printf("List Two\n");
    print_list(test_DLL_two, print_me);
    
    add_list(test_DLL, test_DLL_two);
    
    printf("Combined list\n");
    print_list(test_DLL, print_me);

    free_list(test_DLL, free_me);
}

void print_me(void *item) {
    char *str = item;
    printf("%s\n", str);
}

void free_me(void *item) {
    free(item);
}

char *test_string(unsigned int length) {
    unsigned int i;
    long nRand;
    char cRand;
    char *new_string = malloc(sizeof(char) * length + 1);
    for ( i = 0; i < length; i++) {
        nRand = random();
        cRand = (char) (nRand % 126);
        if (cRand < 33) {
            cRand += 33;
        }
        new_string[i] = cRand;
        srandom(nRand);
    }
    // Terminate the string
    new_string[length] = 0;
    return new_string;
}
