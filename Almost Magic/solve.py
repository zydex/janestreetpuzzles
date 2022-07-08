from z3 import *
import time

def displayGrid(m,X):
    count = 0
    for i,set in enumerate([3,5,6,6,5,3]):
        if i == 0 or i == 1:
            print("      ", end="")
        elif i == 5:
            print("            ", end="")
        for i in range(count, set+count):
            if (m[X[i]].as_long() >= 10):
                print(m[X[i]], end="    ")
            else:
                print(m[X[i]], end="     ")
        print("\n\n")
        count += set

def column(matrix, i):
    """Get the column i of matrix"""
    return [matrix[j][i] for j in range(3)]

def get_diagonals(matrix):
    """Get the diagonals of matrix"""
    return ([matrix[i][i] for i in range(3)], [matrix[i][3 - i - 1] for i in range(3)])

start = time.time()

X = IntVector("X", 28)

sq1 = [0, 1, 2, 3, 4, 5, 9, 10, 11]
sq2 = [5, 6, 7, 11, 12, 13, 17, 18, 19]
sq3 = [8, 9, 10, 14, 15, 16, 20, 21, 22]
sq4 = [16, 17, 18, 22, 23, 24, 25, 26, 27]

s = Solver()

s.add(Distinct(X))
s.add([x > 0 for x in X])
s.add(Sum(X) < 1112)

def buildSquare(sq):
    built = [[X[sq[0]], X[sq[1]], X[sq[2]]],
                [X[sq[3]], X[sq[4]], X[sq[5]]],
                [X[sq[6]], X[sq[7]], X[sq[8]]]]
    return built

def genSquareRules(sq):

    sq1 = buildSquare(sq)
    d1, d2 = get_diagonals(sq1)

    for i in range(3):
        if i < 2:
            s.add(Sum(sq1[i]) - Sum(sq1[i+1]) <= 1, Sum(sq1[i]) - Sum(sq1[i+1]) >= -1)
            s.add(Sum(column(sq1, i)) - Sum(column(sq1, i+1)) <= 1, Sum(column(sq1, i)) - Sum(column(sq1, i+1)) >= -1)
        s.add(Sum(d1) - Sum(sq1[i]) <= 1, Sum(d1) - Sum(sq1[i]) >= -1)
        s.add(Sum(d2) - Sum(sq1[i]) <= 1, Sum(d2) - Sum(sq1[i]) >= -1)
        s.add(Sum(d1) - Sum(column(sq1, i)) <= 1, Sum(d1) - Sum(column(sq1, i)) >= -1)
        s.add(Sum(d2) - Sum(column(sq1, i)) <= 1, Sum(d2) - Sum(column(sq1, i)) >= -1)

    return s

s = genSquareRules(sq1)
s = genSquareRules(sq2)
s = genSquareRules(sq3)
s = genSquareRules(sq4)

# ----- borrowed from github/gowen100 ---------
# breaks symmetry of solutions
# makes it all just work and so much faster

s.add(X[10] > X[11])
s.add(X[11] > X[16])
s.add(X[16] > X[17])

s.add(X[0] > X[7])
s.add(X[7] > X[27])
s.add(X[27]> X[20]) 

while s.check() == sat:

    print("\nSolution found.\n")

    m = s.model()

    print(" ")

    tot = sum([m[X[i]].as_long() for i in range(0, 28)])

    displayGrid(m,X)

    print("Answer:", tot)

    print("\nTime taken:", time.time() - start)

    print("")

    s.add(Sum(X) < tot)

    s.check()

print("No additional solutions found.")
print("")



