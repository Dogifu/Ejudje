//
//  main.cpp
//  блок
//
//  Created by user on 21.11.2023.
//

#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int n, p, b, b_max, cur_unix;

    try {
        std::cin >> n >> p >> b >> b_max >> cur_unix;
    } catch (const std::exception& e) {
        return 1;
    }

    std::vector<int> tries;

    int failure;
    while (std::cin >> failure) {
        if (failure >= cur_unix - 2 * b_max) {
            tries.push_back(failure);
        }
    }

    std::sort(tries.begin(), tries.end());

    int b_min = b;
    int b_cur = b_min;
    bool blocked_before = false;
    int block_start = 0;
    int try_num = 0;

    while (try_num + n <= tries.size()) {
        if (tries[try_num + n - 1] - tries[try_num] >= p) {
            try_num++;
            continue;
        }

        if (blocked_before) {
            b_cur *= 2;
            b_cur = std::min(b_max, b_cur);
        }

        try_num += n;
        block_start = tries[try_num - 1];
        blocked_before = true;
    }

    if (block_start + b_cur < cur_unix || !blocked_before) {
        std::cout << "ok" << std::endl;
    } else {
        std::cout << block_start + b_cur << std::endl;
    }

    return 0;
}
