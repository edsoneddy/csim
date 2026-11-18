# EZREQUIEL NOCOLAS CHIPANA PACO 
# tarea 1

def SP(l):
    s=[]
    for i in range(len(l)):
        for j in range(i+1,len(l)):
            s.append(l[i]+l[j])
    return s

def CD(l,x):
    c=0
    for i in l:
        if i!=0 and i!=x and x%i==0:
            c+=1
    return c

l=list(map(int,input().split()))

s=SP(l)
print(*s,sep=', ')

d=[CD(l,x) for x in s]
print(*d,sep=', ')