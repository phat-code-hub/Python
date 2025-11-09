a= [1,2,5,1,2,3,4,2,4,1]
b= []
cnt=0
while cnt<6:
    print(cnt,a[cnt]+1)
    b.append(a[cnt]+1)
    cnt+=1
print(b)