class EmptyException(Exception):

    def __init__(self):
        Exception.__init__(self, 'Data not found')


class NoDataAccessException(Exception):

    def __init__(self,message):
        Exception.__init__(self, message)


class UserNotFound(Exception):

    def __init__(self,message):
        Exception.__init__(self, message)


class UserDisabled(Exception):

    def __init__(self,message):
        Exception.__init__(self, message)


class SessionExpired(Exception):

    def __init__(self,message):
        Exception.__init__(self, message)

class PasswordExpired(Exception):

    def __init__(self,message):
        Exception.__init__(self, message)


class LockedAccount(Exception):

    def __init__(self,message):
        Exception.__init__(self, message)


class InvalidUser(Exception):

    def __init__(self,message):
        Exception.__init__(self, message)


class ForceChangePassword(Exception):

    def __init__(self,message):
        Exception.__init__(self, message)


class PasswordNotAllowed(Exception):

    def __init__(self,message):
        Exception.__init__(self, message)


class PasswordChangeRequiredException(Exception):

    def __init__(self, data):
        Exception.__init__(self, data)

