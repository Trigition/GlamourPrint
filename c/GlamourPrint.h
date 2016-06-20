#ifndef _GLAMOURPRINT_H_
#define _GLAMOURPRINT_H_

#include <stdio.h>
#include <stdlib.h>

#include "LL.h"

typedef unsigned int uint;

typedef struct out_segment {
    char *string;
    uint length;
    char *color;
} output_segment;

void reprint(char *line_str);
DLL *colored_string(char *base_string, char *color);

#endif
