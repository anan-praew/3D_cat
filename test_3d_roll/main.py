import pygame as pg
import moderngl as mgl
import sys
from model import *
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene
import pandas as pd
import time
#from psychopy import gui

global subj
subj = 'ik'

class GraphicsEngine:

    def __init__(self, win_size=(800, 450)):
        # init pygame modules
        pg.init()
        # window size
        self.WIN_SIZE = win_size
        # set opengl attr
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        # create opengl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        # mouse settings
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        # detect and use existing opengl context
        self.ctx = mgl.create_context()
        # self.ctx.front_face = 'cw'
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        # create an object to help track time
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        self.ntrl = 360
        self.stimdur = 0.5
        self.delay = 0.8
        self.mem = np.tile(np.arange(0,360),1)
        np.random.shuffle(self.mem)
        self.prb = np.random.choice(np.arange(0,360),self.ntrl)
        self.iti = -(np.random.rand(self.ntrl)*0.2+0.3)
        self.resp = []
        self.rt = []
        self.condid = 0
        # light
        self.light = Light()
        # camera
        self.camera = Camera(self)
        # mesh
        self.mesh = Mesh(self)
        # scene
        self.scene = Scene(self)

    def check_events(self):
        global resp,timer
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                pg.quit()
                sys.exit()
            if (resp==1) and (event.type == pg.KEYDOWN and event.key == pg.K_p):
                self.resp.append(self.scene.returndeg())
                self.rt.append(timer - self.stimdur - self.delay)

                if self.condid < self.ntrl:
                    resp = 0
                    timer = self.iti[self.condid]
                    self.initScene()
                else:

                    df = pd.DataFrame(([subj]*self.ntrl,self.mem,self.prb,self.iti,np.ones(self.ntrl)*self.stimdur,np.ones(self.ntrl)*self.delay,self.resp,self.rt)).T
                    df.columns = ['sub','mem','prb','iti','stimdur','delay','resp','rt']
                    timestr = time.strftime("%Y%m%d-%H%M%S")
                    df.to_csv('data/subj_' + str(subj) + '_' + timestr +'_roll.csv')
                    
                    self.mesh.destroy()
                    pg.quit()
                    sys.exit()

    # render
    def render(self):
        # clear framebuffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        # render scene
        # self.scene.update()
        self.scene.render()
        # swap buffers
        pg.display.flip()
        

    # if want to get time
    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def initScene(self):
        self.scene.clear()
        Scene.r = self.mem[self.condid]
        self.scene.load()

    # actually running!
    def run(self):
        
        global resp,timer

        resp = 0
        timer = self.iti[self.condid];

        self.initScene()

        while True:

            self.get_time()
            self.check_events()
            # self.camera.update()

            if resp == 0:
                if timer<0: # prestim
                    self.scene.clear()
                elif timer<self.stimdur: # stim
                    self.initScene()
                elif timer<(self.delay+self.stimdur): # delay
                    self.scene.clear()
                else: # response
                    Scene.r = self.prb[self.condid]
                    self.scene.load()
                    resp = 1;
                    self.condid += 1;
            else:
                self.scene.update()
                
            self.render()
            self.delta_time = self.clock.tick(60)
            timer += self.clock.tick(60)* 0.001

if __name__ == '__main__':

    #myDlg = gui.Dlg(title="CC3D experiment")
    #myDlg.addText('Subject info')
    #myDlg.addField('Name:')
    #ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
    
    #if myDlg.OK:  # or if ok_data is not None
    
    app = GraphicsEngine()
    app.run()

    #subj = myDlg.data[0];
    
    #else:
        #print('user cancelled')

    






























