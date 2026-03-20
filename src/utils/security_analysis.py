import hashlib
import os
import re

def analyze_password_strength(password: str) -> dict:
    """"Evaluate the strength of a given password."""
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters.")
        
    if len(password) >= 12:
        score += 1
        
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Missing lowercase letters.")
        
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Missing uppercase letters.")
        
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Missing numbers.")
        
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Missing special characters.")
        
    # Translate score to strength
    if score < 3:
        strength = "Weak"
    elif score < 5:
        strength = "Moderate"
    else:
        strength = "Strong"
        
    return {
        "score": score,
        "max_score": 6,
        "strength": strength,
        "feedback": feedback
    }

def get_file_hash(filepath: str, algo="sha256") -> str:
    """Computes the hash of a file for malware scanning or integrity checks."""
    if not os.path.exists(filepath):
        return None
    
    h = hashlib.new(algo)
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
            
    return h.hexdigest()
