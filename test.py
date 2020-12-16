from math import pi, sin, cos
import sys

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
import direct.directbase.DirectStart
from panda3d.core import WindowProperties
from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from panda3d.core import CollisionTube,CollisionSegment
from panda3d.core import Filename,AmbientLight,DirectionalLight
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from panda3d.core import Point3,Vec3,Vec4,BitMask32
from panda3d.core import LightRampAttrib
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math

SPEED = 0.5

def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1),
                        pos=(-1.3, pos), align=TextNode.ALeft, scale = .05)

# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1,1,1,1),
                        pos=(1.3,-0.95), align=TextNode.ARight, scale = .07)

class World(DirectObject):

    def __init__(self):

        self.controlMap = {"left":0, "right":0, "forward":0, "backward":0,
            "zoom-in":0, "zoom-out":0, "wheel-in":0, "wheel-out":0}
        self.mousebtn = [0,0,0]
        base.win.setClearColor(Vec4(0,0,0,1))

        # Post the instructions

        self.title = addTitle("Panda3D Tutorial: Better Ralph (Walking on Uneven Terrain)")
        self.inst1 = addInstructions(0.95, "[ESC]: Quit")
        self.inst2 = addInstructions(0.90, "W A S D keys move Ralph forward, left, back, and right, respectively.")
        self.inst3 = addInstructions(0.85, "Use the mouse to look around and steer Ralph.")
        self.inst4 = addInstructions(0.80, "Zoom in and out using the mouse wheel, or page up and page down keys.")

        # Set up the environment
        #
        # This environment model contains collision meshes.  If you look
        # in the egg file, you will see the following:
        #
        #    <Collide> { Polyset keep descend }
        #
        # This tag causes the following mesh to be converted to a collision
        # mesh -- a mesh which is optimized for collision, not rendering.
        # It also keeps the original mesh, so there are now two copies ---
        # one optimized for rendering, one for collisions.

        self.environ = loader.loadModel("models/world")
        self.environ.reparentTo(render)
        self.environ.setPos(0,0,0)

        # Create the main character, Ralph

        ralphStartPos = self.environ.find("**/start_point").getPos()
        self.ralph = Actor("models/ralph",
                                 {"run":"models/ralph-run",
                                  "walk":"models/ralph-walk"})
        self.ralph.reparentTo(render)
        self.ralph.setScale(.2)
        self.ralph.setPos(ralphStartPos)

        # Accept the control keys for movement and rotation

        self.accept("escape", sys.exit)
        self.accept("w", self.setControl, ["forward",1])
        self.accept("a", self.setControl, ["left",1])
        self.accept("s", self.setControl, ["backward",1])
        self.accept("d", self.setControl, ["right",1])
        self.accept("w-up", self.setControl, ["forward",0])
        self.accept("a-up", self.setControl, ["left",0])
        self.accept("s-up", self.setControl, ["backward",0])
        self.accept("d-up", self.setControl, ["right",0])
#        self.accept("mouse1", self.setControl, ["zoom-in", 1])
#        self.accept("mouse1-up", self.setControl, ["zoom-in", 0])
#        self.accept("mouse3", self.setControl, ["zoom-out", 1])
#        self.accept("mouse3-up", self.setControl, ["zoom-out", 0])
        self.accept("wheel_up", self.setControl, ["wheel-in", 1])
        self.accept("wheel_down", self.setControl, ["wheel-out", 1])
        self.accept("page_up", self.setControl, ["zoom-in", 1])
        self.accept("page_up-up", self.setControl, ["zoom-in", 0])
        self.accept("page_down", self.setControl, ["zoom-out", 1])
        self.accept("page_down-up", self.setControl, ["zoom-out", 0])

        taskMgr.add(self.move,"moveTask")

        # Game state variables
        self.isMoving = False

        # Set up the camera
        # Adding the camera to Ralph is a simple way to keep the camera locked
        # in behind Ralph regardless of ralph's movement.
        base.camera.reparentTo(self.ralph)
        # We don't actually want to point the camera at Ralph's feet.
        # This value will serve as a vertical offset so we can look over Ralph
        self.cameraTargetHeight = 6.0
        # How far should the camera be from Ralph
        self.cameraDistance = 30
        # Initialize the pitch of the camera
        self.cameraPitch = 10
        # This just disables the built in camera controls; we're using our own.
        base.disableMouse()
        # The mouse moves rotates the camera so lets get rid of the cursor
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        

        # We will detect the height of the terrain by creating a collision
        # ray and casting it downward toward the terrain.  One ray will
        # start above ralph's head.
        # A ray may hit the terrain, or it may hit a rock or a tree.  If it
        # hits the terrain, we can detect the height.  If it hits anything
        # else, we rule that the move is illegal.

        self.cTrav = CollisionTraverser()

        self.ralphGroundRay = CollisionRay()
        self.ralphGroundRay.setOrigin(0,0,1000)
        self.ralphGroundRay.setDirection(0,0,-1)
        self.ralphGroundCol = CollisionNode('ralphRay')
        self.ralphGroundCol.addSolid(self.ralphGroundRay)
        self.ralphGroundCol.setFromCollideMask(BitMask32.bit(0))
        self.ralphGroundCol.setIntoCollideMask(BitMask32.allOff())
        self.ralphGroundColNp = self.ralph.attachNewNode(self.ralphGroundCol)
        self.ralphGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.ralphGroundColNp, self.ralphGroundHandler)

        # We will detect anything obstructing the camera's view of the player

        self.cameraRay = CollisionSegment((0,0,self.cameraTargetHeight),(0,5,5))
        self.cameraCol = CollisionNode('cameraRay')
        self.cameraCol.addSolid(self.cameraRay)
        self.cameraCol.setFromCollideMask(BitMask32.bit(0))
        self.cameraCol.setIntoCollideMask(BitMask32.allOff())
        self.cameraColNp = self.ralph.attachNewNode(self.cameraCol)
        self.cameraColHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.cameraColNp, self.cameraColHandler)

############## CollisionTube doesn't seem to be working
#        self.cameraRay = CollisionTube( (0,0,self.cameraTargetHeight),
#                                        (0,25,25),
#                                        (self.cameraTargetHeight/2))
#        self.cameraCol = CollisionNode('cameraRay')
#        self.cameraCol.addSolid(self.cameraRay)
#        self.cameraCol.setFromCollideMask(BitMask32.bit(0))
#        self.cameraCol.setIntoCollideMask(BitMask32.allOff())
#        self.cameraColNp = self.ralph.attachNewNode(self.cameraCol)
#        self.cameraColHandler = CollisionHandlerQueue()
#        self.cTrav.addCollider(self.cameraColNp, self.cameraColHandler)
############

        # Uncomment this line to see the collision rays
        #self.ralphGroundColNp.show()
        #self.camGroundColNp.show()
        #self.cameraColNp.show()

        # Uncomment this line to show a visual representation of the
        # collisions occuring
        #self.cTrav.showCollisions(render)

        # Create some lighting
        # lets add hdr lighting for fun
        render.setShaderAuto()
        render.setAttrib(LightRampAttrib.makeHdr1())
        ambientLight = AmbientLight("ambientLight")
        # existing lighting is effectively darkened so boost ambient a bit
        ambientLight.setColor(Vec4(.4, .4, .4, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(Vec3(-5, -5, -5))
        # hdr can handle any amount of lighting
        # lets make things nice and sunny
        directionalLight.setColor(Vec4(2.0, 2.0, 2.0, 1.0))
        directionalLight.setSpecularColor(Vec4(2.0, 2.0, 2.0, 1))
        render.setLight(render.attachNewNode(ambientLight))
        render.setLight(render.attachNewNode(directionalLight))

    #Records the state of the arrow keys
    def setControl(self, key, value):
        self.controlMap[key] = value


    # Accepts arrow keys to move either the player or the menu cursor,
    # Also deals with grid checking and collision detection
    def move(self, task):

        # save ralph's initial position so that we can restore it,
        # in case he falls off the map or runs into something.

        startpos = self.ralph.getPos()

        # If a move-key is pressed, move ralph in the specified direction.
        if (self.controlMap["forward"]!=0):
            self.ralph.setY(self.ralph, -25 * globalClock.getDt())
        if (self.controlMap["backward"]!=0):
            self.ralph.setY(self.ralph, 25 * globalClock.getDt())
        if (self.controlMap["left"]!=0):
            self.ralph.setX(self.ralph, 25 * globalClock.getDt())
        if (self.controlMap["right"]!=0):
            self.ralph.setX(self.ralph, -25 * globalClock.getDt())

        # If a zoom button is pressed, zoom in or out
        if (self.controlMap["wheel-in"]!=0):
            self.cameraDistance -= 0.1 * self.cameraDistance;
            if (self.cameraDistance < 5):
                self.cameraDistance = 5
            self.controlMap["wheel-in"] = 0
        elif (self.controlMap["wheel-out"]!=0):
            self.cameraDistance += 0.1 * self.cameraDistance;
            if (self.cameraDistance > 250):
                self.cameraDistance = 250
            self.controlMap["wheel-out"] = 0
        if (self.controlMap["zoom-in"]!=0):
            self.cameraDistance -= globalClock.getDt() * self.cameraDistance;
            if (self.cameraDistance < 5):
                self.cameraDistance = 5
        elif (self.controlMap["zoom-out"]!=0):
            self.cameraDistance += globalClock.getDt() * self.cameraDistance;
            if (self.cameraDistance > 250):
                self.cameraDistance = 250

        # Use mouse input to turn both Ralph and the Camera
        if base.mouseWatcherNode.hasMouse():
            # get changes in mouse position
            md = base.win.getPointer(0)
            x = md.getX()
            y = md.getY()
            deltaX = md.getX() - 200
            deltaY = md.getY() - 200
            # reset mouse cursor position
            base.win.movePointer(0, 200, 200)
            # alter ralph's yaw by an amount proportionate to deltaX
            self.ralph.setH(self.ralph.getH() - 0.3* deltaX)
            # find the new camera pitch and clamp it to a reasonable range
            self.cameraPitch = self.cameraPitch + 0.1 * deltaY
            if (self.cameraPitch < -60): self.cameraPitch = -60
            if (self.cameraPitch >  80): self.cameraPitch =  80
            base.camera.setHpr(0,self.cameraPitch,0)
            # set the camera at around ralph's middle
            # We should pivot around here instead of the view target which is noticebly higher
            base.camera.setPos(0,0,self.cameraTargetHeight/2)
            # back the camera out to its proper distance
            base.camera.setY(base.camera,self.cameraDistance)

        # point the camera at the view target
        viewTarget = Point3(0,0,self.cameraTargetHeight)
        base.camera.lookAt(viewTarget)
        # reposition the end of the  camera's obstruction ray trace
        self.cameraRay.setPointB(base.camera.getPos())


        # If ralph is moving, loop the run animation.
        # If he is standing still, stop the animation.

        if (self.controlMap["forward"]!=0) or (self.controlMap["left"]!=0) or (self.controlMap["right"]!=0) or (self.controlMap["backward"]!=0):
            if self.isMoving is False:
                self.ralph.loop("run")
                self.isMoving = True
        else:
            if self.isMoving:
                self.ralph.stop()
                self.ralph.pose("walk",5)
                self.isMoving = False

        # Now check for collisions.

        self.cTrav.traverse(render)

        # Adjust ralph's Z coordinate.  If ralph's ray hit terrain,
        # update his Z. If it hit anything else, or didn't hit anything, put
        # him back where he was last frame.

        entries = []
        for i in range(self.ralphGroundHandler.getNumEntries()):
            entry = self.ralphGroundHandler.getEntry(i)
            entries.append(entry)
        entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))
        if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
            self.ralph.setZ(entries[0].getSurfacePoint(render).getZ())
        else:
            self.ralph.setPos(startpos)

        # We will detect anything obstructing the camera via a ray trace
        # from the view target around the avatar's head, to the desired camera
        # podition. If the ray intersects anything, we move the camera to the
        # the first intersection point, This brings the camera in between its
        # ideal position, and any present obstructions.

        entries = []
        for i in range(self.cameraColHandler.getNumEntries()):
            entry = self.cameraColHandler.getEntry(i)
            entries.append(entry)
        entries.sort(lambda x,y: cmp(-y.getSurfacePoint(self.ralph).getY(),
                                     -x.getSurfacePoint(self.ralph).getY()))
        if (len(entries)>0):
            collisionPoint =  entries[0].getSurfacePoint(self.ralph)
            collisionVec = ( viewTarget - collisionPoint)
            if ( collisionVec.lengthSquared() < self.cameraDistance * self.cameraDistance ):
                base.camera.setPos(collisionPoint)
                if (entries[0].getIntoNode().getName() == "terrain"):
                    base.camera.setZ(base.camera, 0.2)
                base.camera.setY(base.camera, 0.3)

        return task.cont

w = World()
run()
