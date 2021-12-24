"""AuthHeaderDriver Module."""

from ...contracts import AuthContract
from ...drivers import BaseDriver
from ...app import App


class AuthHeaderDriver(BaseDriver, AuthContract):
    def __init__(self, app: App):
        """AuthHeaderDriver initializer.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.
        """
        self.app = app

    def user(self, auth_model):
        """Gets the user based on this driver implementation

        Arguments:
            auth_model {orator.orm.Model} -- An Orator ORM type object.

        Returns:
            Model|bool
        """
        request = self.app.make("Request")
        token = request.header("Authorization").split(" ")[1]

        if token and auth_model:
            return (
                auth_model.where(
                    "remember_token", token
                ).first()
                or False
            )

        return False

    def save(self, *args, **kwargs):
        """Saves the cookie to some state.

        In this case the state is saving to a cookie.

        Arguments:
            remember_token {string} -- A token containing the state.

        Returns:
            bool
        """
        return True

    def delete(self):
        """Deletes the state depending on the implementation of this driver.

        Returns:
            bool
        """
        return True

    def logout(self):
        """Deletes the state depending on the implementation of this driver.

        Returns:
            bool
        """
        self.delete()
        self.app.make("Request").reset_user()
