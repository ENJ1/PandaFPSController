import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import WindowProperties
from math import pi, sin, cos
import sys
import time

from direct.showbase.ShowBase import ShowBase

#set up a loading screen
from direct.gui.OnscreenText import OnscreenText,TextNode

from direct.task import Task
from direct.actor.Actor import Actor
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

from panda3d.core import TransparencyAttrib
from pandac.PandaModules import WindowProperties

from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from panda3d.core import *
from panda3d.physics import *

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # enable physics engine
        self.enableParticles()

        # take care of cursor shit
        self.resetCursor()

        # set up loading screen
        self.loadingText=OnscreenText("Loading...",1,fg=(1,1,1,1),pos=(0,0),align=TextNode.ACenter,scale=.07,mayChange=1)
        self.graphicsEngine.renderFrame() #render a frame otherwise the screen will remain black
        self.graphicsEngine.renderFrame() #idem dito
        self.graphicsEngine.renderFrame() #you need to do this because you didn't yet call run()
        self.graphicsEngine.renderFrame() #run() automatically renders the frames for you

        # get menu background music playing
        self.loadingText.setText('Loading models/audio/sfx/menu_music.ogg') 
        self.graphicsEngine.renderFrame() #render a frame otherwise the screen will remain black
        self.graphicsEngine.renderFrame() #idem dito
        self.graphicsEngine.renderFrame() #you need to do this because you didn't yet call run()
        self.graphicsEngine.renderFrame() #run() automatically renders the frames for you
        menuMusic = self.loader.loadSfx("models/audio/sfx/menu_music.ogg")
        menuMusic.setLoop(True)
        menuMusic.play()

        # set title window
        props = WindowProperties( )
        props.setTitle( 'Tokoyo Ghoul' )
        self.win.requestProperties( props )

        # Load the environment model.
        self.loadingText.setText('Loading models/environment.egg.pz') 
        self.setBackgroundColor((0,1,1, .5))
        self.graphicsEngine.renderFrame() #render a frame otherwise the screen will remain black
        self.graphicsEngine.renderFrame() #idem dito
        self.graphicsEngine.renderFrame() #you need to do this because you didn't yet call run()
        self.graphicsEngine.renderFrame() #run() automatically renders the frames for you
        self.scene = self.loader.loadModel("models/output.bam")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.15, 0.15, 0.15)
        self.scene.setPos(0, 0, 0)
        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # add fog and such
        #myFog = Fog("titlefog")
        #myFog.setColor((1,0,0,0.1))
        #myFog.setExpDensity(0.3)
        #self.render.setFog(myFog)

        # Load and transform the didicus actor.
        #self.pandaActor = Actor("models/camera",
            #{"walk": "models/panda-walk4"})
        self.loadingText.setText('Loading models/african.x')
        self.graphicsEngine.renderFrame() #render a frame otherwise the screen will remain black
        self.graphicsEngine.renderFrame() #idem dito
        self.graphicsEngine.renderFrame() #you need to do this because you didn't yet call run()
        self.graphicsEngine.renderFrame() #run() automatically renders the frames for you
        self.pandaActor = Actor("models/camera")
        self.pandaActor.setPos(10,-10,5)
        self.pandaActor.setScale(0.5, 0.5, 0.5)
        self.pandaActor.reparentTo(self.render)
        # Loop its animation.
        #self.pandaActor.loop("walk")
        # Create the four lerp intervals needed for the panda to
        # walk back and forth.
        pandaPosInterval1 = self.pandaActor.posInterval(13,Point3(-10, -10, 5),startPos=Point3(0, 0, 5))
        pandaPosInterval2 = self.pandaActor.posInterval(13,Point3(0, 0, 5),startPos=Point3(-10, -10, 5))
        pandaHprInterval1 = self.pandaActor.hprInterval(3,Point3(180, 0, 0),startHpr=Point3(0, 0, 0))
        pandaHprInterval2 = self.pandaActor.hprInterval(3,Point3(0, 0, 0),startHpr=Point3(180, 0, 0))

        # Create and play the sequence that coordinates the intervals.
        self.pandaPace = Sequence(pandaPosInterval1,pandaHprInterval1,pandaPosInterval2,pandaHprInterval2,name="pandaPace")
        self.pandaPace.loop()

        # Make the menu options
        # Create a frame
        self.startgamebutton = DirectButton(pos = (1, 0, -0.6),text = ("Play"),scale=.1, command=self.startGame)
        self.exitbutton = DirectButton(pos = (1, 0, -0.74),text = ("Exit"),scale=.1, command=self.close)

        # load the title image
        self.loadingText.setText('Loading images/title.png')
        self.graphicsEngine.renderFrame() #render a frame otherwise the screen will remain black
        self.graphicsEngine.renderFrame() #idem dito
        self.graphicsEngine.renderFrame() #you need to do this because you didn't yet call run()
        self.graphicsEngine.renderFrame() #run() automatically renders the frames for you

        # clean up loading screen
        self.loadingText.cleanup()

    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(75 * sin(angleRadians), -75 * cos(angleRadians), 20)
        #self.camera.setPos(0, 0, 20)
        self.camera.setHpr(angleDegrees, -10, 0)
        return Task.cont

    # Callback function to set text 
    def startGame(self):
        print ("starting game")
        # clear everything on the menu
        self.scene.removeNode()
        self.startgamebutton.removeNode()
        self.exitbutton.removeNode()

        # set cursor for first person shit
        self.disableMouse()
        #self.cursorShit()

        # load the new place
        # Load the environment model.
        self.loadingText=OnscreenText("Loading...",1,fg=(1,1,1,1),pos=(0,0),align=TextNode.ACenter,scale=.07,mayChange=1)
        self.loadingText.setText('Loading models/environment.egg.pz') 
        self.setBackgroundColor((0,0,0))
        self.graphicsEngine.renderFrame() #render a frame otherwise the screen will remain black
        self.graphicsEngine.renderFrame() #idem dito
        self.graphicsEngine.renderFrame() #you need to do this because you didn't yet call run()
        self.graphicsEngine.renderFrame() #run() automatically renders the frames for you
        self.scene = self.loader.loadModel("models/output.bam")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(1, 1, 1)
        self.scene.setPos(0, 0, 0)
        # clean up loading screen
        self.loadingText.cleanup()

        # remove camera rotation and enable other shit
        self.taskMgr.remove("SpinCameraTask")

        # load the model for first person camera
        node = NodePath("PhysicsNode")
        node.reparentTo(self.render)
        an = ActorNode("girl")
        anp = node.attachNewNode(an)
        self.physicsMgr.attachPhysicalNode(an)
        self.cameraModel = loader.loadModel("models/camera")
        self.cameraModel.reparentTo(self.render) # inherit transforms
        self.cameraModel.setEffect(CompassEffect.make(render)) # NOT inherit rotation
        self.cameraModel.reparentTo(anp)
        self.cameraModel.setPos(10,-10,30)
        self.cameraModel.setScale(5, 5, 5)
        self.camera.reparentTo(self.cameraModel)
        self.camera.lookAt(self.cameraModel)
        self.camera.setY(0) # camera distance from model

        # start doing some gravity stuff
        an.getPhysicsObject().setMass(136.077)

        gravityFN = ForceNode('world-forces')
        gravityFNP= self.render.attachNewNode(gravityFN)
        gravityForce= LinearVectorForce(0,0,-.81) #gravity acceleration
        gravityFN.addForce(gravityForce)

        base.physicsMgr.addLinearForce(gravityForce)

        # collisions
        fromObject2 = self.scene.attachNewNode(CollisionNode('colNode'))
        fromObject2.node().addSolid(CollisionBox(Point3(-100,-100,0), Point3(100,100,20)))
        fromObject2.show()

        fromObject = self.cameraModel.attachNewNode(CollisionNode('colNode'))
        fromObject.node().addSolid(CollisionRay(0, 0, 0, 0, 0, -1))

        lifter = CollisionHandlerFloor()
        lifter.addCollider(fromObject, self.cameraModel)

        self.keyMap = {"w" : False, "s" : False, "a" : False, "d" : False, "spacebar" : False}

        self.accept("w", self.setKey, ["w", True])
        self.accept("s", self.setKey, ["s", True])  
        self.accept("a", self.setKey, ["a", True])  
        self.accept("d", self.setKey, ["d", True])
        self.accept("space", self.setKey, ["spacebar", True])

        self.accept("w-up", self.setKey, ["w", False])
        self.accept("s-up", self.setKey, ["s", False])
        self.accept("a-up", self.setKey, ["a", False])
        self.accept("d-up", self.setKey, ["d", False])
        self.accept("space-up", self.setKey, ["spacebar", False])

        self.cursorShit()

        self.taskMgr.add(self.cameraControl, "Camera Control")

    def close(self):
        sys.exit()

    def setKey(self, key, value):
        self.keyMap[key] = value

    def cameraControl(self, task):
        dt = globalClock.getDt()
        if(dt > .20):
            return task.cont

        if(self.mouseWatcherNode.hasMouse() == True):
            mpos = self.mouseWatcherNode.getMouse()
            self.camera.setP(mpos.getY() * 30)
            self.camera.setH(mpos.getX() * -50)
            if (mpos.getX() < 1.0 and mpos.getX() > -1.0 ):
                self.cameraModel.setH(self.cameraModel.getH())
            else:
                self.cameraModel.setH(self.cameraModel.getH() + mpos.getX() * -1)

            """ this task updates the mouse 
            md = self.win.getPointer(0)
            x = md.getX()
            y = md.getY()
            if self.win.movePointer(0, self.win.getXSize()/2, self.win.getYSize()/2):
                self.cameraModel.setH(self.cameraModel.getH() -  (x - self.win.getXSize()/2)*0.01)
                self.camera.setP(self.camera.getP() - (y - self.win.getYSize()/2)*0.01)"""

        if(self.keyMap["w"] == True):
            self.cameraModel.setY(self.cameraModel, 15 * dt)
            print("camera moving forward")
            return task.cont
        elif(self.keyMap["s"] == True):
            self.cameraModel.setY(self.cameraModel, -15 * dt)
            print("camera moving backwards")
            return task.cont
        elif(self.keyMap["a"] == True):
            self.cameraModel.setX(self.cameraModel, -10 * dt)
            print("camera moving left")
            return task.cont
        elif(self.keyMap["d"] == True):
            self.cameraModel.setX(self.cameraModel, 10 * dt)
            print("camera moving right")
            return task.cont
        elif(self.keyMap["spacebar"] == True):
            self.cameraModel.setZ(self.cameraModel, 10 * dt)
            print("camera moving up")
            return task.cont
        else:
            return task.cont

    def cursorShit(self):
        # To set relative mode and hide the cursor:
        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_confined)
        self.win.requestProperties(props)

    def resetCursor(self):
        # To revert to normal mode:
        props = WindowProperties()
        props.setCursorHidden(False)
        props.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(props)


# load up the game menu 
app = MyApp()
app.run()
