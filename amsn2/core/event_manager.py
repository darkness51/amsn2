class aMSNEvents:
    # ContactList events
    CONTACTVIEW_UPDATED = 0
    GROUPVIEW_UPDATED = 1
    CLVIEW_UPDATED = 2
    AMSNCONTACT_UPDATED = 3
    # PersonalInfo events
    PERSONALINFO_UPDATED = 4

class aMSNEventManager:
    def __init__(self, core):
        """
        @type core: L{amsn2.core.amsn.aMSNCore}
        """

        self._core = core
        self._events_cbs = [ [[], []] for e in dir(aMSNEvents) if e.isupper()]
        self._events_tree = [aMSNEventTree(None) for e in dir(aMSNEvents) if e.isupper()]
        self.events = aMSNEvents()

    def emit(self, event, *args):
        """ emit the event
        @type event: int defined in L{amsn2.core.event_manager.aMSNEvents}
        @type args: args 
        """
        # rw callback
        for cb in self._events_cbs[event][0]:
            #TODO: try except
            cb(*args)

        # ro callback
        for cb in self._events_cbs[event][1]:
            #TODO: try except
            cb(*args)

    def register(self, event, callback, type='ro', deps=[]):
        """
        Register a callback for an event:
            - ro callback: doesn't need to modify the view
            - rw callback: modify the view, can have dependencies which actually
              are the names of the callbacks from which it depends
        @type event: int defined in L{amsn2.core.event_manager.aMSNEvents}
        @type callback: L{amsn2.core.event_manager.aMSNEventCallback}
        @type type: str
        @type deps: list
        """
        if type is 'ro':
            self._events_cbs[event][1].append(callback)

        elif type is 'rw':
            if self._events_tree[event].insert(callback, deps):
                self._events_cbs[event][0] = self._events_tree[event].get_callbacks_sequence()
            else:
                print 'Failed adding callback '+callback.__name__+' to event '+event+': missing dependencies'

    def unregister(self, event, callback):
        """ unregister a callback for an event 
        @type event: int defined in L{amsn2.core.event_manager.aMSNEvents}
        @type callback: L{amsn2.core.event_manager.aMSNEventCallback}
        """
        if self._events_tree[event].is_listed(callback):
            self._events_tree[event].remove(callback)
            self._events_cbs[event][0] = self._events_tree.get_callbacks_sequence()
        else:
            self._events_cbs[event][1].remove(callback)




class aMSNEventCallback:
    def __init__(self, tree, callback_function, deps):
        """
        @type tree: L{amsn2.core.event_manager.aMSNEventTree}
        @type callback_function: Function
        @type deps: list
        """
        self.data = callback_function
        self.id = callback_function.__name__
        self._deps = set(deps)
        self._tree = tree

    def depends(self, cb):
        """
        @type cb: L{amsn2.core.event_manager.aMSNEventCallback}
        """
        for dep in self._deps:
            if cb.id == dep or (\
               cb._tree.right is not None and \
               cb._tree.right.is_listed(dep)):
                return True
        return False

class aMSNEventTree:
    def __init__(self, parent):
        """
        @type parent: L{amsn2.core.event_manager.aMSNEventTree}
        """
        self.parent = parent
        self.root = None
        self.left = None
        self.right = None
        self._elements = set()

    def remove(self, callback_function):
        """
        @type callback_function: Function
        """
        if self.is_listed(callback_function.__name__):
            cb_obj = self._find(callback_function.__name__)

            # keep callbacks that do not depend on the one being removed
            if cb_obj._tree.parent is not None:
                if cb_obj._tree.parent.right is cb_obj._tree:
                    cb_obj._tree.parent.right = cb_obj._tree.left
                else:
                    cb_obj._tree.parent.left = cb_obj._tree.left

            else:
                # remove the root
                self.root = self.left.root
                self.right = self.left.right
                self._elements = self.left._elements
                self.left = self.left.left

        else:
            print 'Trying to remove missing callback '+callback_function.__name__

    # FIXME: what if a dependence is not yet in the tree?
    def insert(self, callback_function, deps=[]):
        """
        @type callback_function: Function
        @type deps: list
        """
        cb_obj = aMSNEventCallback(self, callback_function, deps)
        if self.is_listed(cb_obj.id):
            self.remove(callback_function)
            print 'Trying to add already added callback '+callback_function.__name__

        deps_satisfied = [self.is_listed(dep) for dep in deps]

        # workaround if there are no dependencies
        deps_satisfied.extend([True, True])

        if reduce(lambda x, y: x and y, deps_satisfied):
            self._insert(cb_obj)
            return True
        else:
            # can't satisfy all dependencies
            return False

    def is_listed(self, item):
        """
        @type item: str
        """
        return item in self._elements

    def get_callbacks_sequence(self):
        return self._inorder([])

    def _insert(self, cb):
        """
        @type cb: L{amsn2.core.event_manager.aMSNEventCallback}
        """
        self._elements.add(cb.id)
        cb._tree = self
        if self.root is None:
            self.root = cb

        elif cb.depends(self.root):
            if self.right is None:
                self.right = aMSNEventTree(self)
            self.right._insert(cb)

        else:
            if self.left is None:
                self.left = aMSNEventTree(self)
            self.left._insert(cb)

    def _inorder(self, q):
        """
        @type q: list
        """
        if self.left is not None:
            q = self.left._inorder(q)
        q.append(self.root.data)
        if self.right is not None:
            q = self.right._inorder(q)
        return q

    def _find(self, str_id):
        """
        @type str_id: str
        """
        if self.left is not None and self.left.is_listed(str_id):
            return self.left._find(str_id)
        elif self.right is not None and self.right.is_listed(str_id):
            return self.right._find(str_id)
        elif self.root.id == str_id:
            return self.root
        else:
            return None


