
from vector import Vector

vector = Vector(2)
vector2 = Vector(2)
vector.load_from_list([1,1])

print(Vector.__doc__)
print(vector2)
print(vector)

#contain method
if 1 in vector:
    print("1 is present")
if 2 not in vector:
    print("2 is not present")

# length: how many elements vector contains
print(len(vector2))

#length of vector (mathematical)
print(vector.length())

#vector multiplication
vector =  2.5 * vector
vector = vector * (-1)
print(vector)

#adding two vectors
vector2 = vector2 + vector
print(vector2)

#access to 2nd coordinate
print(vector2[2])

#sum of elements
print(vector.sum())

#vector product
print(vector.dot_product(vector2))
