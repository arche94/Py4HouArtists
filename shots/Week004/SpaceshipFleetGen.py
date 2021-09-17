import hou
import random

# globals
root = hou.node('obj')

def initFleetRoot(ptCloud):
  fleetRoot = root.node('SpaceshipFleet')
  if not fleetRoot:
    fleetRoot = root.createNode('subnet')
    fleetRoot.setName('SpaceshipFleet')
  clearNode(fleetRoot)
  
  if ptCloud.type().name() == 'geo':
    ptCloud = ptCloud.node('OUT')

  ptCloudGeo = ptCloud.geometry()
  for pt in ptCloudGeo.points():
    hou.ui.setStatusMessage('Instancing ship {0}...'.format(pt.number()))
    ship = initShip(fleetRoot, pt)
    ship.setColor(randomColor(ship.node('spaceship1').evalParm('seed')))

  layoutNodes(fleetRoot)
  fleetRoot.setColor(hou.Color((0, 1, 0)))
  hou.ui.setStatusMessage('Fleet initialized')

def initShip(fleetRoot, pt):
  ptPos = pt.position()

  shipRoot = fleetRoot.createNode('subnet')
  
  shipGeo = shipRoot.createNode('spaceship')
  shipGeo.parm('seed').set(pt.attribValue('shipType'))
  shipGeo.parm('seed').pressButton()
  
  shipOut = shipRoot.createNode('geo')
  
  objMerge = shipOut.createNode('object_merge')
  objMerge.parm('objpath1').set(shipGeo.node('geo/OUT').path())
  
  objPyType = setShipType(objMerge)
  objPyGrp = createThrusterGroup(objPyType)
  
  objXform = objPyGrp.createOutputNode('xform')
  objXform.parmTuple('t').set((ptPos[0], ptPos[1], ptPos[2]))

  objOut = objXform.createOutputNode('null', node_name='OUT')

  setOutputFlags(shipGeo, visible=False)
  setOutputFlags(objOut)
  layoutNodes(shipRoot)

  return shipRoot

def setShipType(obj):
  objType = obj.parent().parent().node('spaceship1').parm('seed').eval()
  py = obj.createOutputNode('python', 'set_ship_type')
  pyStr = py.parm('python').eval()
  pyStr += 'geo.addAttrib(hou.attribType.Global, "shipType", ' + str(objType) + ', create_local_variable=False)'
  py.parm('python').set(pyStr)
  return py

def createThrusterGroup(obj):
  objGeo = obj.geometry()
  thrusterLimit = None

  # compute min along Z axis
  for pt in objGeo.points():
    ptPos = pt.position()
    if (ptPos[0] > -0.15) & (ptPos[0] < 0.15) & \
      (ptPos[1] > -0.15) & (ptPos[1] < 0.15):
      if not thrusterLimit:
        thrusterLimit = pt
      else: 
        if ptPos[2] < thrusterLimit.position()[2]:
          thrusterLimit = pt
  
  vecLimit = (0, 0, thrusterLimit.position()[2])
  
  # create thruster group
  py = obj.createOutputNode('python', 'create_thruster_grp')
  pyStr = str(py.parm('python').eval())
  pyStr += 'group = geo.createPointGroup("thruster")\n' \
    'for pt in geo.points():\n' \
    '\tptPos = pt.position()\n' \
    '\tif ptPos.distanceTo(hou.Vector3(' + str(vecLimit) + ')) < 0.25:\n' \
    '\t\tgroup.add(pt)'
  py.parm('python').set(pyStr)
  
  return py 

def clearNode(node):
  for c in node.children():
    c.destroy()

def layoutNodes(node):
  node.layoutChildren()
  for c in node.children():
    c.move((5, -1))

def setOutputFlags(node, visible=True):
  if visible:
    node.setGenericFlag(hou.nodeFlag.Display, True)
    node.setGenericFlag(hou.nodeFlag.Render, True)
  else:
    node.setGenericFlag(hou.nodeFlag.Display, False)
    node.setGenericFlag(hou.nodeFlag.Render, False)

def randomColor(seed=None):
  random.seed(seed)
  cx = random.random()
  cy = 1 - random.random()
  cz = pow(random.random(), 2)
  return hou.Color((cx, cy, cz))
    

proceed = hou.ui.displayMessage('Select point cloud', buttons=('Cancel', 'Select point cloud'), default_choice=1, title='Initialize speceship fleet', help='In order to initialize a spaceship fleet you need to select the points to use for initializing ship instances')

if proceed:
  ptCloud = hou.ui.selectNode(initial_node=root, title='Select point cloud geo')
  if ptCloud:
    initFleetRoot(hou.node(ptCloud))