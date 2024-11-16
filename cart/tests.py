def count_bidon(em, v):
    count = 0
    ob = 0
    for e in em:
        if ob + e > v:
            count += 1
            ob = 0
        ob += e

    return count if ob == 0 else count + 1

print(count_bidon([1, 3, 2, 4, 10, 8, 4 ,2 , 5, 3], 12))
