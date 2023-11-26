//
//  main.cpp
//  ФИЛЬТР БЛУМА
//
//  Created by user on 21.11.2023.
//


#include <iostream>
#include <vector>
#include <cmath>
#include <sstream>
#include <stdexcept>

class BloomFilter
{
private:
    std::vector<bool> bitArray;
    unsigned long long size;
    unsigned long long numHashFunctions;
    bool isSet;

    static const unsigned long long MERSENNE_PRIME = 2147483647;

    static unsigned long long getNthPrime(unsigned long long n)
    {
        if (n <= 0)
            return 0;
        if (n == 1)
            return 2;

        unsigned long long count = 1;
        unsigned long long num = 3;

        while (count < n)
        {
            bool isPrime = true;

            for (unsigned long long i = 2; i <= static_cast<unsigned long long>(sqrt(num)); ++i)
            {
                if (num % i == 0)
                {
                    isPrime = false;
                    break;
                }
            }

            if (isPrime)
            {
                count++;
            }

            if (count < n)
            {
                num += 2;
            }
        }

        return num;
    }

    unsigned long long hashFunction(unsigned long long i, unsigned long long key) const
    {
        unsigned long long prime = getNthPrime(i + 1);
        return static_cast<unsigned long long>((((i + 1) * key + prime) % MERSENNE_PRIME) % size);
    }

public:
    BloomFilter() : size(0), numHashFunctions(0), isSet(false) {}

    bool set(float n, double P, float &outSize, float &outNumHashFunctions)
    {
        if (isSet || n == 0 || P >= 1 || P <= 0)
        {
            outSize = 0;
            outNumHashFunctions = 0;
            return false;
        }

        size = static_cast<double>(std::round(-n * log2(P) / log(2)));
        numHashFunctions = static_cast<double>(std::round(-log2(P)));

        if (size == 0 || numHashFunctions == 0)
        {
            outSize = 0;
            outNumHashFunctions = 0;
            return false;
        }

        bitArray = std::vector<bool>(size, false);
        isSet = true;

        outSize = size;
        outNumHashFunctions = numHashFunctions;
        return true;
    }

    bool add(long long key)
    {
        if (!isSet || key < 0)
        {
            throw std::runtime_error("Structure is not initialized or invalid input");
        }

        for (unsigned long long i = 0; i < numHashFunctions; ++i)
        {
            if (key < 0)
            {
                throw std::runtime_error("Invalid input: negative key");
            }

            unsigned long long index = hashFunction(i, key);
            bitArray[index] = true;
        }

        return true;
    }

    bool search(long long key) const
    {
        if (!isSet || key < 0)
        {
            throw std::runtime_error("Structure is not initialized or invalid input");
        }

        for (unsigned long long i = 0; i < numHashFunctions; ++i)
        {
            if (key < 0)
            {
                throw std::runtime_error("Invalid input: negative key");
            }

            unsigned long long index = hashFunction(i, key);
            if (!bitArray[index])
            {
                return false;
            }
        }
        return true;
    }
    std::string print() const
    {
        if (!isSet)
        {
            return "";
        }

        std::string result;
        for (bool bit : bitArray)
        {
            result += (bit ? "1" : "0");
        }
        return result;
    }
};

int main()
{
    BloomFilter bloomFilter;

    float m, k;

    std::string command;
    while (std::getline(std::cin, command))
    {
        if (command.empty())
        {
            continue;
        }

        if (command.front() == ' ' || command.back() == ' ')
        {
            std::cout << "error" << std::endl;
            continue;
        }

        std::istringstream iss(command);
        std::string cmd;
        iss >> cmd;

        try
        {
            if (cmd == "set")
            {
                float n;
                double P;
                if (iss >> n >> P && iss.eof())
                {
                    if (bloomFilter.set(n, P, m, k))
                    {
                        std::cout << m << " " << k << std::endl;
                    }
                    else
                    {
                        std::cout << "error" << std::endl;
                    }
                }
                else
                {
                    throw std::runtime_error("Invalid input");
                }
            }
            else if (cmd == "add")
            {
                float key;
                char nextChar;

                if (iss >> key && iss.eof() && !iss.get(nextChar))
                {
                    if (command.find("-0") != std::string::npos)
                    {
                        std::cout << "error" << std::endl;
                    }
                    else
                    {
                        try
                        {
                            bloomFilter.add(key);
                        }
                        catch (const std::exception &e)
                        {
                            std::cout << "error" << std::endl;
                        }
                    }
                }
                else
                {
                    throw std::runtime_error("Invalid input");
                }
            }
            else if (cmd == "search")
            {
                float key;
                if (iss >> key && iss.eof())
                {
                    if (command.find("-0") != std::string::npos)
                    {
                        std::cout << "error" << std::endl;
                    }
                    else
                    {
                        try
                        {
                            bool searchResult = bloomFilter.search(key);
                            std::cout << (searchResult ? "1" : "0") << std::endl;
                        }
                        catch (const std::exception &e)
                        {
                            std::cout << "error" << std::endl;
                        }
                    }
                }
                else
                {
                    throw std::runtime_error("Invalid input");
                }
            }
            else if (cmd == "print" && iss.eof())
            {
                std::string result = bloomFilter.print();
                if (result == "")
                {
                    std::cout << "error" << std::endl;
                }
                else
                {
                    std::cout << result << std::endl;
                }
            }
            else
            {
                throw std::runtime_error("Invalid command");
            }
        }
        catch (const std::exception &e)
        {
            std::cout << "error" << std::endl;
        }
    }

    return 0;
}
