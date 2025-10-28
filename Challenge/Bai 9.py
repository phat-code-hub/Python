import bisect
students = [(5,"ben"),(20,"Sam")]
bisect.insort(students,(25,"Bob"))
print(students)
bisect.insort(students,(1,"Tom"))
print(students[0][1])