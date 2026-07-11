#include <iostream>
#include <vector>
#include <cmath>

std::vector<int> sieveOfEratosthenes(int n) {
    std::vector<bool> isPrime(n + 1, true);
    isPrime[0] = isPrime[1] = false;

    for (int i = 2; i <= std::sqrt(n); ++i) {
        if (isPrime[i]) {
            for (int j = i * i; j <= n; j += i) {
                isPrime[j] = false;
            }
        }
    }

    std::vector<int> primes;
    for (int i = 2; i <= n; ++i) {
        if (isPrime[i]) {
            primes.push_back(i);
        }
    }

    return primes;
}

int main() {
    int limit = 100;
    std::vector<int> primes = sieveOfEratosthenes(limit);

    std::cout << "Prime numbers up to " << limit << ": ";
    for (int prime : primes) {
        std::cout << prime << " ";
    }
    std::cout << std::endl;

    return 0;
}