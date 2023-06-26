#include <iostream>
#include <cmath>
using namespace std;

extern "C" {
    double square(double base) {

        return sqrt(base);
    }
}