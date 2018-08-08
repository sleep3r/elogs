from collections import defaultdict


class DeepDict(defaultdict):
    def __init__(self, d=None):
        defaultdict.__init__(self, DeepDict)
        if d is not None:
            self.from_dict(d)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def from_dict(self, d):
        for k, v in d.items():
            self[k] = DeepDict()
            if not type(v) == dict:
                self[k] = v
            else:
                self[k] = DeepDict(v)
                # self[k] = self[k].from_dict(v)

        return self

    def merge(self, target):
        for k, v in target.items():
            if isinstance(target[k], DeepDict):
                if isinstance(self[k], DeepDict):
                    self[k].merge(target[k])
                else:
                    self[k] = DeepDict()
                    self.merge(target[k])
            else:
                self[k] = target[k]

    def clear_empty(self):
        for k, v in list(self.items()):
            if isinstance(v, DeepDict):
                v.clear_empty()
                if len(v) == 0:
                    del self[k]

        return self

    def get_dict(self):
        res = {}
        for k, v in self.items():
            if type(v) == DeepDict:
                res[k] = v.get_dict()
            else:
                res[k] = v

        return res