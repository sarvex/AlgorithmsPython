import sys


class Letter:
    def __init__(self, letter, freq):
        self.letter = letter
        self.freq = freq
        self.bitstring = {}

    def __repr__(self):
        return f"{self.letter}:{self.freq}"


class TreeNode:
    def __init__(self, freq, left, right):
        self.freq = freq
        self.left = left
        self.right = right


def parse_file(file_path):
    """
    Read the file and build a dict of all letters and their
    frequencies, then convert the dict into a list of Letters.
    """
    chars = {}
    with open(file_path) as f:
        while True:
            if c := f.read(1):
                chars[c] = chars[c] + 1 if c in chars else 1
            else:
                break
    return sorted((Letter(c, f) for c, f in chars.items()), key=lambda l: l.freq)


def build_tree(letters):
    """
    Run through the list of Letters and build the min heap
    for the Huffman Tree.
    """
    while len(letters) > 1:
        left = letters.pop(0)
        right = letters.pop(0)
        total_freq = left.freq + right.freq
        node = TreeNode(total_freq, left, right)
        letters.append(node)
        letters.sort(key=lambda l: l.freq)
    return letters[0]


def traverse_tree(root, bitstring):
    """
    Recursively traverse the Huffman Tree to set each
    Letter's bitstring dictionary, and return the list of Letters
    """
    if type(root) is Letter:
        root.bitstring[root.letter] = bitstring
        return [root]
    letters = []
    letters += traverse_tree(root.left, f"{bitstring}0")
    letters += traverse_tree(root.right, f"{bitstring}1")
    return letters


def huffman(file_path):
    """
    Parse the file, build the tree, then run through the file
    again, using the letters dictionary to find and print out the
    bitstring for each letter.
    """
    letters_list = parse_file(file_path)
    root = build_tree(letters_list)
    letters = {
        k: v for letter in traverse_tree(root, "") for k, v in letter.bitstring.items()
    }
    print(f"Huffman Coding  of {file_path}: ")
    with open(file_path) as f:
        while True:
            if c := f.read(1):
                print(letters[c], end=" ")
            else:
                break
    print()


if __name__ == "__main__":
    # pass the file path to the huffman function
    huffman(sys.argv[1])
