# Python Practice Questions (Part 2)

Star patterns, number programs, array/list problems, and number patterns, with multiple solution approaches.

---

# Star Patterns

## 1. Right angle triangle

```
*
* *
* * *
* * * *
```

```python
for i in range(0,4):
    for j in range(0,i+1):
        print("*", end=" ")
    print()
```

## 2. Odd-numbered stars per row

```
*
* * *
* * * * *
```

```python
for i in range(0,3):
    for j in range(0,2*i +1):
        print("*", end=" ")
    print()
```

## 3. Pyramid shape (right-aligned triangle)

```python
for i in range(0,4):
    for j in range(0,4-i-1):
        print(" ", end="")
    for j in range(0,i+1):
        print("*", end=" ")
    print()
```

## 4. Full pyramid (5 rows)

```python
for i in range(0,5):
    for j in range(0,5-i-1):
        print(" ", end=" ")
    for j in range(0,2*i+1):
        print("*", end=" ")
    print()
```

## 5. Inverted right angle triangle (shifted right)

```python
for i in range(0,3):
    for j in range(0,i):
        print(" ",end="")
    for j in range(3,i,-1):
        print("*", end=" ")

    print()
```

## 6. Inverted pyramid (3 rows)

```python
for i in range(0,3):
    for j in range(0,i):
        print(" ", end=" ")
    for j in range(3+2 -2*i,0,-1):
        print("*", end=" ")
    print()
```

## 7. Inverted right angle triangle (4 rows)

```python
for i in range(0,4):
    for j in range(4,i,-1):
        print("*", end=" ")
    print()
```

## 8. Inverted right angle triangle (shifted right, 5 rows)

```python
for i in range(0,5):
    for j in range(0,i):
        print(" ", end=" ")
    for j in range(5,i,-1):
        print("*", end=" ")

    print()
```

## 9. Inverted pyramid (5 rows)

```python
for i in range(0,5):
    for j in range(0,2*i):
        print(" ", end=" ")
    for j in range(5+2 - 2*i, 0, -1):
        print("*", end=" ")
    print()
```

## 10. Conditional pattern (top row, last column, and diagonal)

```python
for i in range(0,5):
    for j in range(0,5):
        if (i == 0 or (j==4 and i!=0) or i==j):
            print("*", end="")
        else:
            print(end=" ")
    print()
```

## 11. Diamond shape

```python
n = 4
for i in range(0,n):
    for j in range(n-i-1,0,-1):
        print(" ", end="")

    for j in range(0,i+1):
        print("*", end=" ")
    print()

for i in range(0,n-1):
    for j in range(0,i+1):
        print(" ", end="")
    for j in range(n-i-1,0,-1):
        print("*", end=" ")
    print()
```

## 12. Base line (only the last row has stars)

```python
n = 4
for i in range(1,n+1):
    for j in range(0,n*2):
        if (i==n):
            print("*", end=" ")
        else:
            print(" ", end="")
    print()
```

---

# Basic Programs

## 13. Swap two numbers

```python
a=16
b=15
a,b = b,a
print(a,b)
```

## 14. Positive, zero, or negative

```python
n1 = 0
if n1 >0 :
    print("Positive")
elif n1 == 0:
    print("zero")
else:
    print("negative")
```

## 15. Leap year

```python
year = 2024
if year % 4 ==0 and year % 100 != 0:
    print("Leap year")
elif year % 400 == 0:
    print("leap year")
else:
    print("Not")
```

## 16. Greatest of three numbers

```python
a = 22
b= 21
c =19

if (a >b  and a>c):
    print("A is greater")
elif (b >c  and b>a):
    print("b is greater")
else:
    print("c is greater")
```

## 17. Prime number

```python
n = 3
prime = True
for i in range(2,n):
    if n % i == 0:
        prime = False
        break

if prime:
    print("prime number")
else:
    print("Not")
```

## 18. Fibonacci series

```python
# fibonacci series
# 0+1+1+2+3+5+8
n =7
x =0
y =1
z = 0

for i in range(0,n):
    print(z)

    x = y
    y = z
    z = x+y
```

## 19. Armstrong number

```python
n = 153
org = n
x = len(str(n))
sum = 0
while (n>0):
    sum = sum + (n%10)**x
    n = n//10

if org == sum:
    print("Armstrong")
else:
    print("Not")
```

## 20. Armstrong numbers in an interval

```python
n = 100
n1 = 2000
for i in range(n,n1+1):
    x = len(str(i))
    org = i
    sum = 0
    while (i > 0):
        sum = sum + (i%10)**x
        i = i//10
    if org == sum:
        print(org,end = " ")
```

## 21. Separate even and odd values of a dictionary

```python
dic = {"val1": 1, "val2": 20, "val3":23}
even,odd = [],[]

for i in dic.values():
    if i % 2==0:
        even.append(i)
    else:
        odd.append(i)
print("even ", even)
print("odd ", odd)
```

## 22. Sum of digits of a number

```python
n = 153
sum = 0
while (n>0):
    sum = sum + n%10
    n = n//10
print(sum)
```

## 23. Sum of even digits and product of odd digits

```python
n = 1532
even = 0
odd = 1
while (n>0):
    r = n %10
    if n % 2 == 0:
        even = even + r
        n = n//10
    else:
        odd = odd * r
        n = n//10

print("even ", even)
print("odd ", odd)
```

## 24. Palindrome number

```python
n = 1113
org = n
rev= 0
while(n > 0):
    rev = rev*10 + n%10
    n = n//10
if org == rev:
    print("palindrome")
else:
    print("Not")
```

---

# Array / List Questions

## 25. Reverse an array

```python
a = [1,2,3,4,5]
st,end = 0,len(a)-1
while(st<end):
    a[st],a[end] = a[end],a[st]
    st = st + 1
    end = end - 1
print(a)
```

## 26. Middle of an array

```python
a = [1,3,5,6,6]
if len(a) % 2 ==0:
    middle1 = len(a) // 2
    middle2 = (len(a) // 2) -1
    print(a[middle1])
    print(a[middle2])
else:
    middle1 = len(a) // 2
    print(a[middle1])
```

## 27. Missing element of an array

```python
n = 10
a = [1,2,3,10,5,8,9,6,4]
total = (n * (n +1))/2
sum = 0
diff = 0
for i in a:
    sum = sum + i
    diff = total - sum
print(int(diff))
```

## 28. Nth greatest element in an array

```python
a = [4,5,9,8,10,3]
max = 0
n = int(input("Enter no.: "))
for i in range(n):
    max = a[0]
    for j in a:
        if j > max:
            max = j
    a.remove(max)
print(max)
```

## 29. Nth smallest number from an array

```python
a = [4,5,9,8,10,3]
min = 0
n = int(input("Enter a number: "))
for i in range(n):
    min = a[0]
    for j in a:
        if j < min:
            min = j
    a.remove(min)
print(min)
```

## 30. Find a fixed point in an array

```python
a = [1,2,2,3,6]
for i in range(len(a)):
    if i == a[i]:
        print(a[i])
```

## 31. Count occurrences of a value in a list

```python
l = [1,2,6,8,9,2,1,6,4,5,5,2]
count = 0
for i in l:
    if i == 1:
        count += 1
print(count)
```

## 32. Count duplicate values

```python
l = [1,2,3,4,5,3,1,5]
seen = set()
duplicates = set()
for i in l:
    if i not in seen:
        seen.add(i)
    else:
        duplicates.add(i)
print(len(duplicates))
```

## 33. Remove duplicates from a list

```python
l1 = [1, 2, 3, 4 ,5 ,3, 1,5]
l2 = []
for i in l1:
    if i not in l2:
        l2.append(i)
print(l2)
```

## 34. Add an element at a specific location

```python
list1 = [1,2,3,4,9]
value = 3
pos = 1
# No loop needed! Just call it directly
list1.insert(pos, value)

print(list1)  # Output: [1, 3, 2, 3, 4, 9]

# Slice before 'pos', add the value in a list, then slice from 'pos' onwards
list2 = [1,2,3,4,9]
list2 = list2[:pos] + [value] + list2[pos:]

print(list2)  # Output: [1, 3, 2, 3, 4, 9]

# No built in
list3 = [1,2,3,4,9]

list3.append(None)
print(list3)
for i in range(len(list3)-1,pos,-1):
    list3[i] = list3[i-1]

list3[pos] = value

print(list3)
```

## 35. Shift list elements n steps left

```python
arr = [1,2,3,4,5]
n = 3

for i in range(n):
    first = arr.pop(0)
    arr.append(first)
print(arr)


# second
a = [1,2,3,4,5]
for _ in range(n):
    first = a[0]

    for i in range(len(a)-1):
        a[i] = a[i+1]

    a[len(a)-1] = first
print(a)
```

## 36. Shift list elements n steps right

```python
a = [1,2,3,4,5]
n = 3
for i in range(n):
    last = a.pop()
    a.insert(0,last)

print(a)

#
a = [1,2,3,4,5]
for _ in range(n):
    last =  a[len(a)-1]
    for i in range(len(a)-1,0,-1):
        a[i] = a[i-1]

    a[0] = last
print(a)
```

---

# Number Patterns

## 37. Descending rows of counting numbers

```
1 2 3 4
1 2 3
1 2
1
```

```python
for i in range(0,4):
    n = 0
    for j in range(4,i,-1):
        n += 1
        print(n, end=" ")
    print()

for i in range(4, 0, -1):      # Counts down: 4, 3, 2, 1
    for j in range(1, i + 1):  # Counts up from 1 to the current row limit
        print(j, end=" ")
    print()
```

## 38. Descending rows of repeated numbers

```
4 4 4 4
3 3 3
2 2
1
```

```python
for i in range(0,4):
    for j in range(4,i,-1):
        print(4- i, end=" ")
    print()

for i in range(4, 0, -1):  # Counts down: 4, 3, 2, 1
    for j in range(i):     # Runs 'i' times for each row
        print(i, end=" ")
    print()
```

---

# More List Questions

## 39. Swap elements in a string list

```python
l1 = ["Gfg", "is", "best", "for", "Geeks"]
# swap: G to e and e to G
print(len(l1))
for i in range(len(l1)):
    l1[i] = l1[i].replace("G", "-").replace("e","G").replace("-", "e")
print(l1)
```

## 40. Remove multiple elements from a list

```python
l = [12,15,12,3,10]
r = [12,30]

l = [item for item in l if item not in r]
print(l)

l = [12,15,12,3,10]
l2 = []
for i in l:
    if i not in r:
       l2.append(i)

print(l2)
```

## 41. Print duplicates from a list of integers

```python
l = [10,20,30,20,20,30,40,50,20,60,60,-20,-20]
seen = set()
duplicate = []
for i in l:
    if l.count(i) > 1 and i not in seen:
        duplicate.append(i)
        seen.add(i)
print(duplicate)

dic = {}
for i in l:
    dic[i] = dic.get(i,0)+1

duplicates = []
for key,values in dic.items():
    if values > 1:
        duplicates.append(key)

print(duplicates)
```
