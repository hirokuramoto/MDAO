#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.3.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
sys.path.insert(0, r'/home/kura1/OpenFOAM/kura1-v1912/run/airFoil2D/optimize')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
Pad = geompy.ImportSTEP("/home/kura1/OpenFOAM/kura1-v1912/run/airFoil2D/cad/original_model.step", False, True)
inlet = geompy.CreateGroup(Pad, geompy.ShapeType["FACE"])
geompy.UnionIDs(inlet, [27])
outlet = geompy.CreateGroup(Pad, geompy.ShapeType["FACE"])
geompy.UnionIDs(outlet, [13])
wall = geompy.CreateGroup(Pad, geompy.ShapeType["FACE"])
geompy.UnionIDs(wall, [20, 3])
wall_empty = geompy.CreateGroup(Pad, geompy.ShapeType["FACE"])
geompy.UnionIDs(wall_empty, [62, 59])
wing = geompy.CreateGroup(Pad, geompy.ShapeType["FACE"])
geompy.UnionIDs(wing, [48, 55, 31, 41])
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Pad, 'Pad' )
geompy.addToStudyInFather( Pad, inlet, 'inlet' )
geompy.addToStudyInFather( Pad, outlet, 'outlet' )
geompy.addToStudyInFather( Pad, wall, 'wall' )
geompy.addToStudyInFather( Pad, wall_empty, 'wall_empty' )
geompy.addToStudyInFather( Pad, wing, 'wing' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                 # multiples meshes built in parallel, complex and numerous mesh edition (performance)

Mesh_1 = smesh.Mesh(Pad)
NETGEN_1D_2D_3D = Mesh_1.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
NETGEN_3D_Parameters_1 = NETGEN_1D_2D_3D.Parameters()
NETGEN_3D_Parameters_1.SetMaxSize( 0.002 )
NETGEN_3D_Parameters_1.SetMinSize( 0.0001 )
NETGEN_3D_Parameters_1.SetSecondOrder( 0 )
NETGEN_3D_Parameters_1.SetOptimize( 1 )
NETGEN_3D_Parameters_1.SetFineness( 3 )
NETGEN_3D_Parameters_1.SetChordalError( -1 )
NETGEN_3D_Parameters_1.SetChordalErrorEnabled( 0 )
NETGEN_3D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_3D_Parameters_1.SetFuseEdges( 1 )
NETGEN_3D_Parameters_1.SetQuadAllowed( 0 )
NETGEN_3D_Parameters_1.SetCheckChartBoundary( 64 )
#Viscous_Layers_1 = NETGEN_1D_2D_3D.ViscousLayers(0.001,4,1,[ 48, 55, 31, 41 ],0,smeshBuilder.SURF_OFFSET_SMOOTH)
#Viscous_Layers_1.SetTotalThickness( 0.001 )
#Viscous_Layers_1.SetNumberLayers( 4 )
#Viscous_Layers_1.SetStretchFactor( 1 )
#Viscous_Layers_1.SetMethod( smeshBuilder.SURF_OFFSET_SMOOTH )
#Viscous_Layers_1.SetFaces( [ 48, 55, 31, 41 ], 0 )
isDone = Mesh_1.Compute()
inlet_1 = Mesh_1.GroupOnGeom(inlet,'inlet',SMESH.FACE)
outlet_1 = Mesh_1.GroupOnGeom(outlet,'outlet',SMESH.FACE)
wall_1 = Mesh_1.GroupOnGeom(wall,'wall',SMESH.FACE)
wall_empty_1 = Mesh_1.GroupOnGeom(wall_empty,'wall_empty',SMESH.FACE)
wing_1 = Mesh_1.GroupOnGeom(wing,'wing',SMESH.FACE)
try:
  Mesh_1.ExportUNV( r'/home/kura1/OpenFOAM/kura1-v1912/run/airFoil2D/Mesh_1.unv' )
  pass
except:
  print('ExportUNV() failed. Invalid file name?')


## Set names of Mesh objects
smesh.SetName(NETGEN_1D_2D_3D.GetAlgorithm(), 'NETGEN 1D-2D-3D')
smesh.SetName(NETGEN_3D_Parameters_1, 'NETGEN 3D Parameters_1')
#smesh.SetName(Viscous_Layers_1, 'Viscous Layers_1')
smesh.SetName(inlet_1, 'inlet')
smesh.SetName(outlet_1, 'outlet')
smesh.SetName(wall_1, 'wall')
smesh.SetName(wall_empty_1, 'wall_empty')
smesh.SetName(wing_1, 'wing')
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
