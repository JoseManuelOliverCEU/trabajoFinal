from app.models import User

def test_user_password_hash_and_verify():
    u = User(username="pepe", role="user")
    u.set_password("Password123!")

    # No debe guardarse en claro
    assert u.password_hash != "Password123!"
    assert isinstance(u.password_hash, str)
    assert len(u.password_hash) > 20

    # Debe verificar bien
    assert u.check_password("Password123!") is True
    assert u.check_password("bad") is False

def test_is_admin_flag():
    admin = User(username="admin", role="admin")
    user = User(username="user", role="user")
    assert admin.is_admin() is True
    assert user.is_admin() is False