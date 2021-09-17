# Iterates a list of elements
# For each element does something different based on its type

values = [
  5,
  10,
  'foo',
  (4.5, 1.2, 'Goofy', 10, dict, (6.4, 'something')),
  4.5,
  'test',
  None
]

print('Value list: {0}'.format(values))

def elaborate(list):
  print('Computing list {0}'.format(list))
  res = dict()
  for v in list:
    if type(v) is int or type(v) is float:
      tmp = v
      if type(v) is float:
        tmp = int(round(v))
        print('Computing Fibonacci sequence for {0} (rounded to {1})'.format(v, tmp))
      else:
        print('Computing Fibonacci sequence for {0}'.format(v))
      fib0 = 1
      fib1 = 1
      for i in range(2, int(tmp)):
        tmp = fib1
        fib1 += fib0
        fib0 = tmp
      key = 'fib({0})'.format(tmp)
      res[key] = fib1
    elif type(v) is str:
      print('Computing letter set used in "{0}"'.format(v))
      letters = []
      for l in v:
        letters.append(l)
      letters = set(letters)
      key = 'set({0})'.format(v)
      res[key] = letters
    elif type(v) is tuple:
      key = 'elaborate({0})'.format(v)
      res[key] = elaborate(v)
    else:
      print('Cannot elaborate value {0} of type {1}'.format(v, type(v)))
  return res

def printResults(res, prefix=''):
  for k, v in res.items():
    if type(v) is dict:
      printResults(v, prefix=prefix+'-')
    else:
      print('{0} {1} = {2}'.format(prefix, k, v))

results = elaborate(values)
printResults(results)