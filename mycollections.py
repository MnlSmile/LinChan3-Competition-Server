class BiMapNotABijectionError(Exception): pass

class BiMap:
    def __init__(self, d:dict|None=None):
        """
        Creates a map in both directions.

        d: dict | None = None  

            Initialize via a dict obj.
            Receives a bijection.
        """
        self.forward_map = {}
        self.backward_map = {}
        if d is not None:
            self.merge(d)
    def merge(self, d:dict):
        for k, v in d.items():
            self.add(k, v)
    def add(self, k, v):
        if k in self.forward_map or v in self.backward_map:
            raise BiMapNotABijectionError('Must be a bijection')
        else:
            self.forward_map[k] = v
            self.backward_map[v] = k
    def __getitem__(self, kov):
        if isinstance(kov, slice):
            if kov.start == ...:
                if kov.stop == ...:
                    raise IndexError('Slice must keep one end a value')
                else:
                    return self.backward_map[kov.stop]
            else:
                if kov.stop != ...:
                    raise IndexError('Slice must keep one end a "..."')
                else:
                    return self.forward_map[kov.start]
        else:
            if kov in self.forward_map:
                return self.forward_map[kov]
            elif kov in self.backward_map:
                return self.backward_map[kov]
            else:
                raise IndexError(kov)
    def __delitem__(self, kov):
        if isinstance(kov, slice):
            if kov.start == ...:
                if kov.stop == ...:
                    raise IndexError('Slice must keep one end a value')
                else:
                    v = kov.stop
                    k = self.backward_map.pop(v)
                    del self.forward_map[k]
            else:
                if kov.stop != ...:
                    raise IndexError('Slice must keep one end a "..."')
                else:
                    k = kov.start
                    v = self.forward_map.pop(k)
                    del self.backward_map[v]
        else:
            if kov in self.forward_map:
                v = self.forward_map[kov]
                del self.forward_map[kov]
                del self.backward_map[v]
            elif kov in self.backward_map:
                v = self.backward_map[kov]
                del self.backward_map[kov]
                del self.forward_map[v]
            else:
                raise IndexError(kov)
    def __setitem__(self, k, v):
        if k in self.forward_map:
            del self[k]
        if v in self.backward_map:
            del self[v]
        self.add(k, v)
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([repr(k) + ' <-> ' + repr(v) for k, v in self.forward_map.items()])})"
    def __len__(self):
        return len(self.forward_map)
    def __contains__(self, kov):
        return kov in self.forward_map or kov in self.backward_map
    def __iter__(self):
        return self.forward_map
    def items(self) -> list[tuple]:
        return self.forward_map.items()

d = {1: 'a', 2: 'b'}

bm = BiMap()
bm.merge(d)
print(bm)
print(bm[...: 'b'])
print(bm[1: ...])
print(bm[1])
print(bm['b'])
del bm[1]