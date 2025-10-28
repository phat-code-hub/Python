def f2(X):
    def f3():
        return X
    return f3
fun4 = f2(5)
print(fun4())