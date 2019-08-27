import logging
import json
import sys
import datetime
import yaml
import logging.config

with open(r"D:\Anupam_Technical\Code\PythonCode\DsAlgosPython\config\LoggingConfig.yml", 'r') as config:
    config = yaml.safe_load(config)
    logging.config.dictConfig(config)
logger = logging.getLogger(__name__)


def configure_logging():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler("SpellChecker.log")
    file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    log_format = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
    console_handler.setFormatter(log_format)
    file_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.debug("Test log")


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
        return self.__get(self.root, key, 0)

    def __get(self, node, key, d):
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
        return self.__get(node.next[ord(key[d])], key, d + 1)

    def put(self, key, value):
        root = self.__put(self.root, key, value, 0)
        return root

    def __put(self, node, key, value, d):
        # node: Subtrie under which to insert the key value pair
        if node is None:
            node = self.Node(self.radix)
        if len(key) == d:
            node.value = value
            self.key_count += 1
            return node
        node.next[ord(key[d])] = self.__put(node.next[ord(key[d])], key, value, d + 1)
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
        self.root = self.__delete(self.root, key, 0)

    def __delete(self, node, key, key_curr_index):
        if node is None:
            return None
        if key_curr_index == len(key):
            node.value = None
        else:
            node.next[ord(key[key_curr_index])] = self.__delete(node.next[ord(key[key_curr_index])], key,
                                                                key_curr_index + 1)
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
        return self.__search(self.root, str_input, 0, 0)

    def __search(self, node, str_input, key_curr_index, length):
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
        return self.__search(node.next[ord(str_input[key_curr_index])], key_curr_index + 1, length)

    def collect_keys(self, node, key, queue):
        if node is None:
            return None
        if node.value is not None:
            queue.append(key)
        for i in range(self.radix):
            self.collect_keys(node.next[i], key + chr(i), queue)

    class Node:
        def __init__(self, radix):
            self.value = None
            self.next = [None for i in range(radix)]


def main():
    file_name = sys.argv[1]
    trie = TrieST()
    logger.info("Inside  main")
    counter = 0
    start_time = datetime.datetime.now()
    for word in get_dict_words(file_name):
        trie.put(word, 1)
        counter += 1
        if counter % 5000 == 0:
            end_time = datetime.datetime.now()
            time_diff = end_time - start_time
            logger.info(
                "Time taken for inserting {} records is {} seconds".format(counter, str(time_diff.total_seconds())))
    logger.info("Inserted all dictionary words in the trie")
    val = trie.get("shore")
    logger.info("found shore")


def get_dict_words(file_name):
    with open(file_name, 'r') as words_file:
        dict_words = json.load(words_file)
    words_list = [key for (key, value) in dict_words.items()]
    return words_list


if __name__ == "__main__":
    main()
