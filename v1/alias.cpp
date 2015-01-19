// my first program in C++
#include <iostream>
#include <stack>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

double probability[1326];
int alias[1326];
double pdf[1326];
int length;

void generate_alias(double pdf[], int l) 
{
    length = l;
    double probabilities[length];

    double average = 1.0 / length;
    memcpy(probabilities, pdf, length*(sizeof(double)));
    memcpy(probability, pdf, length*(sizeof(double)));
    srand(time(NULL));

    std::stack<int> small;
    std::stack<int> large;

    int i;
    for (i = 0; i < length; i++) {
        if (probabilities[i] >= average) {
            large.push(i);
        } else {
            small.push(i);
        }
    }

    while (!small.empty() && !large.empty()) {
        int less = small.top();
        small.pop();
        int more = large.top();
        large.pop();

        probability[less] = probabilities[less] * length;
        alias[less] = more;

        probabilities[more] = probabilities[more] + probabilities[less] - average;
        if (probabilities[more] >= 1.0 / length) {
            large.push(more);
        } else {
            small.push(more);
        }
    }

    while (!small.empty()) {
        probability[small.top()] = 1.0;
        small.pop();
    }
    while (!large.empty()) {
        probability[large.top()] = 1.0;
        large.pop();
    }
    printf("Generated alias table.\n");
}

int next() {
    int column = rand() % length;
    bool coinToss = (rand() / (double) RAND_MAX) < probability[column];
    return coinToss ? column : alias[column];
}

int main()
{
    double pdf[4] = {0.49, 0.05, 0.21, 0.25};
    int results[4];
    generate_alias(pdf, 4);
    printf("Generated alias table.\n");
    for (int i = 0; i < 10000; i++) {
        int nxt = next();
        printf("%d\n", nxt);
        results[nxt]++;
    }

    printf("Results: 0 - %.2f 1 - %.2f 2 - %.2f 3 - %.2f\n", results[0] / 10000.0, results[1] / 10000.0, results[2] / 10000.0, results[3] / 10000.0); 
}
