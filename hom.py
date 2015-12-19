import __builtin__
import operator


class list(__builtin__.list):
    def select(self, where=True, op=operator.eq):
        return _Select(self, where, op)

    def collect(self):
        return _Collect(self)

    def do(self):
        return _Do(self)

    def reduce(self):
        return _Reduce(self)

    def each(self, function):
        if len(self) == 0:
            raise EmptyListError(".each() Called on empty list")
        return list([function(i) for i in self])


def select(seq, where=True, op=operator.eq):
    return _Select(seq, where, op)


def collect(seq):
    return _Collect(seq)


def do(seq):
    return _Do(seq)


def reduce(seq):
    return _Reduce(seq)


def each(seq, function):
    return list(seq).each(function)


class EmptyListError(Exception):
    pass


class _HOMProxy(object):
    def __init__(self, seq):
        self._seq = seq
        self._keys = []

    def __getattr__(self, key):
        self._keys.append(key)
        return self


class _Select(_HOMProxy):
    def __init__(self, seq, where, op):
        super(_Select, self).__init__(seq)
        self._where = where
        self._op = op

    def __call__(self, *args, **kwargs):
        if len(self._seq) == 0:
            raise EmptyListError("HOM called on empty list")
        result = list()
        append = result.append
        call = None
        keys = self._keys
        op = self._op
        where = self._where
        for i in self._seq:
            target = i
            for key in keys:
                target = getattr(target, key)
            if call is None:
                call = callable(target)
            if call:
                if op(target(*args, **kwargs), where):
                    append(i)
            elif op(target, where):
                append(i)
        return result


class _Collect(_HOMProxy):
    def __call__(self, *args, **kwargs):
        if len(self._seq) == 0:
            raise EmptyListError("HOM called on empty list")
        result = list()
        append = result.append
        call = None
        keys = self._keys
        for target in self._seq:
            for key in keys:
                target = getattr(target, key)
            if call is None:
                call = callable(target)
            if call:
                append(target(*args, **kwargs))
            else:
                append(target)
        return result


class _Do(_HOMProxy):
    def __call__(self, *args, **kwargs):
        if len(self._seq) == 0:
            raise EmptyListError("HOM called on empty list")
        keys = self._keys
        for target in self._seq:
            for key in keys:
                target = getattr(target, key)
            target(*args, **kwargs)
        return list(self._seq)


class _Reduce(_HOMProxy):
    def __call__(self):
        if len(self._seq) == 0:
            raise EmptyListError("HOM called on empty list")
        result = self._seq[0]
        keys = self._keys
        for i in self._seq[1:]:
            target = result
            for key in keys:
                target = getattr(target, key)
            result = target(i)
        return result
