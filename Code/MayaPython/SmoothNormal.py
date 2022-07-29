import maya.cmds as cmds
import maya.OpenMaya as om


def createWindow():
    if cmds.window('mywindow', exists=True):
        cmds.deleteUI('mywindow')
    windowvar = cmds.window('mywindow')
    cmds.columnLayout()
    cmds.button(l='Create', command='createFunc()')
    cmds.button(l='Normal', command='normalToColor()')
    cmds.showWindow('mywindow')

def createFunc():
    cubeList = cmds.ls('myCube')
    if len(cubeList) > 0:
        cmds.delete(cubeList)
    pCube = cmds.polyCube(w=10, h=10, d=10, name='myCube')

def normalToColor():
    selectionList = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(selectionList)
    iterator = om.MItSelectionList(selectionList)
    dagPath = om.MDagPath()
    target = om.MObject()
    nodeFn = om.MFnDagNode()

    iterator.reset()
    print iterator
    while not iterator.isDone():
        print iterator
        iterator.getDagPath(dagPath, target)
        nodeFn.setObject(dagPath)
        if(not dagPath.hasFn(om.MFn.kMesh)):
            iterator.next()
            continue

        mfnMesh = om.MFnMesh(dagPath)
        vertexIterator = om.MItMeshVertex(dagPath, target)
        space = om.MSpace.kWorld

        # init
        print 'init'
        normals = om.MFloatVectorArray()
        tangents = om.MFloatVectorArray()
        biTangents = om.MFloatVectorArray()
        mfnMesh.getNormals(normals)
        mfnMesh.getTangents(tangents)
        mfnMesh.getBinormals(biTangents)

        colors = om.MColorArray()
        # clear
        print 'clear'
        colorSets = []
        mfnMesh.getColorSetNames(colorSets)
        if(colorSets.count > 0):
            for name in colorSets:
                mfnMesh.deleteColorSet(name, None, selectionList)

        # re create
        print 're create'
        colorSetName = 'ColorSet1'
        angleWeight = False
        mfnMesh.createColorSetWithName(colorSetName)
        mfnMesh.setCurrentColorSetName(colorSetName)

        # world normal
        smoothNormals = om.MFloatVectorArray()
        mfnMesh.getVertexNormals(angleWeight, smoothNormals, space)
        vertNum = smoothNormals.length()

        ids = om.MIntArray()
        while not vertexIterator.isDone():
            vertID = vertexIterator.index()
            ids.append(vertID)
            tempNormal = om.MFloatVector(0,0,0)
            tempNormal = smoothNormals[vertID]
            tempNormal.normalize()

            normalColor = om.MColor(tempNormal.x, tempNormal.y, tempNormal.z, 1)
            print normalColor
            colors.append(normalColor)
            vertexIterator.next()

        mfnMesh.setVertexColors(colors, ids)

        # to tangent space
        print 'tangent'
        index = 1
        vertColors = om.MColorArray()
        mfnMesh.getVertexColors(vertColors)
        colors.clear()
        faceVertIterator = om.MItMeshFaceVertex(dagPath, target)
        while not faceVertIterator.isDone():
            faceID = faceVertIterator.faceId()
            vertID = faceVertIterator.vertId()
            faceVertColor = vertColors[vertID]

            tangentID = mfnMesh.getTangentId(faceID, vertID)
            tangent = tangents[tangentID]
            bitangent = biTangents[tangentID]
            normal = om.MVector()
            faceVertIterator.getNormal(normal)

            smoothNormal = om.MVector(faceVertColor[0], faceVertColor[1], faceVertColor[2])
            # TBN
            x = smoothNormal * om.MVector(tangent[0], tangent[1], tangent[2])
            y = smoothNormal * om.MVector(bitangent[0], bitangent[1], bitangent[2])
            z = smoothNormal * om.MVector(normal[0], normal[1], normal[2])

            normalizeColor = om.MColor()
            normalizeColor.r = x * 0.5 + 0.5
            normalizeColor.g = y * 0.5 + 0.5
            normalizeColor.b = z * 0.5 + 0.5
            normalizeColor.a = 1
            print normalizeColor
            mfnMesh.setFaceVertexColor(normalizeColor, faceID, vertID)

            index += 1
            faceVertIterator.next()

        iterator.next()
    cmds.polyColorPerVertex(colorDisplayOption=True)
createWindow()