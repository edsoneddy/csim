# generate sieve of eratosthenes up to n
def sieve_of_eratosthenes(n):
    """Generates a list of prime numbers up to n using the Sieve of Eratosthenes algorithm."""
    if n < 2:
        return []
    
    # Initialize a boolean array to track prime status of numbers
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False  # 0 and 1 are not prime numbers
    
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    
    # Collecting all prime numbers
    primes = [i for i in range(n + 1) if is_prime[i]]
    return primes

print(sieve_of_eratosthenes(30))  # Example usage: prints prime numbers up to 30