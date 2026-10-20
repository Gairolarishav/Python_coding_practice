# Python Practice Questions

A collection of string, list, number, and pattern problems with multiple solution approaches.

---

# String Questions

## 1. Check if two strings are anagrams of each other

```python
# If both strings have same characters
str1 = "listen"
str2 = "silent"

def anagram(str1, str2):
    # Fix uppercase and spacing discrepancies
    str1 = str1.lower().replace(" ", "")
    str2 = str2.lower().replace(" ", "")

    if len(str1) != len(str2):
        return "Not Anagram"

    freq1 = {}
    freq2 = {}

    for char in str1:
        freq1[char] = freq1.get(char, 0) + 1

    for char in str2:
        freq2[char] = freq2.get(char, 0) + 1

    if freq1 == freq2:
        return "Anagram"
    else:
        return "Not Anagram"


print(anagram("listen", "silent"))
```

## 2. Check whether the string is Symmetrical or Palindrome

- **Symmetrical:** both halves of the string are the same.
- **Palindrome:** the string reads the same forward and backward.

```python
string = "khokho"
half = len(string) // 2

if len(string) % 2 == 0:
    first_half = string[:half]
    second_half = string[half:]
else:
    first_half = string[:half]
    second_half = string[half + 1:]

if first_half == second_half:
    print("Symmetrical")
else:
    print("Not symmetrical")


if string == string[::-1]:
    print("Palindrome")
else:
    print("Not Palindrome")
```

## 3. Reverse words in a given string

```python
string = "geeks quiz practice code"
output = "code practice quiz geeks"

string = string.split(" ")
string = string[::-1]
print(" ".join(string))
```

## 4. Avoid space in string length

```python
st1 = "geeksforgeeks 33 best"
count = 0
for i in st1:
    if i != " ":
        count += 1
print(count)
```

## 5. Print even length words in a string

```python
text = "I am laxmi hi"

for word in text.split():
    if len(word) % 2 == 0:
        print(word, end=" ")
```

---

# List Questions

## 6. Remove all occurrences of a specific item from a list

```python
# l1 = [5,20,25,50,20]
l1 = [20, 20, 20, 5]
output = [5,25,50]
n = 20

# Method 1: Using list comprehension
l1 = [i for i in l1 if i != n]

print(l1)

# Method 2: Using while loop
while n in l1:
    l1.remove(n)

print(l1)

# Method 3: Using a for loop with a new list
result = []

for i in l1:
    if i != n:
        result.append(i)

print(result)
```

## 7. Replace list items with a new value if found

```python
l1 = [5, 10, 15, 20, 25, 50, 20]
n = 20
new_value = 200

for i in range(len(l1)):
    if l1[i] == n:
        l1[i] = new_value

print(l1)

# Shorter method using list comprehension
l1 = [new_value if i == n else i for i in l1]

print(l1)
```

## 8. Add a new item to a list after a specific item

```python
l1 = [5, 10, 15, 20, 25]
n = 15
new_item = 100
# Expected output: [5, 10, 15, 100, 20, 25]

# Method 1: Using a for loop
for i in range(len(l1)):
    if l1[i] == n:
        l1.insert(i+1, new_item)

print(l1)

# Method 2: Using index()
if n in l1:
    index = l1.index(n)
    l1.insert(index + 1, new_item)

print(l1)
```

## 9. Iterate both lists simultaneously

```python
l1 = [10,20,30,40]
l2 = [10,200,300,400,6]

# Using zip
for i,j in zip(l1,l2):
    print(i,j)

# Method 1: Using range() and indexes
for i in range(min(len(l1), len(l2))):
    print(l1[i], l2[i])
```

## 10. Concatenate two lists in the following order

```python
list1 = ["Hello", "take"]
list2 = ["Dear", "sir"]

# Using zip
output = []
for i,j in zip(list1,list2):
    output.append(f"{i} {j}")

print(output)

list1 = ["Hello", "take"]
list2 = ["Dear", "sir"]
output = []

for i in list1:
    for j in list2:
        output.append(f"{i} {j}")

print(output)
# Output: ['Hello Dear', 'Hello sir', 'take Dear', 'take sir']


print(list1 + list2)
list1.extend(list2)
print(list1)
```

## 11. Concatenate two lists index-wise

```python
list1 = ["M", "na", "i", "ke"]
list2 = ["y", "me", "s", "lly"]

# Using zip
output = []
for i,j in zip(list1,list2):
    output.append(i+j)

print(output)

# Inner loop
output = []
for i in range(len(list1)):
    for j in range(i, i+1):
        output.append(list1[i]+list2[j])

print(output)

# Method 2: Using indexes, without zip()
output = []

for i in range(len(list1)):
    output.append(list1[i] + list2[i])

print(output)
```

## 12. Check if the list contains three consecutive common numbers

```python
l1 = [4,5,5,5,3,8]
output = 5

l1 = [4, 4, 5, 5, 5, 8]

# Using a for loop
# range(len(l1) - 2) prevents crashes: Because you are looking ahead using i + 1 and i + 2,
# stopping the loop 2 elements before the end ensures you never trigger an IndexError.
for i in range(len(l1) - 2):
    if l1[i] == l1[i + 1] == l1[i + 2]:
        print("Three consecutive common numbers:", l1[i])
        break
else:
    print("Not found")


print(l1, l1[1:], l1[2:])

# Method 2: Using zip() (Pythonic approach)
print(zip(l1))
for a, b, c in zip(l1, l1[1:], l1[2:]):
    if a == b == c:
        print("Found:", a)
        break
else:
    print("Not found")
```

## 13. Test if the list contains elements in a range

```python
l1 = [4,6,5,7,3,9,12]
k,j = 3,10
contains = True

for i in l1:
    if i <= k or i >= j:
        contains = False
        break

print(contains)

print(all(k <= i <= j for i in l1))
```

## 14. Extract elements with frequency greater than k

```python
l1 = [4,6,4,3,3,4,3,4,3,8]
k = 3
output = [4,3]

# Using dict
dic = {}
for i in l1:
    dic[i] = dic.get(i, 0) + 1
    if dic[i] > k:
        print(i)

output = []
# Using count
for i in l1:
    if l1.count(i) > k:
        if i not in output:
            output.append(i)

print(output)
```

## 15. Print unique elements which are not repeated

```python
l1 = [1,3,5,6,3,5,6,1,2]
unique = []

for i in l1:
    if l1.count(i) < 2:
        unique.append(i)

print(unique)

# Using dict
unique = []
dic = {}
for i in l1:
    dic[i] = dic.get(i, 0) + 1

for i in l1:
    if dic[i] == 1:
        unique.append(i)

print(unique)
```

## 16. List product excluding duplicates

```python
l1 = [1,3,5,6,3,5,6,1,7,1]

product = 1
for i in set(l1):
    product *= i

print(product)

# Using for loop
unique = []
product = 1
for i in l1:
    if i not in unique:
        unique.append(i)
        product *= i


print(unique)
print(product)
```

## 17. Count unique values inside a list

```python
l1 = [1,2,2,5,8,4,4,8]
unique = []
for i in l1:
    if l1.count(i) < 2:
        unique.append(i)

print(len(unique))

# Using dict
frequency = {}

for i in l1:
    frequency[i] = frequency.get(i, 0) + 1

unique = []

for i in l1:
    if frequency[i] == 1:
        unique.append(i)

print(unique)
print(len(unique))
```

## 18. Print duplicates from a list of integers

```python
l1 = [10,20,30,20,20,30,40,50,20,60,60,-20,-20]
duplicate = []
seen = set()
for i in l1:
    if l1.count(i) > 1 and i not in seen:
        duplicate.append(i)
        seen.add(i)
print(list(duplicate))

dic = {}
for i in l1:
    dic[i] = dic.get(i, 0) + 1

duplicate = []
seen = set()

for i in l1:
    if dic[i] > 1 and i not in seen:
        duplicate.append(i)
        seen.add(i)

print(duplicate)

# Single loop
seen = set()
duplicate = []
added = set()

for i in l1:
    if i in seen and i not in added:
        duplicate.append(i)
        added.add(i)
    seen.add(i)

print(duplicate)
```

## 19. Remove empty tuples from a list

```python
l1 = [(), ('ram', '15'), (), ('laxman', 6)]

# Using len
for i in l1:
    if len(i) < 1:
        l1.remove(i)

print(l1)

# Using if
for i in l1:
    if i == ():
        l1.remove(i)
print(l1)

# Using list comprehension
l1 = [(), ('ram', '15'), (), ('laxman', 6)]

l1 = [i for i in l1 if i != ()]

print(l1)
```

## 20. Remove multiple elements from a list

```python
l1 = [12,15,3,10, 12]
remo = [12, 3]

l1 = [i for i in l1 if i not in remo]
print(l1)

l2 = []
for i in l1:
    if i not in remo:
       l2.append(i)

print(l2)
```

## 21. Print positive numbers in a range (user input)

```python
num1 = int(input("Enter number 1: "))
num2 = int(input("Enter number 2: "))

if num1 > num2:
    num1, num2 = num2, num1

for i in range(num1, num2 + 1):
    if i > 0:
        print(i)
```

## 22. Find the largest number in a list

```python
l1 = [10,20,3,90,100]

# Using max()
print(max(l1))

# Using a for loop
maximum = l1[0]

for i in l1:
    if maximum < i:
        maximum = i
print(maximum)

# Using sort()
l1.sort()
print(l1[-1])
```

## 23. Find the Nth largest number

```python
l1 = [10, 20, 3, 90, 100, 250, 45, 500, 12]

n = int(input("Which largest number do you want? "))

unique = list(set(l1))
largest = []

for j in range(n):
    if not unique:
        break

    maximum = unique[0]

    for i in unique:
        if i > maximum:
            maximum = i

    largest.append(maximum)
    unique.remove(maximum)

if len(largest) == n and n > 0:
    print(largest[-1])
else:
    print("Invalid position")


# Here is a simple solution using for loops, without sort() or max().
l1 = [10, 20, 30]

n = int(input("Enter position: "))

for j in range(n):
    largest = l1[0]

    for i in l1:
        if i > largest:
            largest = i

    l1.remove(largest)

print("Nth largest number:", largest)
```

## 24. Find the Nth smallest number in a list

```python
l1 = [10,20,3,90,10]
num = int(input("Enter no."))

for j in range(num):
    min = l1[0]

    for i in l1:
        if i < min:
            min = i

    l1.remove(min)
print(min)
```

## 25. Sum of digits of each number in a list

```python
l1 = [12,97,68,94]
sum1 = []

for i in l1:
    n = 0
    while (i > 0):
        n = n + (i%10)

        i = i // 10
    sum1.append(n)
print(sum1)
```

## 26. Shallow copy vs deep copy

```python
import copy
l1 = [4, 8, 2, 10, 15, 18]
l11 = [4, 8, 2, 10, 15, 18]

l2 = l1.copy()
l3 = copy.deepcopy(l11)
l2.append(2)
l3.append(2)

print(l2)
print(l1)
print(l3)
print(l11)
```

## 27. Reverse a list

```python
l1 = [4,5,6,7,8,9]

# l1.reverse()
# print(l1)

st, end = 0, len(l1) - 1

while (st < end):
    l1[st], l1[end] = l1[end], l1[st]

    st = st + 1
    end = end - 1

print(l1)
```

## 28. Different ways to clear a list

```python
l1 = [2,3,5,6,7]

l1.clear()
print(l1)

for i in range(0, len(l1)):
    l1.pop(0)

print(l1)
```

## 29. Swap characters in a string list

```python
l1 = ["Gfg", "is", "best", "for", "Geeks"]
# swap: G to e and e to G

for i in range(len(l1)):
    l1[i] = l1[i].replace("G", "-").replace("e", "G").replace("-","e")
print(l1)
```

## 30. Interchange elements at two positions in a list

```python
l1 = [12,35,9,56,24]

elem1 = int(input("Enter first position :"))
elem2 = int(input("Enter second position :"))

l1[elem1 -1] , l1[elem2-1] = l1[elem2-1], l1[elem2-1]

print(l1)
```

---

# Pattern Programs

## 31. Print the pattern (descending numbers)

```
1 2 3 4            4 4 4 4
1 2 3              3 3 3
1 2                2 2
1                  1
```

```python
for i in range(4,0,-1):
    for j in range(1,i+1):
        print(j, end= " ")

    print()

for i in range(4,0,-1):
    for j in range(1,i+1):
        print(i, end=" ")
    print()
```

## 32. Print the pattern (letters of a word)

```
p
p y
p y t
p y t h
p y t h o
p y t h o n
```

```python
string = input("enter a string")
for i in range(len(string)):
    for j in range(0,i+1):
        print(string[j], end=" ")
    print()
```

## 33. Print the pattern (floyd's triangle)

```
1
2 3
4 5 6
7 8 9 10
```

```python
k = 1
for i in range(4):
    for j in range(0,i+1):
        print(k, end=" ")
        k += 1
    print()
```

---

# More List Questions

## 34. Shift list elements n steps left

```python
l1 = [1, 2, 3, 4, 5]
n = 3

# Method 1: Using slicing (easiest)
n = n % len(l1)
print(n)
l1 = l1[n:] + l1[:n]

print(l1)

# Method 2: Using a loop (without slicing)
l1 = [1, 2, 3, 4, 5]
n = 3

for i in range(n):
    first = l1.pop(0)
    l1.append(first)

print(l1)
```

## 35. Shift list elements n steps right

```python
l1 = [1, 2, 3, 4, 5]
n = 1

n = n % len(l1)
print( l1[-n:], l1[:-n])

l1 = l1[-n:] + l1[:-n]
print(l1)

l1 = [1, 2, 3, 4, 5]
n = 1

for i in range(n):
    last = l1.pop()
    l1.insert(0, last)
print(l1)
```

## 36. Add an element at a specific location

```python
l1 = [1,2,3,4]
value = 3
pos = 2

l1.insert(pos-1,value)
print(l1)


l1 = [1,2,3,4]
value = 3
pos = 2
l2 = []

for i in range(len(l1) + 1):
    if i == pos - 1:
        l2.append(value)

    if i < len(l1):
        l2.append(l1[i])
print(l2)
```

## 37. Count the number of occurrences of a specific element

```python
l1 = [1, 2, 3, 8, 9, 45, 5, 1]

value = 1
print(l1.count(value))

# Method 2: Using a for loop
l1 = [1, 2, 3, 8, 9, 45, 5, 1]

value = 1
count = 0

for i in l1:
    if i == value:
        count += 1

print(count)
```

---

# Number Programs

## 38. Palindrome number or not

```python
n = 1113

org = n
rev = 0

while (n > 0):
    rev = rev * 10 + n % 10
    n = n // 10

if org == rev:
    print("yes")
else:
    print("not")
```

## 39. Sum of even digits and product of odd digits

```python
num = 1532
even = 0
odd = 1
while (num > 0):
    r = num % 10
    if r % 2 == 0:
        even = even + r
        num = num // 10
    else:
        odd = odd * r
        num = num // 10
print("Even:-", even)
print("odd:-", odd)
```

## 40. Sum of digits of a given number

```python
num = 153
su = 0

while (num > 0):
    su = su + num % 10
    num = num // 10
print(su)
```

---

# Star Patterns

## 41. Inverted triangle (shrinking stars)

```python
n = 3
for i in range(n):
    for j in range(0, 2*i):
        print(" " ,end=" ")
    for j in range(0, n+2 - 2*i):
        print("*", end=" ")

    print()
```

## 42. Diamond pattern

```python
n = 3
for i in range(n):
    for j in range(0, n-i-1):
        print(" ", end="")
    for j in range(0, i+1):
        print("*", end=" ")
    print()

for i in range(0, n-1):
    for j in range(0, i+1):
        print(" ", end="")
    for j in range(0, n-i-1):
        print("*", end=" ")
    print()
```
