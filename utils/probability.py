import random


async def oneIn(num: int = 2):
    random_number = random.randrange(1, num + 1)

    if random_number <= 1:
        return True
    else:
        return False
