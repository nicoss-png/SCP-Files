import unittest

from auth import (
    EASTER_EGG_NAME,
    EASTER_EGG_PASSWORD,
    is_reptor_easter_egg,
    login_user,
    register_user,
)


class ReptorEasterEggTests(unittest.TestCase):
    def test_credentials_trigger_easter_egg_without_authenticating(self):
        self.assertTrue(is_reptor_easter_egg("  reptor tech inc.  ", EASTER_EGG_PASSWORD))
        self.assertFalse(is_reptor_easter_egg(EASTER_EGG_NAME, "wrong"))
        self.assertFalse(login_user(EASTER_EGG_NAME, EASTER_EGG_PASSWORD)[0])

    def test_account_name_is_reserved_for_registration(self):
        registered, message = register_user(
            EASTER_EGG_NAME.lower(), "different-password", "0", "Researcher", "Site-19"
        )
        self.assertFalse(registered)
        self.assertIn("RESERVED", message)


if __name__ == "__main__":
    unittest.main()
