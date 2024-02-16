class TreeNode:
    def __init__(self, word):
        self.word = word
        self.left = None
        self.right = None

def insert_children(node, children):
    if len(children) > 0:
        node.left = TreeNode(children[0]['word'])
        if 'children' in children[0]:
            insert_children(node.left, children[0]['children'])
    if len(children) > 1:
        node.right = TreeNode(children[1]['word'])
        if 'children' in children[1]:
            insert_children(node.right, children[1]['children'])

def build_binary_tree(data):
    root = TreeNode(data['word'])
    if 'children' in data:
        insert_children(root, data['children'])
    return root

def print_tree(node, level=0):
    if node is not None:
        print_tree(node.right, level + 1)
        print(' ' * 4 * level + '->', node.word)
        print_tree(node.left, level + 1)

# JSON Data
data = {
    "word": "Artificial Intelligence",
    "children": [
        {
            "word": "Machine Learning",
            "children": [
                {
                    "word": "Supervised Learning",
                    "children": []
                },
                {
                    "word": "Unsupervised Learning",
                    "children": []
                }
            ]
        },
        {
            "word": "Deep Learning",
            "children": [
                {
                    "word": "Neural Networks",
                    "children": []
                },
                {
                    "word": "Convolutional Neural Networks",
                    "children": []
                }
            ]
        }
    ]
}

# Building the binary tree
binary_tree_root = build_binary_tree(data)

# Printing the binary tree
print_tree(binary_tree_root)
