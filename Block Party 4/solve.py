from z3 import *
import numpy
import time

def taxicabDistance(p, q):
    # sum of absolute difference between coordinates
    distance = 0
    for p_i,q_i in zip(p,q):
        distance += abs(p_i - q_i)
    return distance

# initialize 2d array of z3 expressions as ints
A = [[ BitVec("a_%s_%s" % (i, j), 32) for j in range(10) ] 
      for i in range(10)]

# initialize solver
s = Solver()

start = time.time()

def getTaxicab(coord, radius):
    coordinates = []
    excluded = []
    for i in range(coord[0]-radius,coord[0]+radius+1):
        for j in range(coord[1]-radius,coord[1]+radius+1):
            if taxicabDistance(coord, (i,j)) == radius and i < 10 and j < 10 and i > -1 and j > -1 and (i,j) != coord:
                coordinates.append((i,j))
            elif taxicabDistance(coord, (i,j)) < radius and i < 10 and j < 10 and i > -1 and j > -1 and (i,j) != coord:
                excluded.append((i,j))
    return coordinates, excluded

for d in range(10):
    for e in range(10):
        for a in range(1,11):
            coordinates, excluded = getTaxicab((d,e), a)
            s.add(If(A[d][e] == a, Or([A[i][j] == A[d][e] for i,j in coordinates]), True))
            s.add(If(A[d][e] == a, And([A[i][j] != A[d][e] for i,j in excluded]), True))

s.add(Or([A[i][j] == a for a in range(1, 11) for i in range(10) for j in range(10)]))

# cluster constraints
cluster1 = [A[0][0],A[1][0],A[2][0],A[3][0],A[4][0],A[5][0],A[6][0],A[1][1],A[2][1],A[3][1]]
cluster2 = [A[0][1],A[0][2],A[0][3],A[1][2],A[1][3],A[1][4]]
cluster3 = [A[0][4],A[0][5],A[0][6],A[0][7],A[0][8],A[0][9],A[1][5],A[1][8],A[1][9]]
cluster4 = [A[1][6],A[1][7],A[2][7]]
cluster5 = [A[2][2],A[2][3],A[3][3]]
cluster6 = [A[2][4],A[2][5]]
cluster7 = [A[2][8],A[2][9],A[3][8],A[3][9],A[4][9],A[5][9],A[5][8]]
cluster8 = [A[3][2],A[4][2],A[5][2],A[4][1]]
cluster9 = [A[3][4],A[4][4],A[4][3]]
cluster10 = [A[2][6],A[3][7],A[3][6],A[3][5],A[4][7],A[4][8]]
cluster11 = [A[4][5],A[5][5]]
cluster12 = [A[5][3],A[6][3],A[6][4],A[6][5],A[7][4]]
cluster13 = [A[5][6],A[5][7],A[6][6]]
cluster14 = [A[6][9],A[6][8],A[6][7]]
cluster15 = [A[6][2],A[7][2]]
cluster16 = [A[6][1],A[7][1],A[8][1],A[9][1],A[7][0],A[8][0],A[9][0],A[9][2],A[8][2],A[9][3]]
cluster17 = [A[7][3],A[8][3],A[8][4],A[9][4],A[9][5]]
cluster18 = [A[7][7],A[8][7],A[7][8],A[8][8]]
cluster19 = [A[7][6],A[8][6],A[9][6],A[8][5],A[9][7],A[9][8],A[9][9],A[8][9],A[7][9]]

clusters = [cluster1, cluster2, cluster3, cluster4, cluster5, cluster6, cluster7, cluster8, cluster9, cluster10, cluster11, cluster12, cluster13, cluster14, cluster15, cluster16, cluster17, cluster18, cluster19]

for cluster in clusters:
    for cell in cluster:
        s.add(Or([cell == i for i in range(1, len(cluster)+1)]))
    s.add(Distinct(cluster))

# puzzle constraints + 1 cell assumption
s.add(A[0][1] == 3, A[0][5] == 7, A[1][3] == 4, A[2][8] == 2,
      A[3][3] == 1, A[4][0] == 6, A[4][2] == 1, A[5][7] == 3,
      A[5][9] == 6, A[6][6] == 2, A[7][1] == 2, A[8][6] == 6,
      A[9][4] == 5, A[9][8] == 2, A[4][6] == 1, A[5][1] == 1,
      A[5][4] == 1, A[7][5] == 1)

print("\nConstraints defined. Solving...")

while s.check() == sat:
    print("\nSolution found.")
    m = s.model()

    print(" ")

    for i in range(10):
        for j in range(10):
            if m[A[i][j]].as_long() < 10:
                print(m[A[i][j]], end="    ")
            else:
                print(m[A[i][j]], end="   ")
        print("\n")

    tot = 0

    for i in range(10):
        tot += numpy.prod([m[A[i][j]].as_long() for j in range(10)])

    print("Answer:", tot)

    print("\nTime taken:", time.time() - start)

    print("")

    s.add(Or([A[i][j] != m[A[i][j]].as_long() for i in range(10) for j in range(10)]))
    s.check()

print("No additional solutions found.")
print("")
