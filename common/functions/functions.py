
import random
import string

def generate_random_password(length):
  letters = string.ascii_letters + string.digits
  return ''.join(random.choice(letters) for i in range(length))