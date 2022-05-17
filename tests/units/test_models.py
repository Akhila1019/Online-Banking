from models import Credentials,Registration

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password_hashed, authenticated, and active fields are defined correctly
    """
    user = Credentials('sruthi', 'sru123')
    assert user.username == 'sruthi'
    assert user.pwdhash != 'sru123'
    assert user.is_authenticated
    assert user.is_active
    assert not user.is_anonymous


# def test_new_user_with_fixture(new_user):
#     """
#     GIVEN a User model
#     WHEN a new User is created
#     THEN check the email and password_hashed fields are defined correctly
#     """
#     assert new_user.username == 'sruthi'
#     assert new_user.pwdhash != 'sru123'


def test_setting_password():
    """
    GIVEN an existing User
    WHEN the password for the user is set
    THEN check the password is stored correctly and not as plaintext
    """
    new_user = Credentials('sruthi', 'sru123')
    new_user.set_password('thi234')
    assert new_user.pwdhash != 'thi234'
    assert new_user.is_password_correct('thi234')
    assert not new_user.is_password_correct('thi23')
    assert not new_user.is_password_correct('sru123')


# def test_user_id(new_user):
#     """
#     GIVEN an existing User
#     WHEN the ID of the user is defined to a value
#     THEN check the user ID returns a string (and not an integer) as needed by Flask-WTF
#     """
#     new_user.id = 17
#     assert isinstance(new_user.get_id(), str)
#     assert not isinstance(new_user.get_id(), int)
#     assert new_user.get_id() == '17'