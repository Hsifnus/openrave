# -*- coding: utf-8 -*-
# Copyright (C) 2011 Rosen Diankov <rosen.diankov@gmail.com>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from openravepy import *
from numpy import *

g_epsilon = 1e-7
g_jacobianstep = 0.01
g_envfiles = ['data/lab1.env.xml','data/pr2wam_test1.env.xml','data/hanoi_complex.env.xml']
g_robotfiles = ['robots/pr2-beta-static.zae','robots/barrettsegway.robot.xml','robots/neuronics-katana.zae']

def setup_module(module):
    RaveInitialize(load_all_plugins=True)
    
def teardown_module(module):
    RaveDestroy()

def transdist(list0,list1):
    return sum([sum(abs(item0-item1)) for item0, item1 in izip(list0,list1)])

def axisangledist(axis0,axis1):
    return arccos(numpy.minimum(1.0,abs(dot(quatFromAxisAngle(axis0),quatFromAxisAngle(axis1)))))

def randtrans():
    T = matrixFromAxisAngle(random.rand(3)*6-3)
    T[0:3,3] = random.rand(3)-0.5            
    return T

def randquat(N=1):
    L = 0
    while any(L == 0):
        q = random.rand(N,4)-0.5
        L = sqrt(sum(q**2,1))
    return q/tile(L,(4,1)).transpose()

def randpose(N=1):
    poses = random.rand(N,7)-0.5
    poses[:,0:4] /= tile(sqrt(sum(poses[:,0:4]**2,1)),(4,1)).transpose()
    return poses

def randlimits(lower,upper):
    return lower+random.rand(len(lower))*(upper-lower)

def bodymaxjointdist(link,localtrans):
    body = link.GetParent()
    joints = body.GetChain(0,link.GetIndex(),returnjoints=True)
    baseanchor = joints[0].GetAnchor()
    eetrans = transformPoints(link.GetTransform(),[localtrans])
    armlength = 0
    for j in body.GetDependencyOrderedJoints()[::-1]:
        armlength += sqrt(sum((eetrans-j.GetAnchor())**2))
        eetrans = j.GetAnchor()    
    return armlength

class EnvironmentSetup(object):
    def setup(self):
        self.env=Environment()
        self.env.StopSimulation()
        RaveSetDebugLevel(Level_Debug|Level_VerifyPlans)
    def teardown(self):
        self.env.Destroy()
        self.env=None
