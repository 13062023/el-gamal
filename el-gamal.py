import random

# Генерація випадкового простого числа
def generate_prime_number(length):
    while True:
        p = random.randrange(2**(length-1), 2**length)
        if is_prime(p):
            return p

# Перевірка, чи число є простим
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Знаходження примітивного кореня за модулем p
def find_primitive_root(p):
    if p == 2:
        return 1
    p1 = 2
    p2 = (p - 1) // p1
    while True:
        g = random.randint(2, p - 1)
        if pow(g, p2, p) != 1 and pow(g, p1, p) != 1:
            return g

# Знаходження оберненого елемента a в полі за модулем m
def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Оберненого елемента не існує')
    return x % m

# Розширений алгоритм Евкліда
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

# Функція підписування повідомлення
def sign_message(message, p, g, a):
    # Генерація випадкового числа k
    k = random.randint(1, p - 2)

    # Обчислення першого компонента підпису
    r = pow(g, k, p)

    # Обчислення геш-значення повідомлення
    h = hash(message)

    # Обчислення другого компонента підпису
    k_inv = mod_inverse(k, p - 1)
    s = ((h - a * r) * k_inv) % (p - 1)

    return r, s

# Функція перевірки підпису
def verify_signature(message, signature, p, g, b):
    r, s = signature

    # Обчислення геш-значення повідомлення
    h = hash(message)

    # Обчислення першої складової перевірки
    y = pow(b, r, p)
    u1 = (h * mod_inverse(s, p - 1)) % (p - 1)

    # Обчислення другої складової перевірки
    u2 = (r * mod_inverse(s, p - 1)) % (p - 1)

    # Обчислення перевірочного значення
    v = (pow(g, u1, p) * pow(y, u2, p)) % p

    return v == r

# Генерація загальносистемних параметрів
p = generate_prime_number(2048)
g = find_primitive_root(p)

# Генерація особистого ключа
a = random.randint(1, p - 2)

# Обчислення відкритого ключа
b = pow(g, a, p)

# Повідомлення, яке потрібно підписати
message = 'Hello, World!'

# Підпис повідомлення
signature = sign_message(message, p, g, a)

# Перевірка підпису
is_valid = verify_signature(message, signature, p, g, b)

print('Підпис вірний:', is_valid)
