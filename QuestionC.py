# Write a new library that can be integrated to the Ormuco stack.
# Dealing with network issues everyday, latency is our biggest problem.
# Thus, your challenge is to write a new Geo Distributed LRU (Least Recently Used)
# cache with time expiration. This library will be used extensively by many of our
# services so it needs to meet the following criteria:

#     1 - Simplicity. Integration needs to be dead simple.
#     2 - Resilient to network failures or crashes.
#     3 - Near real time replication of data across Geolocation. Writes need to be in real time.
#     4 - Data consistency across regions
#     5 - Locality of reference, data should almost always be available from the closest region
#     6 - Flexible Schema
#     7 - Cache can expire

# I implemented a simple cache using a doubly linked list and a hashmap for fast
# writes and retrieval time. I also implemented an expiration timeout that is reset
# every time the cache is accessed.

# I did not however implement geolocation and my solution is not resilient to
# network failures or crashes. I am not entirely sure what I am asked to do for
# these last 2 points.

# My LRUCache takes in a size in number of elements and a timeout in seconds.


from threading import Thread
from time import sleep


class Element:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        # previous oldest element
        self.prev = None
        # next oldest element
        self.next = None


class LRUCache:

    def __init__(self, max_size, timeout):
        self.cache = {}
        if max_size <= 0:
            raise ValueError("Invalid size")
        self.max_size = max_size
        self.head = None
        self.tail = None

        if timeout <= 0:
            raise ValueError("Invalid timeout")
        self.timeout = timeout
        self.time_remaining = timeout
        self.expired = False
        self.__start_timeout_timer()

    def update(self, key, value):
        self.__reset_timeout()
        # check if key already in cache
        if key in self.cache:
            element = self.cache[key]
            element.value = value

            # Update head and tail of the cache
            if self.head != element:
                self.__delete(element, False)
                self.set_head(element)

        else:
            # Check if cache is full
            if len(self.cache) >= self.max_size:
                self.__delete(self.tail, True)

            new_element = Element(key, value)
            self.__set_head(new_element)
            self.cache[key] = new_element

    def get(self, key):
        self.__reset_timeout()
        if key not in self.cache:
            return None

        element = self.cache[key]

        if self.head == element:
            return element.value
        self.__delete(element, False)
        self.__set_head(element)
        return element.value

    # Helper function to see the contents of the cache
    def print_cache(self):
        if self.head is None:
            print("Cache is empty")
        else:
            element = self.head
            print(f"Head : ({element.key}, {element.value})")
            while element.next is not None:
                element = element.next
                print(f"({element.key}, {element.value})")

    def __set_head(self, element):
        if self.head is None:
            self.head = element
            self.tail = element
        else:
            element.next = self.head
            self.head.prev = element
            self.head = element

    def __delete(self, element, size_exceeded):
        if len(self.cache) == 0:
            return

        if self.tail == element:
            self.tail = element.prev
            element.prev.next = None
        else:
            if element.prev:
                element.prev.next = element.next
            if element.next:
                element.next.prev = element.prev
        # Remove the element from the cache dictionary
        if size_exceeded:
            del self.cache[element.key]

    def __reset_timeout(self):
        self.time_remaining = self.timeout
        if self.expired:
            self.__start_timeout_timer()

    def __start_timeout_timer(self):
        thread = Thread(target=self.__adjust_time_remaining)
        thread.start()
        self.expired = False

    def __adjust_time_remaining(self):
        while True:
            if self.time_remaining <= 0:
                self.cache.clear()
                self.head = None
                self.tail = None
                self.expired = True
                print("Cache expired")
                break

            sleep(1)
            self.time_remaining -= 1
