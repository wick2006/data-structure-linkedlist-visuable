#include "linkedlist.h"
#include <cstdlib>
#include <new>
#include <vector>

struct Node {
    int value;
    Node* next;
    Node(int v): value(v), next(nullptr) {}
};

class LinkedList {
public:
    LinkedList(): head(nullptr), sz(0) {}
    ~LinkedList() { clear(); }

    void clear() {
        Node* cur = head;
        while (cur) {
            Node* tmp = cur->next;
            delete cur;
            cur = tmp;
        }
        head = nullptr;
        sz = 0;
    }

    void insert_head(int v) {
        Node* n = new Node(v);
        n->next = head;
        head = n;
        ++sz;
    }

    void insert_tail(int v) {
        Node* n = new Node(v);
        if (!head) {
            head = n;
        } else {
            Node* cur = head;
            while (cur->next) cur = cur->next;
            cur->next = n;
        }
        ++sz;
    }

    bool insert_at(int index, int v) {
        if (index < 0 || index > sz) return false;
        if (index == 0) { insert_head(v); return true; }
        Node* cur = head;
        for (int i = 0; i < index - 1; ++i) cur = cur->next;
        Node* n = new Node(v);
        n->next = cur->next;
        cur->next = n;
        ++sz;
        return true;
    }

    int delete_value(int v) {
        Node* cur = head;
        Node* prev = nullptr;
        while (cur) {
            if (cur->value == v) {
                if (prev) prev->next = cur->next;
                else head = cur->next;
                delete cur;
                --sz;
                return 1;
            }
            prev = cur;
            cur = cur->next;
        }
        return 0;
    }

    bool delete_at(int index) {
        if (index < 0 || index >= sz) return false;
        Node* cur = head;
        Node* prev = nullptr;
        for (int i = 0; i < index; ++i) {
            prev = cur;
            cur = cur->next;
        }
        if (prev) prev->next = cur->next;
        else head = cur->next;
        delete cur;
        --sz;
        return true;
    }

    void reverse() {
        Node* prev = nullptr;
        Node* cur = head;
        while (cur) {
            Node* nxt = cur->next;
            cur->next = prev;
            prev = cur;
            cur = nxt;
        }
        head = prev;
    }

    int search(int v) {
        Node* cur = head;
        int idx = 0;
        while (cur) {
            if (cur->value == v) return idx;
            cur = cur->next;
            ++idx;
        }
        return -1;
    }

    int size() const { return sz; }

    std::vector<int> to_vector() const {
        std::vector<int> out;
        out.reserve(sz);
        Node* cur = head;
        while (cur) {
            out.push_back(cur->value);
            cur = cur->next;
        }
        return out;
    }

private:
    Node* head;
    int sz;
};

extern "C" {

#ifdef _MSC_VER
    #define LL_EXPORT __declspec(dllexport)
#else
    #define LL_EXPORT __attribute__((visibility("default")))
#endif

LL_EXPORT void* ll_create() {
    try {
        return reinterpret_cast<void*>(new LinkedList());
    } catch (const std::bad_alloc&) {
        return nullptr;
    }
}

LL_EXPORT void ll_destroy(void* list) {
    if (!list) return;
    LinkedList* L = reinterpret_cast<LinkedList*>(list);
    delete L;
}

LL_EXPORT int ll_insert_head(void* list, int value) {
    if (!list) return -1;
    LinkedList* L = reinterpret_cast<LinkedList*>(list);
    L->insert_head(value);
    return 0;
}

LL_EXPORT int ll_insert_tail(void* list, int value) {
    if (!list) return -1;
    LinkedList* L = reinterpret_cast<LinkedList*>(list);
    L->insert_tail(value);
    return 0;
}

LL_EXPORT int ll_insert_at(void* list, int index, int value) {
    if (!list) return -1;
    LinkedList* L = reinterpret_cast<LinkedList*>(list);
    return L->insert_at(index, value) ? 0 : -1;
}

LL_EXPORT int ll_delete_value(void* list, int value) {
    if (!list) return -1;
    LinkedList* L = reinterpret_cast<LinkedList*>(list);
    return L->delete_value(value);
}

LL_EXPORT int ll_delete_at(void* list, int index) {
    if (!list) return -1;
    LinkedList* L = reinterpret_cast<LinkedList*>(list);
    return L->delete_at(index) ? 0 : -1;
}

LL_EXPORT int ll_reverse(void* list) {
    if (!list) return -1;
    LinkedList* L = reinterpret_cast<LinkedList*>(list);
    L->reverse();
    return 0;
}

LL_EXPORT int ll_search(void* list, int value) {
    if (!list) return -1;
    LinkedList* L = reinterpret_cast<LinkedList*>(list);
    return L->search(value);
}

LL_EXPORT int ll_size(void* list) {
    if (!list) return -1;
    LinkedList* L = reinterpret_cast<LinkedList*>(list);
    return L->size();
}

LL_EXPORT int* ll_to_array(void* list, int* out_len) {
    if (!list || !out_len) return nullptr;
    LinkedList* L = reinterpret_cast<LinkedList*>(list);
    std::vector<int> v = L->to_vector();
    if (v.empty()) {
        *out_len = 0;
        return nullptr;
    }
    *out_len = static_cast<int>(v.size());
    int* arr = (int*)std::malloc(sizeof(int) * (*out_len));
    if (!arr) {
        *out_len = 0;
        return nullptr;
    }
    for (int i = 0; i < *out_len; ++i) arr[i] = v[i];
    return arr;
}

LL_EXPORT void ll_free_array(int* arr) {
    if (!arr) return;
    std::free(arr);
}

} // extern "C"

