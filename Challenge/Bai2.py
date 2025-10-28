l = [x for x in range(1,5)]
print(l)
f= [2 if x%2 else 1 for x in l]
print(f)
n = [x*s for x,s in zip(l,f)]
print(n)

for w in reversed("HelloWorld"):
    print(w)