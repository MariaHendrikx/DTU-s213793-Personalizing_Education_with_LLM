class TreeNode:
    def __init__(self, word):
        self.word = word
        self.children = []

def insert_children(node, children_data):
    for child_data in children_data:
        child_node = TreeNode(child_data['word'])
        node.children.append(child_node)
        if 'children' in child_data:
            insert_children(child_node, child_data['children'])

def build_tree(data):
    root = TreeNode(data['word'])
    if 'children' in data:
        insert_children(root, data['children'])
    return root

def print_tree(node, level=0):
    print(' ' * 4 * level + '->', node.word)
    for child in node.children:
        print_tree(child, level + 1)


# JSON Data
data = {} # Replace with the JSON data

# Building the tree
root = build_tree(data)
# Printing the tree
print_tree(root)
