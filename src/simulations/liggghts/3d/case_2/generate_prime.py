import random
import sympy

# Generar un número primo aleatorio mayor que 10,000
def generate_prime():
    while True:
        num = random.randint(10001, 20000)  # Rango ajustado para mayor eficiencia
        if sympy.isprime(num):
            return num

if __name__ == "__main__":
    prime = generate_prime()
    with open("prime_seed.txt", "w") as f:
        f.write(f"{prime}\n")  # Asegúrate de que hay una nueva línea al final

