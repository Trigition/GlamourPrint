#ifndef _GLAMOURPRINT_H_
#define _GLAMOURPRINT_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "LL.h"
#include "colors.h"

typedef unsigned int uint;

typedef struct outsegment {
    char *string;
    char *suffix;
    char *prefix;
    uint length;
} Out_Segment;

void reprint(char *line_str);
Out_Segment *colored_string(char *base_string, char *color);
char *compile_outsegment(Out_Segment *segment);
#endif
