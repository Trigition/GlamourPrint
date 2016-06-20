#include "GlamourPrint.h"

void reprint(char *line_str) {
    printf("%s", line_str);
    printf("\r");
}

DLL *colored_string(char *base_string, char *color) {
    DLL *structured_string = get_new_list();
    
    append(structured_string, color);
    append(structured_string, base_string);
    return structured_string;
}
