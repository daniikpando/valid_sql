import abc
# from itertools import chain, imap


class NodeAbstract(abc.ABC):
    """
    Abstract interface to implement for nodes
    """

    @abc.abstractmethod
    def add_node(self, node):
        raise NotImplementedError


class Node(NodeAbstract):
    POSSIBLE_NEAR_PARENT = []
    # POSSIBLE_NEAR_CHILDS = []

    def __init__(self, content=None) -> None:
        self.content = content
        self.childrens = []
        self.parent = None


    # def __str__(self) -> str:
    #     query = ''
    #     visited = set()
    #     def dfs(visited, graph, node, acc):
    #         if node not in visited:
    #             visited.add(node)
    #             acc += f'{node.KEY} {node.content} '
    #             for neighbour in node.childrens:
    #                 dfs(visited, graph, neighbour, acc)
    #         return acc

    #     return dfs(visited, self.childrens, self, query)

    # def __iter__(self):
    #     "implement the iterator protocol"
    #     for v in chain(*imap(iter, self.children)):
    #         yield v
    #     yield self.value

    def add_node(self, node):
        node.parent = self
        self.childrens.append(node)

    def validate_content(self) -> bool:
        return True

    def validate_tree(self):
        visited = set()
        nonvisited = set(self)
        errors = []
        nonvisited.update(self.childrens)
        while nonvisited:
            item = nonvisited.pop()
            # already seen
            if item in visited:
                continue
            # mark item
            visited.add(item)

            if item.POSSIBLE_NEAR_PARENT:
                valid = item.parent.__class__ in item.POSSIBLE_NEAR_PARENT
                if not valid:
                    errors.append({'current_node': item.KEY,
                                   'parent_node': item.parent.KEY})

            # add children
            nonvisited.update(item.childrens)

        return not any(errors), errors

class UpdateNode(Node):
    KEY = 'update'
    #POSSIBLE_NEAR_CHILDS = [SetUpdateNode]
    pass


class SetUpdateNode(Node):
    KEY = 'set'
    POSSIBLE_NEAR_PARENT = [UpdateNode]
    # POSSIBLE_NEAR_CHILDS = ["WhereUpdateNode"]


class WhereUpdateNode(Node):
    KEY = 'where'
    POSSIBLE_NEAR_PARENT = [SetUpdateNode]


def main():
    # good
    where = WhereUpdateNode(content="id=1")
    set_ = SetUpdateNode(content="name='dani'")
    statement = UpdateNode(content='users')
    set_.add_node(where)
    statement.add_node(set_)

    # bad
    bad_statement = UpdateNode(content='users1')
    where2 = WhereUpdateNode(content="id=1")
    bad_statement.add_node(where2)

    # bad
    bad_repeated_statement = UpdateNode(content='users2')
    where3 = WhereUpdateNode(content="id=1")
    set2 = SetUpdateNode(content="name='dani1'")
    set3 = SetUpdateNode(content="name='dani'")
    set3.add_node(where3)
    bad_repeated_statement.add_node(set3)
    bad_repeated_statement.add_node(set2)
    
    return {1: statement.validate_tree(), 
            2: bad_statement.validate_tree(),
            3: bad_repeated_statement.validate_tree()}

