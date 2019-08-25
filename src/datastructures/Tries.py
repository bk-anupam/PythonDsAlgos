class TrieST:
    def __init__(self):
        """We are taking extended ASCII table which consists of 256 characters as the radix value
        i.e. the integer value of an ascii character would be its corresponding index in the node
        array
        """
        self.radix = 256
        self.root = self.Node(self.radix)
        self.key_count = 0

    def get(self, key):
        return self.get(self.root, key, 0)

    def get(self, node, key, d):
        """
        Recursive function that searches for a key in a subtrie
        :param node: Subtrie under which to search for the key
        :param key: key
        :param d: key index ibn the the current recursive call
        :return: the subtrie (or leaf node) if the key exists, null otherwise
        """
        if node is None:
            return None
        if len(key) == d:
            return node
        return self.get(node.next[ord(key[d])], key, d+1)

    def put(self, key, value):
        root = self.put(self.root, key, value, 0)
        return root

    def put(self, node, key, value, d):
        # node: Subtrie under which to insert the key value pair
        if node is None:
            node = self.Node(self.radix)
        if len(key) == d:
            node.value = value
            self.key_count += 1
            return node
        node.next[ord(key[d])] = self.put(node.next[ord(key[d])], key, value, d+1)
        return node

    def contains(self, key):
        if self.get(key) is None:
            return False
        else:
            return True

    def is_empty(self):
        return self.size() == 0

    @property
    def keys(self):
        """Returns all the keys in the symbol table"""
        return self.keys_with_prefix("")

    def size(self):
        return self.key_count

    def delete(self, key):
        """Removes a key and its associated value"""
        self.root = self.delete(self.root, key, 0)

    def delete(self, node, key, key_curr_index):
        if node is None:
            return None
        if key_curr_index == len(key):
            node.value = None
        else:
            node.next[ord(key[key_curr_index])] = self.delete(node.next[ord(key[key_curr_index])], key, key_curr_index+1)
        if node.value is not None:
            return node
        for i in range(self.radix):
            if node.next[i] is not None:
                return node
        return None

    def keys_with_prefix(self, prefix):
        """Returns all the keys that start with a specific prefix"""
        queue = []
        self.collect_keys(self.get(self.root, prefix, 0), prefix, queue)
        return queue

    def longest_prefix_of(self, str_input):
        """Returns the longest key that is a prefix of input"""
        return self.search(self.root, str_input, 0, 0)

    def search(self, node, str_input, key_curr_index, length):
        """
        Recursive function that returns length of the key that is the longest prefix of str_input
        :param node: The subtrie under which to search the key
        :param str_input: The string input for which we need to search the key in trie that is the longest prefix
        :param key_curr_index: The character index in str_input at which the current recursive call is (starting from 0)
        :param length: The length of the key that is the longest prefix of str_input (starts with 0)
        :return: The length of the key that is the longest prefix of str_input
        """
        if node is None:
            return length
        if node.value is not None:
            length = key_curr_index
        if key_curr_index == length:
            return length
        return self.search(node.next[ord(str_input[key_curr_index])], key_curr_index+1, length)

    def collect_keys(self, node, key, queue):
        if node is None:
            return None
        if node.value is not None:
            queue.append(key)
        for i in range(self.radix):
            self.collect_keys(node.next[i], key+chr(i), queue)

    class Node:
        def __init__(self, radix):
            self.value = None
            self.next = [None for i in range(radix)]

