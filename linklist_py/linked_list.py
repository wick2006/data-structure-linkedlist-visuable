# linklist_py/linked_list.py
from typing import List, Optional

class Node:
    def __init__(self, value: int):
        self.value = value
        self.next: Optional['Node'] = None

class LinkedListPY:
    def __init__(self):
        self.head: Optional[Node] = None
        self._size = 0

    def insert_head(self, v: int) -> None:
        n = Node(v)
        n.next = self.head
        self.head = n
        self._size += 1

    def insert_tail(self, v: int) -> None:
        n = Node(v)
        if not self.head:
            self.head = n
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = n
        self._size += 1

    def insert_at(self, index: int, v: int) -> bool:
        if index < 0 or index > self._size:
            return False
        if index == 0:
            self.insert_head(v)
            return True
        cur = self.head
        for _ in range(index - 1):
            cur = cur.next
        n = Node(v)
        n.next = cur.next
        cur.next = n
        self._size += 1
        return True

    def delete_value(self, v: int) -> int:
        prev = None
        cur = self.head
        while cur:
            if cur.value == v:
                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next
                self._size -= 1
                return 1
            prev = cur
            cur = cur.next
        return 0

    def delete_at(self, index: int) -> bool:
        if index < 0 or index >= self._size:
            return False
        prev = None
        cur = self.head
        for _ in range(index):
            prev = cur
            cur = cur.next
        if prev:
            prev.next = cur.next
        else:
            self.head = cur.next
        self._size -= 1
        return True

    def reverse(self) -> None:
        prev = None
        cur = self.head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev

    def search(self, v: int) -> int:
        idx = 0
        cur = self.head
        while cur:
            if cur.value == v:
                return idx
            cur = cur.next
            idx += 1
        return -1

    def size(self) -> int:
        return self._size

    def to_list(self) -> List[int]:
        out = []
        cur = self.head
        while cur:
            out.append(cur.value)
            cur = cur.next
        return out
