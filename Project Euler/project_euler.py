import itertools
from fractions import gcd
import operator 
import math        

def erat2( ):
    D = {  }
    yield 2
    for q in itertools.islice(itertools.count(3), 0, None, 2):
        p = D.pop(q, None)
        if p is None:
            D[q*q] = q
            yield q
        else:
            x = p + q
            while x in D or not (x&1):
                x += p
            D[x] = p

def is_prime(n):
        for i in range(2, int(math.sqrt(abs(n)))):
            if (n%i == 0):
                return False
        return True    

def lcm(a,b):
        return (a*b)/gcd(a,b)

def no_of_divisors(n): #this is highly inefficient
    c = 0
    for i in range(1,n+1):
        if (n % i == 0):
            c = c + 1
    return c

def prob_1():
    print sum((x for x in range(1000) if x%3==0 or x%5==0))

def prob_2():
    sum_even = 0
    a , b = 0 , 1
    while (a < 90):
   	if (a % 2 == 0):
  		sum_even += a
   	a, b = b, a+b
    print sum_even

def prob_3():
    N = 13195
    max_prime = 1
    pit = erat2()
    f = pit.next()
    while(f < N):
        if(N % f == 0):
            max_prime = f
        f = pit.next()
    print max_prime            

def prob_4():
    N = 100
    print [x*y for x in range(N) for y in range(N) if (str(x*y) == str(x*y)[::-1])][-1]
    
def prob_5():
    mult = 1
    for i in range(2,11):
        mult = lcm(mult,i)
    print mult

def prob_6():
    N = 100
    ss = sum((x*x for x in range(N+1)))
    sqs = sum(range(N+1))**2
    print sqs-ss
    
def prob_7():
    pit = erat2()
    print [pit.next() for x in range(10001)][-1]    

def prob_8():
    strN = """73167176531330624919225119674426574742355349194934
96983520312774506326239578318016984801869478851843
85861560789112949495459501737958331952853208805511
12540698747158523863050715693290963295227443043557
66896648950445244523161731856403098711121722383113
62229893423380308135336276614282806444486645238749
30358907296290491560440772390713810515859307960866
70172427121883998797908792274921901699720888093776
65727333001053367881220235421809751254540594752243
52584907711670556013604839586446706324415722155397
53697817977846174064955149290862569321978468622482
83972241375657056057490261407972968652414535100474
82166370484403199890008895243450658541227588666881
16427171479924442928230863465674813919123162824586
17866458359124566529476545682848912883142607690042
24219022671055626321111109370544217506941658960408
07198403850962455444362981230987879927244284909188
84580156166097919133875499200524063689912560717606
05886116467109405077541002256983155200055935729725
71636269561882670428252483600823257530420752963450"""
    strN = "".join(strN.split())
    print max(reduce(operator.mul, map(int,strN[i:i+5]),1) for i in range(0,996)) 

def prob_9():
    print [a*b*(1000-a-b) for a in range(333) for b in range(a+1,499) if ( 2*b < (1000 - a) and ((a**2 + b**2) == (1000-a-b)**2))]   
             
def prob_10():
    pit,s = erat2(),0
    p = pit.next()
    while (p < 2000000):
        s += p
        p = pit.next()
    print s                
    
# def prob_12():#this is highly inefficient
#     i,tn = 1,1
#     while (no_of_divisors(tn) < 501):
#         tn = sum(range(i+1))
#         i = i + 1
#     print tn
    
def prob_14():
    def collatz_len(num):
        n,i = num,1
        while (n != 1):
            if (n%2 == 0):
                n = n/2
            else:
                n = 3*n+1
            i = i + 1
        return (num,i)
    print max((collatz_len(x) for x in range(2,1000000)),key=lambda x:x[1])[0]

def prob_16():
    N, s = 2**1000, 0
    while ( N != 0):
        s += N % 10
        N = N/10
    print s

def prob_20():
    N, s = math.factorial(100) , 0
    while ( N != 0):
        s += N % 10
        N = N/10
    print s

def prob_22():
    totalsc = 0
    with open('names.txt') as f:
        for i,nm in enumerate(sorted(f.read().split(','))):
            totalsc += (i+1)*sum(map(lambda n: ord(n)-ord('A')+1,nm[1:-1]))
    print totalsc

def prob_24():
    for i,perm in enumerate(itertools.permutations("0123456789")):
        if (i == 999999):
            print reduce(operator.add,perm,'')
            return

def prob_25():
    a,b,n = 1,1,1
    while (len(str(a)) < 1000):
        a,b = b,a+b
        n = n + 1
    print n

def prob_27():
    maxc = 0
    for s,t in  ((a,b) for a in range(-1000,1000) for b in range (-1000,1000)):
        n = 0
        while (is_prime(n**2 + s*n + t)):
            if (n+1 > maxc):
                maxc = n+1
                prod = s*t
            n = n + 1
    print prod           

def prob_28():
    s,i,pos = 1,1,1
    for i in range(1,501):
        for x in range(4):
            pos += 2*i
            s += pos
    print s

def prob_29():
    print len({a**b for a in range(2,101) for b in range(2,101)})

def prob_49():
    perms={}
    for i in range(1000,10000):
        if (is_prime(i)):
            ss = ''.join(sorted(str(i)))
            if(perms.get(ss) is None):            
                perms[ss] = [str(i)]
            else: 
                perms[ss].append(str(i))
    for ln in [x for x in perms.keys() if len(perms[x])>=3]:
        for i in range(0,len(perms[ln])-2):
            for j in range(i+1,len(perms[ln])-1):
                for k in range(j+1,len(perms[ln])):
                    if ((int(perms[ln][k])-int(perms[ln][j])) == (int(perms[ln][j])-int(perms[ln][i])) == 3330):
                        print perms[ln][i]+perms[ln][j]+perms[ln][k]
                        return

