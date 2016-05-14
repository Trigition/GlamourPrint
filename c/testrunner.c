#include "GlamourPrint.h"
#include "LL.h"

void print_me(void *item);
void free_me(void *item);

int main(int argc, char **argv) {
    char *test1 = "This is test string 1";
    char *test2 = "This is test string 2";
    char *test3 = "This is test string 3";
    DLL *test_DLL = get_new_list();
    printf("Inserting...\n");
    append(test_DLL, test1);
    printf("Inserting again...\n");
    append(test_DLL, test2);
    printf("Inserttttiinnngggg...\n");
    append(test_DLL, test3);
    print_list(test_DLL, print_me);
    free_list(test_DLL, free_me);
}

void print_me(void *item) {
    char *str = item;
    printf("%s\n", str);
}

void free_me(void *item) {
    return;
}
