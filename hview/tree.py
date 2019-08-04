class Tree(object):

    @classmethod
    def build(cls, items, adapter):
        adapter_inst = adapter()
        root = cls(adapter_inst.root_name)
        for item in items:
            hierarchy = adapter_inst.hierarchy(item)
            item_node = {
                'original': item,
                'hierarchy': hierarchy,
                'value': adapter_inst.value(item),
                'name': adapter_inst.label(item),
            }
            root.insert_item(hierarchy, item_node)
        return root.list_transformed()

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


class ItemAdapter(object):
    root_name = 'root'
    label_key = 'name'
    value_key = 'value'

    def label(self, item):
        return item[self.label_key]

    def value(self, item):
        return item[self.value_key]

    def hierarchy(self, item):
        return [self.label(item)]
