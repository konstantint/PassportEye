'''
PassportEye::Util: Pipeline utility

Author: Konstantin Tretyakov
License: MIT
'''


class Pipeline(object):
    """
    The computation performed in order to extract the information from an image
    is essentially a list of steps of various complexity, where each step uses
    results of the previous steps and introduces its own results.

    Although this is nothing more than a standard sequential program, it seems to be somewhat
    more convenient sometimes to regard it as a "pipeline" consisting of pluggable "components",
    where each component explicitly specifies what inputs it needs and what outputs it produces,
    and the workflow engine wires up the inputs to the outputs.

    This class offers provides a simple implementation of such a pipeline.
    It keeps track of a dictionary of values that were already computed, a dictionary of
    "components" which know how to compute other values, and routes item accesses to computations automatically.

    >>> a = Pipeline()
    >>> a.add_component('1', lambda: 1, ['a'], [])
    >>> a.add_component('2', lambda: 2, ['b'], [])
    >>> a.add_component('s,d', lambda x,y: (x+y, x-y), ['c', 'd'], ['a', 'b'])
    >>> a.add_component('sd', lambda x,y: (x+y, x-y), ['e'], ['a', 'b'])
    >>> a['c']
    3
    >>> a['d']
    -1
    >>> a['e']
    (3, -1)
    >>> a.replace_component('1', lambda: 2, ['a'], [])
    >>> a['e']
    (4, 0)
    >>> a['d']
    0
    """

    def __init__(self):
        self.data = dict()        # Maps key -> data item.
        self.components = dict()  # Maps name -> component
        self.provides = dict()    # Component name -> provides list
        self.depends = dict()     # Component name -> depends list
        self.whoprovides = dict() # key -> component name
        self.data['__data__'] = self.data
        self.data['__pipeline__'] = self

    def add_component(self, name, callable, provides=None, depends=None):
        """
        Add a given callable to a list of components. The provides and depends are lists of strings, specifying what
        keys the component computes and what keys it requires to be present. If those are not given, the callable must
        have fields __provides__ and __depends__.
        """
        provides = provides or getattr(callable, '__provides__', [])
        depends = depends or getattr(callable, '__depends__', [])
        for p in provides:
            if p in self.whoprovides:
                raise Exception("There is already a component that provides %s" % p)
        self.provides[name] = provides
        self.depends[name] = depends
        self.components[name] = callable
        for p in provides:
            self.whoprovides[p] = name

    def remove_component(self, name):
        """Removes an existing component with a given name, invalidating all the values computed by
        the previous component."""
        if name not in self.components:
            raise Exception("No component named %s" % name)
        del self.components[name]
        del self.depends[name]
        for p in self.provides[name]:
            del self.whoprovides[p]
            self.invalidate(p)
        del self.provides[name]

    def replace_component(self, name, callable, provides=None, depends=None):
        """Changes an existing component with a given name, invalidating all the values computed by
        the previous component and its successors."""
        self.remove_component(name)
        self.add_component(name, callable, provides, depends)

    def invalidate(self, key):
        """Remove the given data item along with all items that depend on it in the graph."""
        if key not in self.data:
            return
        del self.data[key]

        # Find all components that used it and invalidate their results
        for cname in self.components:
            if key in self.depends[cname]:
                for downstream_key in self.provides[cname]:
                    self.invalidate(downstream_key)

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        self._compute(key)
        return self.data[key]

    def _compute(self, key):
        if key not in self.data:
            cname = self.whoprovides[key]
            for d in self.depends[cname]:
                self._compute(d)
            inputs = [self.data[d] for d in self.depends[cname]]
            results = self.components[cname](*inputs)
            if len(self.provides[cname]) == 1:
                self.data[self.provides[cname][0]] = results
            else:
                for k, v in zip(self.provides[cname], results):
                    self.data[k] = v

