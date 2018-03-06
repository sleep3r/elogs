from collections import defaultdict

import django
print(django.VERSION)


class deep_dict(defaultdict):
    def __init__(self, d=None):
        defaultdict.__init__(self, deep_dict)
        if d is not None:
            self.from_dict(d)

    def from_dict(self, d):
        for k, v in d.items():
            self[k] = deep_dict()
            if not type(v) == dict:
                self[k] = v
            else:
                self[k] = deep_dict(v)
                # self[k] = self[k].from_dict(v)

        return self

    def merge(self, target):
        for k, v in target.items():
            if isinstance(target[k], deep_dict):
                if isinstance(self[k], deep_dict):
                    self[k].merge(target[k])
                else:
                    self[k] = deep_dict()
                    self.merge(target[k])
            else:
                self[k] = target[k]

    def clear_empty(self):
        for k, v in list(self.items()):
            if isinstance(v, deep_dict):
                v.clear_empty()
                if len(v) == 0:
                    del self[k]

        return self

    def get_dict(self):
        res = {}
        for k, v in self.items():
            if type(v) == deep_dict:
                res[k] = v.get_dict()
            else:
                res[k] = v

        return res