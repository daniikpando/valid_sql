import abc
# from itertools import chain, imap


class NodeAbstract(abc.ABC):
    """
    Abstract interface to implement for nodes
    """

    @abc.abstractmethod
    def add_node(self, node):
        raise NotImplementedError

    @abc.abstractmethod
    def validate_if_any_repeated_node(self):
        raise NotImplementedError

    @abc.abstractmethod
    def validate_content(self):
        raise NotImplementedError

    @abc.abstractmethod
    def validate_tree(self, node):
        raise NotImplementedError


class Node(NodeAbstract):
    POSSIBLE_NEAR_PARENT = []
    # POSSIBLE_NEAR_CHILDS = []

    def __init__(self, content=None) -> None:
        self.content = content
        self.children = []
        self.parent = None

    def __str__(self) -> str:
        query = ''
        visited = set()
        nonvisited = set([self])
        while nonvisited:
            node = nonvisited.pop()
            if node not in visited:
                visited.add(node)
                query += f'{node.KEY} {node.content} '

            nonvisited.update(node.children)

        query += ';'
        return query

    # def __iter__(self):
    #     "implement the iterator protocol"
    #     for v in chain(*imap(iter, self.children)):
    #         yield v
    #     yield self.value

    def add_node(self, node):
        # TODO: add all child nodes and add a weight to be able to order
        node.parent = self
        self.children.append(node)

    def validate_if_any_repeated_node(self):
        node_classes = [self.__class__]
        errors = []

        for child in self.children:
            child_class = child.__class__
            if child_class in node_classes:
                errors.append({'error': 'repeated_keys_not_valid',
                               'detail': {
                                   'current_node': child.KEY,
                                   'parent_node': child.parent.KEY}})
                break
            node_classes.append(child_class)

        return errors

    def validate_content(self) -> bool:
        return True

    def validate_tree(self):
        visited = set()
        nonvisited = set([self])
        errors = []
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
                    errors.append({'error': 'not_valid_SQL_structure',
                                   'detail': {
                                       'current_node': item.KEY,
                                       'parent_node': item.parent.KEY
                                   }})

            # validate if any children repeated
            err = item.validate_if_any_repeated_node()
            if err:
                errors.extend(err)
            # add children
            nonvisited.update(item.children)

        return not any(errors), errors


class UpdateNode(Node):
    KEY = 'update'
    #POSSIBLE_NEAR_CHILDS = [SetUpdateNode]


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

    print(statement)
    return {1: statement.validate_tree(),
            2: bad_statement.validate_tree(),
            3: bad_repeated_statement.validate_tree()}


if __name__ == '__main__':
    main()
