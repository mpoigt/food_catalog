from auth.infrastructure.services.hashing import PasswordHasher


def test_hash_is_not_plaintext():
    hashed = PasswordHasher().hash("secret123")
    assert hashed != "secret123"


def test_verify_accepts_correct_password():
    hasher = PasswordHasher()
    hashed = hasher.hash("secret123")
    assert hasher.verify("secret123", hashed) is True


def test_verify_rejects_wrong_password():
    hasher = PasswordHasher()
    hashed = hasher.hash("secret123")
    assert hasher.verify("wrong-password", hashed) is False


def test_same_password_yields_different_hashes():
    hasher = PasswordHasher()
    assert hasher.hash("secret123") != hasher.hash("secret123")
