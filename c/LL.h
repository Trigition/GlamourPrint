#ifndef _LL_H_
#define _LL_H_

#include <stdio.h>
#include <stdlib.h>

typedef struct v_item {
  void *item;
  struct v_item *next;
  struct v_item *prev;
} DLL_Item;

typedef struct list {
  unsigned int length;
  DLL_Item *head;
  DLL_Item *tail;
} DLL;

DLL *get_new_list();
DLL_Item *get_new_item(void *item);

void append(DLL *list, void *item);
void prepend(DLL *list, void *item);

DLL_Item *truncate(DLL *list);
DLL_Item *pop(DLL *list);
DLL_Item *delete_at(DLL *list, unsigned int index);

void print_list(DLL *list, void (*print_item)(void *));
void free_list(DLL *list, void (*free_item)(void *));
#endif
