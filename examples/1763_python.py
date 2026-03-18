code_a = """
import sys
from antlr4 import InputStream, CommonTokenStream
from csim.python.PythonLexer import PythonLexer
a = [1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0]
n=int(input())
def np(n):# np numero primo
    for j in range(2,int(n**(1/2))+1):
        if n%j==0 and n!=j:
            return False
    return True
for p in range(n):
    s = int(input())
    pw = False
    for j in range(1000):
        h = s * (2 ** j) + 1
        if np(h):
            print(h)
            pw = True
            break
    if pw == False:
        print('-1')
"""
code_b = """
def primo(n):
    for i in range(2,int(n**(1/2))+1):
        if n%i==0 and n!=i:
            return False
            break
    return True

n=int(input())
for i in range(n):
    k=int(input())
    sw=False
    for j in range(1000):
        m=k*(2**j)+1
        if primo(m):
            print(m)
            sw=True
            break
    if sw==False:
        print('-1')
"""

from csim import Compare

similarity_index = Compare(code_a, code_b)
print(similarity_index)
