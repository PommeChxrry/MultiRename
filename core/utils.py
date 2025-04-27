import random
import string

def generate_random_name(length=10):
    # Generates a random file name with letters and numbers
    allowed_chars = string.ascii_letters + string.digits
    random_name = ''.join(random.choice(allowed_chars) for _ in range(length))
    return random_name

def generate_custom_name(base_name, index=1):
    # Generates a custom name with a base name and an index
    return f"{base_name}{index}"

def check_name_conflicts(new_names, target_folder):
    pass