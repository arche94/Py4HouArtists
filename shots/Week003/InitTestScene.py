import hou

# setup controls
ctrl = hou.node('obj').createNode('null', 'CTRL_Transform')
ctrl.setGenericFlag(hou.nodeFlag.Display, False)
ctrl.setColor(hou.Color((1, 0, 0)))
ctrl.setUserData('nodeshape', 'chevron_down')

# setup ground
ground = ctrl.createOutputNode('geo', 'GROUND')
g_grid = ground.createNode('grid')
g_grid.parm('rows').set(2)
g_grid.parm('cols').set(2)

# setup lights
light_front = ctrl.createOutputNode('hlight', 'LIGHT_Front')
light_front.parm('coneenable').set(True)
light_front.parmTuple('t').set((-5,7,12))
light_front.parmTuple('r').set((-37.4,0.45,-0.35))
light_front.parm('light_intensity').setExpression('20*pow(ch("../CTRL_Transform/scale"),2)')
light_front.parmTuple('light_color').set((1,0.71,0.54))

light_back = ctrl.createOutputNode('hlight', 'LIGHT_Back')
light_back.parm('coneenable').set(True)
light_back.parmTuple('t').set((9,1,-13))
light_back.parmTuple('r').set((-14,136,-9.5))
light_back.parm('light_intensity').setExpression('20*pow(ch("../CTRL_Transform/scale"),2)')
light_back.parmTuple('light_color').set((0.36,0.41,1))

# setup camera
cam = ctrl.createOutputNode('cam', 'CAM_Main')
cam.parmTuple('t').set((-1.6, 2.4, 9.5))
cam.parmTuple('r').set((-9, -8.8, 1.9))
hou.ui.curDesktop().paneTabOfType(hou.paneTabType.SceneViewer).curViewport().setCamera(cam)

hou.node('obj').layoutChildren()