'''
Basic script to find a non-prime numbers in a text file;
part of deep web riddle 'How deep can you enter'
'''

'''
TODO: optimize;
'''


nonPrimeList = []

# counter = 0

def isPrime(n):
  
    # edge cases 
    if (n <= 1):
        return False
    if (n <= 3):
        return True
  
    # check so that we can skip middle five numbers in the loop 
    if (n % 2 == 0 or n % 3 == 0): 
        return False
  
    i = 5
    while(i * i <= n):
        if (n % i == 0 or n % (i + 2) == 0):
            return False
        i = i + 6
  
    return True


print('Starting to search for non-prime numbers... This may take a while...')
with open('haystack.txt') as file:
    for line in file:
        line = line.split()
        for i in line:
            if (isPrime(int(i))):
                continue
            else:
                print('--- NON-PRIME NUMBER FOUND ---')
                print(i)
                nonPrimeList.append(i)
                continue

print('Search complete, found following non-prime numbers (if any): ')
print(nonPrimeList)