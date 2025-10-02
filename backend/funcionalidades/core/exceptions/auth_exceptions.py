class AuthenticationError(Exception):
    pass


class AuthorizationError(Exception):
    pass


class InvalidCredentialsError(AuthenticationError):
    pass


class RoleError(AuthorizationError):
    pass

