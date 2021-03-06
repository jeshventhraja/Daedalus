from random import *

""" used to find the modular multiplicative inverse """	
def extended_euclid_algorithm(a,b):
	if(a%b==1):
		large=1
		small=(a-1)/b
		return large,small
	else:
		large,small=extended_euclid_algorithm(b,a%b)
		coeff_small=(a-a%b)/b
		large,small=small,small*coeff_small+large
		return large,small

""" To decrypt using Chinese Remainder Theorem """
def decrypt_crt(c,d,p,q):
	dp,dq=(c%p,c%q)
	dp_power,dq_power=(power(dp,d)%p,power(dq,d)%q)
	dummy,pinv=extended_euclid_algorithm(q,p)
	if(pinv*p)%q!=1:
		pinv=q-pinv
	dummy,qinv=extended_euclid_algorithm(p,q)
	if(qinv*q)%p!=1:
		qinv=p-qinv
	ans=(dp_power*q*qinv+dq_power*p*pinv)%(p*q)
	return ans
	
""" Computes a to the power n, using square and multiply algorithm """	
def power(a,n):
	if(n==0):
		return 1
	elif(n==1):
		return a
	elif n%2==1:
		return a*power(a**2,(n-1)/2)
	else:
		return power(a**2,n/2)

""" Encrypts a message c """		
def encrypt(n,e,c):
	exponent=power(c,e)
	cipher=exponent%n
	return cipher
	
""" Finds the gcd of a and b """	
def gcd(a,b):
	if(a==0):
		return b
	elif(b==0):
		return a
	elif(a>b):
		a=a%b
	else:
		b=b%a
	return gcd(a,b)
	
""" Finds out if n is prime or not (all primes are of the form 6k+/- 1 or 2 or 3) """
def not_prime(n):
	a=5
	b=7
	while a<=(n**0.5):
		if(n%a==0 or n%b==0):
			return 1
		a=a+6
		b=b+6
	return 0
	
""" Sets the bounds for the prime numbers """	
lower_limit=100
upper_limit=1000
p=randint(lower_limit,upper_limit)
q=randint(lower_limit,upper_limit)

while p%2==0 or p%3==0 or not_prime(p):
	p=randint(lower_limit,upper_limit)
while q%2==0 or q%3==0 or not_prime(q):
	q=randint(lower_limit,upper_limit)
	
encryption=dict()
encryption["p"]=p
encryption["q"]=q
encryption["n"]=p*q

message=raw_input("Input a message: ")
n=p*q
totient=(p-1)*(q-1)
for i in range(3,totient):
	coprime=1
	if(gcd(i,totient)!=1):
		coprime=0
	if(coprime==1):
		break
e=i
encryption["e"]=e
encryption["totient"]=totient

large,small=extended_euclid_algorithm(totient,e)
if(small*e)%totient==1:
	d=small
else:
	d=totient-small
encryption["d"]=d
decrypted_text=[]
print "encrypted message: ",
for character in message:
	cipher=encrypt(n,e,ord(character))
	print cipher,
	decipher_crt=decrypt_crt(cipher,d,p,q)
	decrypted_text.append(chr(decipher_crt))
print "\nDecrypted message is: ","".join(decrypted_text)
for a in encryption:
	print a,encryption[a]

