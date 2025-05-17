import random

generated_ids = set()


def generate_unique_id():
    if len(generated_ids) >= 10000:
        raise Exception("Всі ID заняті!")

    new_id = random.randint(0, 9999)
    while new_id in generated_ids:
        new_id = random.randint(0, 9999)

    generated_ids.add(new_id)
    return new_id
