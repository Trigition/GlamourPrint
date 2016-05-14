#include "LL.h"

/**
 * This function allocated the header for a new list.
 * @return A pointer to the new list.
 */
DLL *get_new_list() {
    DLL *new_list;
    new_list = malloc(sizeof(DLL));
    new_list->length = 0;
    new_list->head = NULL;
    new_list->tail = NULL;
    return new_list;
}

DLL_Item *get_new_item(void *item) {
    // Allocate space
    DLL_Item *new_item = malloc(sizeof(DLL_Item));
    new_item->item = item;
    new_item->next = NULL;
    new_item->prev = NULL;
    return new_item;
}

/**
 * This function appends a new item to the list.
 * @param list The list that the item will be appended to.
 * @param item The item being appended.
 */
void append(DLL *list, void *item) {
    // Get tail
    DLL_Item *tail = list->tail;
    // Get new item
    DLL_Item *new_item = get_new_item(item);
    // Check for size
    if (list->length > 0) {
        // Link new item to tail
        tail->next = new_item;
        new_item->prev = tail;
    } else {
        // Head and tail are one and the same
        list->head = new_item;
    }
    // Update header to new tail
    list->tail = new_item;
    // Update length
    list->length++;
}

/**
 *  This function prepends an item to the list.
 *  @param list The list that the item will be prepended to.
 *  @param item The item that is being appended.
 */
void prepend(DLL *list, void *item) {
    // Get head
    DLL_Item *head = list->head;
    // Get new item
    DLL_Item *new_item = get_new_item(item);
    // Check for size
    if (list->length > 0) {
        // Link item to current head
        new_item->next = head;
        head->prev = new_item;
    } else {
        // Head and tail are one and the same
        list->tail = new_item;
    }
    // Update header for new head
    list->head = new_item;
    // Update length
    list->length++;
}


/**
 * This function truncates the last item on the list.
 * @param list The list that will be truncated.
 * @return The truncated item
 */
DLL_Item *truncate(DLL *list) {
    // Get last element
    DLL_Item *last_item = list->tail;
    DLL_Item *new_tail = list->tail->prev;
    // Check size
    if (list->length > 1) {
        // Set the previous item so that it represents the end of the list
        new_tail->next = NULL;
        list->tail = new_tail;
    } else {
        // List will now be empty
        list->head = NULL;
        list->tail = NULL;
    }
    // Update length
    list->length--;
    last_item->next = NULL;
    last_item->prev = NULL;
    return last_item;
}

/**
 * This function pops the first item on the list.
 * @param list The list that will be popped.
 * @return The popped item.
 */
DLL_Item *pop(DLL *list) {
    // Get first element
    DLL_Item *first_item = list->head;
    //Check for size
    if (list->length > 1) {
      // Set the next item so that it represents the beginning of the list
      DLL_Item *new_head = list->head->next;
      new_head->prev = NULL;
      list->head = new_head;
    } else {
      // List will now be empty
      list->head = NULL;
      list->tail = NULL;
    }
    //Update Length
    list->length--;
    first_item->next = NULL;
    first_item->prev = NULL;
    return first_item;
}

/**
 * This function prints the entire list using a given print function.
 * @param list The list to be printed.
 * @param print_item The function specifying how the item should be printed.
 */
void print_list(DLL *list, void(*print_item)(void *)) {
    DLL_Item *cur_item;
    cur_item = list->head;
    while (cur_item != NULL) {
        print_item(cur_item->item);
        cur_item = cur_item->next;
    }
}

/**
 * This function frees the list.
 * @param list The list to be freed.
 * @param free_item The function to free the contained data.
 */
void free_list(DLL *list, void (*free_item)(void *)) {
    DLL_Item *cur_item;
    while (list->length > 0) {
        cur_item = pop(list);
        free_item(cur_item->item);
        free(cur_item);
    }
    free(list);
}
