import operator


def select(seq, where=True, op=operator.eq):
    return _Select(seq, where, op)


def collect(seq):
    return _Collect(seq)


def do(seq):
    return _Do(seq)


class list(list):
    def select(self, where=True, op=operator.eq):
        return _Select(self, where, op)

    def collect(self):
        return _Collect(self)

    def do(self):
        return _Do(self)


class _HOMProxy(object):
    def __init__(self, seq):
        self._seq = seq
        self._keys = []

    def __getattr__(self, key):
        self._keys.append(key)
        return self

    def _call(self, obj, *args, **kwargs):
        call = obj
        for key in self._keys:
            call = getattr(call, key)
        return call(*args, **kwargs)


class _Select(_HOMProxy):
    def __init__(self, seq, where, op):
        super(_Select, self).__init__(seq)
        self._where = where
        self._op = op

    def __call__(self, *args, **kwargs):
        return list(
            [i for i in self._seq
            if self._op(self._call(i, *args, **kwargs), self._where)])


class _Collect(_HOMProxy):
    def __call__(self, *args, **kwargs):
        return list([self._call(i, *args, **kwargs) for i in self._seq])


class _Do(_HOMProxy):
    def __call__(self, *args, **kwargs):
        for i in self._seq:
            self._call(i, *args, **kwargs)
