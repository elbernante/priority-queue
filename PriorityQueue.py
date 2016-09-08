from itertools import count

class PriorityQueue(object):
    def __init__(self, items=None):
        """
        :params items: key:priority pairs
        """
        # TODO: Implement mode: MIN or MAX mode
        # TODO: Implement custom comparator
        # TODO: Implement FIFO/LIFO for equal priorities

        self.heap = []
        self.item_index = {}
        self._count = count()
        if items: self._heapify(items)

    @property
    def peek(self):
        if len(self.heap) == 0: return None
        return self.heap[0][2], self.heap[0][0]

    def push(self, key, priority):
        self.__setitem__(key, priority)

    def pop(self, key=None, *default):
        if len(self.heap) == 0:
            raise IndexError, "pop from empty queue"

        if key is None:
            key = self.heap[0][2]

        return self._remove_item(key, *default)

    def _heapify(self, items):
        """
        :params items: key:priority pairs
        """

        # TODO: Heap building for list of tuples

        self.heap = [(v, next(self._count), k) for k, v in items.items()]
        for i, (_, _, k) in  enumerate(self.heap):
            self.item_index[k] = i

        # TODO: Verify equal count for self.heap and self.item_index

        half = (len(self.heap) // 2) - 1
        last_index = len(self.heap) - 1
        for i in range(half, -1, -1):
            self._down_heapify(i, last_index)

    def _up_heapify(self, i):
        p = (i - 1) // 2
        while p >= 0 and self.heap[p] > self.heap[i]:
            self._swap(p, i)
            i, p = p, (p - 1) // 2

    def _down_heapify(self, i, last_index):
        mc = self._min_child(i, last_index)
        while mc > -1 and self.heap[i] > self.heap[mc]:
            self._swap(i, mc)
            i, mc = mc, self._min_child(mc, last_index)

    def _min_child(self, i, last_index):
        left, right = 2 * i + 1, 2 * i + 2
        return -1 if left > last_index else \
               left if right > last_index else \
               left if self.heap[left] < self.heap[right] else \
               right

    def _swap(self, i, j):
        a, b = self.heap[i][2], self.heap[j][2]
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]  # swap heap
        self.item_index[a], self.item_index[b] = j, i        # update item index

    def _heap_push(self, item):
        """
        :params item: (priority, unique_entry_id, key)
        """
        self.heap.append(item)
        self.item_index[item[2]] = len(self.heap) - 1
        self._up_heapify(len(self.heap) - 1)

    def _remove_item(self, key, *default):
        assert len(self.heap) > 0, "remove from empty queue"

        if len(default) > 1: 
            raise TypeError, "remove() expected at most 2 arguments, got {}" \
                             .format(len(default))

        if len(default) > 0:
            index = self.item_index.get(key, None)
            if index is None: return default[0]
        else:
            index = self.item_index[key]

        item = self.heap[index]
        if len(self.heap) > 1:
            p_0 = self.heap[0][0]

            # set to current highest prioty, and -1 ID to allow to go to root
            new_item = (p_0, -1, item[2])
            self.heap[index] = new_item
            self._up_heapify(index)

            # prepare to remove root
            self._swap(0, len(self.heap) - 1)
            self._down_heapify(0, len(self.heap) - 2)

        # remove root
        self.heap.pop()
        self.item_index.pop(item[2], None)

        return item[2], item[0]

    def _update_item(self, key, priority):
        index = self.item_index[key]
        old_priority = self.heap[index][0]
        updated = (priority, next(self._count), key)
        self.heap[index] = updated

        if priority < old_priority:
            self._up_heapify(index)
        else:
            self._down_heapify(index, len(self.heap) - 1)

    def get(self, key, *default):
        if len(default) > 1: 
            raise TypeError, "get() expected at most 2 arguments, got {}" \
                             .format(len(default))
        if len(default) > 0:
            val = self.item_index.get(key, None)
            return default[0] if val is None else self.heap[val][0]
        else:
            return self.__getitem__(key)

    def iterpop(self):
        while self.heap:
            yield self.pop()

    def items(self):
        for p, _, k in self.heap:
            yield k, p

    def keys(self):
        for _, _, k in self.heap:
            yield k

    def values(self):
        for p, _, _ in self.heap:
            yield p 

    def __contains__(self, key):
        return key in self.item_index

    def __getitem__(self, key):
        return self.heap[self.item_index[key]][0]

    def __setitem__(self, key, value):
        if key not in self.item_index:
            self._heap_push((value, next(self._count), key))
        else:
            self._update_item(key, value)

    def __delitem__(self, key):
        self.pop(key)

    def __iter__(self):
        for _, _, k in self.heap:
            yield k

    def __len__(self):
        return len(self.heap)

    # TODO: addition
    # TODO: subtraction

