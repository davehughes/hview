class Tree(object):
    def __init__(self, name):
        self.name = name
        self.child_map = {}

    def insert_item(self, path_segments, item):
        if not path_segments:
            raise ValueError("Empty path segments")

        seg_head, seg_tail = path_segments[0], path_segments[1:]
        is_leaf_insertion = len(seg_tail) == 0
        if is_leaf_insertion:
            if seg_head in self.child_map:
                raise ValueError("Attempted leaf insertion would overwrite existing item")
            self.child_map[seg_head] = Leaf(item)
            return

        child_tree = self.child_map.setdefault(seg_head, Tree(seg_head))
        child_tree.insert_item(seg_tail, item)

    def list_transformed(self):
        return {
            'name': self.name,
            'children': [v.list_transformed() for k, v in self.child_map.items()]
        }

class Leaf(object):
    def __init__(self, item):
        self.item = item

    def list_transformed(self):
        return self.item
