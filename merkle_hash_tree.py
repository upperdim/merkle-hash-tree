from hashlib import sha256


class Node:
    def __init__(self, left_node, hash, right_node):
        self.left = left_node
        self.hash = hash
        self.right = right_node


class MerkleTree:
    def hash(input_str):
        return sha256(str(input_str).encode('utf-8')).hexdigest()

    def generate_tree(datablocks):
        child_nodes = []
        for datablock in datablocks:
            child_nodes.append(Node(None, MerkleTree.hash(datablock), None))
        return MerkleTree.build_tree(child_nodes)

    def build_tree(child_nodes):
        parents = []
        while len(child_nodes) != 1:
            index = 0
            length = len(child_nodes)
            while index < length:
                left_child = child_nodes[index]
                right_child = None
                # Add duplicate if tree nodes are odd
                if (index + 1) < length:
                    right_child = child_nodes[index + 1]
                else:
                    right_child = Node(None, left_child.hash, None)
                parent_hash = MerkleTree.hash(left_child.hash + right_child.hash)
                parents.append(Node(left_child, parent_hash, right_child))
                index += 2
            child_nodes = parents
            parents = []
        return child_nodes[0]

    def print_tree(root):
        """list contents of the tree nodes level by level
           from root to leaves in reversed BFS order"""
        if not root:
            return
        if not root.left and not root.right:
            print(root.hash)
            return
        q = [root, None]
        while len(q) > 0:
            node = None
            try:
                node = q.pop(0)
            except:
                pass
            if node:
                print(node.hash)
            else:
                print('')
                if len(q) > 0:
                    q.append(None)
            if node and node.left:
                q.append(node.left)
            if node and node.right:
                q.append(node.right)
  

def test_print():
    tests = [
            ['hello', 'there', '123', 'world'],
            ['1', '2', '3'],
            [1, 2, 3],
            ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']]
    for idx, test_datablock in enumerate(tests):
        print(f'Test {idx + 1}: {test_datablock}')
        root = MerkleTree.generate_tree(test_datablock)
        MerkleTree.print_tree(root)
        print('--------------------------------')


def test_comparison():
    def check_integrity(root1, root2):
        print(('Data is genuine.' if root1.hash == root2.hash else 'Data is altered!'))
    
    # Reference and comparison data
    original_data = ['this', 'data', 'is', 'intact']
    original_tree = MerkleTree.generate_tree(original_data)
    modified_data = ['this', 'data', 'is', 'intact']
    modified_tree = MerkleTree.generate_tree(modified_data)
    check_integrity(original_tree, modified_tree)

    # Modify the comparison data
    modified_data[3] = 'MODIFIED!'
    modified_tree = MerkleTree.generate_tree(modified_data)
    check_integrity(original_tree, modified_tree)

    # Revert modifications
    modified_data[3] = 'intact'
    modified_tree = MerkleTree.generate_tree(modified_data)
    check_integrity(original_tree, modified_tree)


def main():
    # test_print()
    test_comparison()


if __name__ == '__main__':
    main()
