import random

def generate_unique_5_digit_number(used_numbers):
    while True:
        new_number = random.randint(10000, 99999)
        if new_number not in used_numbers:
            used_numbers.add(new_number)
            return new_number

# Example usage:
used_numbers_set = set()
for _ in range(1):
    new_number = generate_unique_5_digit_number(used_numbers_set)
    print(new_number)