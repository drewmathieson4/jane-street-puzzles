def sum_digits(n):
    return sum(int(digit) for digit in str(n))


seen = 0
for i in range(10000):
    if sum_digits(i) == 26:
        seen += 1
        if seen == 20:
            print(i)
            break
