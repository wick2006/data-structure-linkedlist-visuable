#ifndef LINKEDLIST_H
#define LINKEDLIST_H

#include <cstddef>

#ifdef __cplusplus
extern "C" {
#endif

/* C 接口：只声明 C 风格函数，保证 ctypes 可用 */
void* ll_create();
void  ll_destroy(void* list);

int ll_insert_head(void* list, int value);
int ll_insert_tail(void* list, int value);
int ll_insert_at(void* list, int index, int value);

int ll_delete_value(void* list, int value);
int ll_delete_at(void* list, int index);

int ll_reverse(void* list);
int ll_search(void* list, int value);
int ll_size(void* list);

int* ll_to_array(void* list, int* out_len);
void ll_free_array(int* arr);

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* LINKEDLIST_H */

