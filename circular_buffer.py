class CircularBuffer(object):

    def __init__(self, max_size=10):
        """inicjalizacja parametrow bufora"""
        self.buffer = [None] * max_size
        self.head = 0
        self.tail = 0
        self.max_size = max_size

    def __str__(self):
        """zwracanie sformatowanego stringa"""
        items = ['{!r}'.format(item) for item in self.buffer]
        return '[' + ', '.join(items) + ']'

    def size(self):
        """Zwracanie rozmiaru bufora"""
        if self.tail >= self.head:
            return self.tail - self.head
        return self.max_size - self.head - self.tail

    def is_empty(self):
        """Zwracanie true, jeśli bufor jest pusty"""
        return self.tail == self.head

    def is_full(self):
        """zwracanie true, jeśli ogon jest przed glowa """
        return self.tail == (self.head-1) % self.max_size

    def enqueue(self, item):
        """Wstawianie elementu na koniec bufora"""
        if self.is_full():
            raise OverflowError(
                "Bufor jest pełny, nie mozna zapisac elementu")
        self.buffer[self.tail] = item
        self.tail = (self.tail + 1) % self.max_size

    def front(self):
        """Zwraca element z przodu bufora"""
        return self.buffer[self.head]

    def dequeue(self):
        """Zwraca element z przodu bufora i usuwa"""
        if self.is_empty():
            raise IndexError("CircularBuffer is empty, unable to dequeue")
        item = self.buffer[self.head]
        self.buffer[self.head] = None
        self.head = (self.head + 1) % self.max_size
        return item