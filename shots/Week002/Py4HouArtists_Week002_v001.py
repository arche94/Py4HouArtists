'''
Defines the class Kitchen
'''

class Kitchen():
  status = {
    'info': dict(),
    'inUse': dict()
  }
  
  def __init__(self, nStoves, nOvens=1, **kwargs):
    self.setInfo('stoves', nStoves)
    self.setInfo('ovens', nOvens)
    self.setInuse('stoves', 0)
    self.setInuse('ovens', 0)
    for k,v in kwargs.items():
      self.setInfo(k, v)
      self.setInuse(k, 0)

  def __repr__(self):
      infos = 'Kitchen with: '
      for k,i in self.status['info'].items():
        infos += '{quantity} {type}, '.format(quantity=i, type=k)
      infos.strip(', ')
      infos += '\nof which are in use: '
      for k,i in self.status['inUse'].items():
        infos += '{quantity} {type}, '.format(quantity=i, type=str(k).replace('inuse', '').lower())
      return infos.strip(', ')

  # sets attribute and status info about an object in the kitchen
  '''
  name : str -> name of the object
  value : Any -> data for the object

  return None
  '''
  def setInfo(self, name: str, value):
      self.status['info'][name] = value 

  # sets attribute and status info about the usage of an object in the kitchen
  '''
  name : str -> name of the object
  value : Any -> data for the object
  '''
  def setInuse(self, name: str, value):
      self.status['inUse'][name] = value 

  # adds objects in the kitchen
  '''
  type : str -> name of the new object
  amount : int (default 1) -> quantity of the object
  '''
  def addObject(self, type, amount=1):
    if (amount < 1):
      print('Cannot add a negative number of {0}'.format(type))
      return
    newAmount = 0
    try:
      newAmount = self.status['info'][type] + amount
    except KeyError:
      newAmount = amount
      self.setInuse(type, 0)  
    self.setInfo(type, newAmount)

  # uses objects in the kitchen
  '''
  type : str -> name of the object to use
  amount : int (default 1) -> quantity of the object to use

  returns string saying how many objects you're using

  raises AttributeError if the amount is greater than the quantity of objects available in the kitchen
  '''
  def useObject(self, type, amount=1):
    availability = self.status['info'][type] - self.status['inUse'][type]
    if availability < amount:
      raise AttributeError('There are not enough {0} unused in the kitchen'.format(type))
    else:
      self.status['inUse'][type] += amount
      return 'You\'re now using {0} {1}'.format(amount, type)

  # releases some of the objects in use
  '''
  type : str -> name of the object to release
  amount : int (default 1) -> quantity of the object to release

  returns string saying how many objects you released

  raises AttributeError if the amount is greater than the quantity of objects currently in use
  '''
  def releaseObject(self, type, amount=1):
    if self.status['inUse'][type] < amount:
      raise AttributeError('There are not {0} {1} in use from the kitchen'.format(amount, type))
    else:
      self.status['inUse'][type] -= amount
      return 'You have released {1} {0}, there are still {2} {0} in use'.format(type, amount, self.status['inUse'][type])

'''
Tests the class Kitchen
'''

#defines kitchen instance initial status
kitchenObjs = {
  'forks': 20,
  'knives': 20,
  'glasses': 10,
  'pots': 4,
  'pans': 3
}
kitchen = Kitchen(4, **kitchenObjs)
print(kitchen)

# add more objects to the kitchen
kitchen.addObject('knives')
kitchen.addObject('dishes', 12)
kitchen.addObject('glasses', 3)
kitchen.addObject('forks', -20)
print(kitchen)

# uses and releases some objects from the kitchen
try:
  print(kitchen.useObject('forks'))
  print(kitchen.useObject('knives', 7))
  print(kitchen.useObject('stoves', 2))
  print(kitchen.useObject('pots', 4))
except AttributeError as e:
  print(e)  
else:
  print('Until here no error occurred')   # this is expected to be executed, no exception should be raised
finally:
  print('Continuing execution')

try:
  print(kitchen.releaseObject('knives', 2))
  print(kitchen.useObject('forks', 3))
  print(kitchen.releaseObject('ovens', 3))  # this is expected to fail end enter the except block
except AttributeError as e:
  print(e)
else:
  print('Until here no error occurred')
finally:
  print('Continuing execution')

try:
  print(kitchen.releaseObject('forks', 2))
  print(kitchen.useObject('ovens', 1))
  print(kitchen.releaseObject('pots', 3))
  print(kitchen.releaseObject('knives'))
  print(kitchen.useObject('glasses', 17))   # this is expected to fail end enter the except block
except AttributeError as e:
  print(e)
else:
  print('Until here no error occurred')
finally:
  print('Continuing execution')

print(kitchen)