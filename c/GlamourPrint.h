#ifndef _GLAMOURPRINT_H_
#define _GLAMOURPRINT_H_

typedef unsigned int uint;

typedef struct out_segment {
    char *string;
    uint length;
    char *color;
} output_segment;

void reprint(char *line_str);
void colored_string();


#endif
