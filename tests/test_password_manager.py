import pytest
from src.password_manager.manager import generate_password
from src.utils.security_analysis import analyze_password_strength

def test_generate_password():
    pwd1 = generate_password(16, use_special=True)
    assert len(pwd1) == 16
    assert any(c in "!@#$%^&*()-_+=" for c in pwd1)
    
    pwd2 = generate_password(20, use_special=False)
    assert len(pwd2) == 20
    assert not any(c in "!@#$%^&*()-_+=" for c in pwd2)

def test_password_strength():
    weak = analyze_password_strength("password")
    assert weak["score"] < 3
    assert weak["strength"] == "Weak"
    
    strong = analyze_password_strength("Str0ng!P@ssw0rd")
    assert strong["score"] >= 5
    assert strong["strength"] == "Strong"
