
class aMSNErrorWindow(object):
    """ This Interface represent an error window """
    def __init__(self, error_text, title = "aMSN Error"):
        """
        @type error_text: str
        @type title: str
        """
        raise NotImplementedError

    def set_title(self, title):
        """
        @type title: str
        """
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

class aMSNNotificationWindow(object):
    """
    This Interface represent a window used to display a notification message,
    generally when an operation has finished succesfully.
    """
    def __init__(self, notification_text, title = "aMSN Notification"):
        """
        @type notification_text: str
        @type title: str
        """
        raise NotImplementedError

    def set_title(self, title):
        """
        @type title: str
        """
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

class aMSNDialogWindow(object):
    """
    This Interface represent a dialog window, used to ask the user
    about something to do.
    """
    def __init__(self, message, actions, title = "aMSN Dialog"):
        """
        @type message: str
        @type actions: tuple
        @param actions: A tuple containing the options between
        which the user can choose. Every option is a tuple itself, of the form (name, callback),
        where callback is the function that will be called if the option is selected.
        @type title: str
        """
        raise NotImplementedError

    def set_title(self, title):
        """
        @type title: str
        """
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

class aMSNContactInputWindow(object):
    """
    This Interface represent a window used to get a new contact.
    """
    def __init__(self, message, callback, groupviews, title = "aMSN Contact Input"):
        """
        @type message: tuple
        @param message: A tuple with the messages to be shown in the input window,
        of the form (account_string, invite_string).
        @type callback: function
        @param callback: The function that will be called when the contact info has been filled.
        The prototype is callback(email, invite_message, groups).
        @type groupviews: list
        @param groupviews: a list of L{amsn2.views.contactlistview.aMSNGroupView} of existing groups
        @type title: str
        """
        raise NotImplementedError

    def set_title(self, title):
        """
        @type title: str
        """
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

class aMSNGroupInputWindow(object):
    """
    This Interface represent a window used to get a new group.
    """
    def __init__(self, message, callback, contactviews, title = "aMSN Group Input"):
        """
        @type message: tuple
        @param message: A tuple with the messages to be shown in the input window.
        @type callback: function
        @param callback: The function that will be called when the group info has been filled.
        The prototype is callback(name_group, contacts).
        @type contactviews: list
        @param contactviews: a list of L{amsn2.views.contactlistview.aMSNContactView} of existing contacts
        @type title: str
        """
        raise NotImplementedError

    def set_title(self, title):
        """
        @type title: str
        """
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

class aMSNContactDeleteWindow(object):
    """
    This Interface represent a window used to delete a contact.
    """
    def __init__(self, message, callback, contactviews, title = "aMSN Delete Contact"):
        """
        @type message: tuple
        @param message: A tuple with the messages to be shown in the window.
        @type callback: function
        @param callback: The function that will be called when the account has been entered.
        The prototype is callback(account), where account is the email of the account to delete.
        @type contactviews: list
        @param contactviews: a list of L{amsn2.views.contactlistview.aMSNContactView} of all the contacts
        that can be removed from the AddressBook.
        @type title: str
        """
        raise NotImplementedError

    def set_title(self, title):
        """
        @type title: str
        """
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

class aMSNGroupDeleteWindow(object):
    """
    This Interface represent a window used to delete a group.
    """
    def __init__(self, message, callback, groupviews, title = "aMSN Delete Group"):
        """
        @type message: tuple
        @param message: A tuple with the messages to be shown in the window.
        @type callback: function
        @param callback: The function that will be called when the group has been entered.
        The prototype is callback(group), where group is the group name.
        @type groupviews: list
        @param groupviews: a list of L{amsn2.views.contactlistview.aMSNGroupView} of all the groups
        that can be removed from the AddressBook.
        @type title: str
        """
        raise NotImplementedError

    def set_title(self, title):
        """
        @type title: str
        """
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

