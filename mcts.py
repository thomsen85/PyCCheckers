class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.data = [0, 0]
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def backpropegate(self, updater):
        self.data[0] += updater[0]
        self.data[1] += updater[1]

        if not self.is_root:
            self.parent.backpropegate(updater)

    def __eq__(self, obj):
        return self.name == obj

    def __str__(self):
        return f"{self.name}: {self.data}"

    @property
    def is_root(self):
        return self.parent is None


class Tree:
    """A class for managing nodes"""

    def __init__(self, root_node):
        self.root_node = root_node

    def add_game(self, moves, won):
        backprop_data = (1, 1) if won else (0, 1)

        parent = self.root_node
        new_branch = False
        for move in moves:
            # self.move_in_children(move, parent.children)
            if self.move_in_children(move, parent.children) and not new_branch:
                parent = parent.children[parent.children.index(move)]
            else:
                new_branch = True
                new_parent = Node(move, parent)
                parent.add_child(new_parent)
                parent = new_parent

        parent.backpropegate(backprop_data)

    def move_in_children(self, move, children):
        for child in children:
            if child == move:
                return True

        return False

    def get_visualization(self, parent, wanted_depth, depth=1):
        string = ""
        if parent.is_root or True:
            string = str(parent)

        if len(parent.children) == 0 or depth > wanted_depth:
            return str(parent)

        for child in parent.children:
            string += (
                "\n"
                + "\t" * depth
                + "- "
                + self.get_visualization(child, wanted_depth, depth + 1)
            )

        return string


if __name__ == "__main__":
    print("----- Tree and Node Tester -----")
    root_node = Node("Start")
    tree = Tree(root_node)
    #
    game1 = [(13, 3, 14, 4), (13, 14, 14, 13)]
    game2 = [(13, 3, 12, 4)]
    game3 = [(13, 3, 14, 4), (13, 14, 12, 13)]
    tree.add_game(game1, True)
    tree.add_game(game2, False)
    tree.add_game(game3, False)

    print(tree.get_visualization(root_node))
