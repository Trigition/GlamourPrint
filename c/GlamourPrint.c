#include "GlamourPrint.h"

void reprint(char *line_str) {
    printf("%s", line_str);
    printf("\r");
}

Out_Segment *colored_string(char *base_string, char *color) {
    // Create and construct new colored_segment datastructure
    Out_Segment *colored_segment;
    colored_segment = malloc(sizeof(Out_Segment));
    uint size = strlen(base_string);
    colored_segment->string = base_string;
    colored_segment->length = size;
    colored_segment->prefix = color;
    colored_segment->suffix = RESET;
    size += strlen(color) + strlen(RESET);

    return colored_segment;}

char *compile_outsegment(Out_Segment *segment) {
    char *compiled_string;
    return compiled_string;
}
