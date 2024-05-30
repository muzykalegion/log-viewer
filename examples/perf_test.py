import timeit

t = timeit.timeit('b.extend(a)', setup='b=[];a=range(0,10)', number=100000000)
print(t)

t = timeit.timeit('b = a[:]', setup='b=[];a=range(0,10)', number=100000000)
print(t)

t = timeit.timeit('b = list(a)', setup='b=[];a=range(0,10)', number=100000000)
print(t)

t = timeit.timeit('b = [elem for elem in a]', setup='b=[];a=range(0,10)', number=100000000)
print(t)

t = timeit.timeit('for elem in a: b.append(elem)', setup='b=[];a=range(0,10)', number=100000000)
print(t)
#
# timeit.timeit('b = deepcopy(a)', setup='from copy import deepcopy; b=[];a=range(0,10)', number=100000000)