#include <iostream>
#include <iomanip>
#include <chrono>

int main() {
    const int iterations = 200000000;
    double result = 1.0;
    int k = 4; // 4 * i for i = 1

    auto start = std::chrono::high_resolution_clock::now();

    for (int i = 1; i <= iterations; ++i) {
        result -= 1.0 / (k - 1);
        result += 1.0 / (k + 1);
        k += 4;
    }

    result *= 4.0;

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;

    std::cout << std::fixed << std::setprecision(12) << "Result: " << result << "\n";
    std::cout << std::fixed << std::setprecision(6) << "Execution Time: " << elapsed.count() << " seconds\n";

    return 0;
}
