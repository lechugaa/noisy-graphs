import heapq


class MinHeap:
    def __init__(self):
        self.__h = []

    def push(self, value):
        heapq.heappush(self.__h, value)

    def pop(self):
        return heapq.heappop(self.__h)

    def __getitem__(self, item):
        return self.__h[item]

    def __len__(self):
        return len(self.__h)

    def __repr__(self):
        return f"{[value for value in self.__h]}"

    def __str__(self):
        return f"{[value for value in self.__h]}"


class MaxHeap:
    def __init__(self):
        self.__h = []

    def push(self, value):
        heapq.heappush(self.__h, -value)

    def pop(self):
        return -heapq.heappop(self.__h)

    def __getitem__(self, item):
        return -self.__h[item]

    def __len__(self):
        return len(self.__h)

    def __repr__(self):
        return f"{[-value for value in self.__h]}"

    def __str__(self):
        return f"{[-value for value in self.__h]}"
