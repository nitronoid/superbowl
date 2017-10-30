import maya.OpenMaya as OpenMaya
 
def convertMeshToRib(  ):
    # get the active selection
    selection = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(selection)
    iterSel = OpenMaya.MItSelectionList(selection, OpenMaya.MFn.kMesh)

    # go througt selection
    while not iterSel.isDone():

        # get dagPath
        dagPath = OpenMaya.MDagPath()
        iterSel.getDagPath( dagPath )

        # create empty point array
        inMeshMPointArray = OpenMaya.MPointArray()

        # create function set and get points in world space
        currentInMeshMFnMesh = OpenMaya.MFnMesh(dagPath)
        currentInMeshMFnMesh.getPoints(inMeshMPointArray, OpenMaya.MSpace.kWorld)
        mFaceIt = OpenMaya.MItMeshPolygon(dagPath)

        # create arrays to store faces and points
        faceList = []
        pointList = []
        nFaceVerts = []

        while not mFaceIt.isDone():
            # create a maya point array to store data
            mayaPoint = OpenMaya.MPointArray()
            # get the points of this face
            mFaceIt.getPoints(mayaPoint)
            
            p = []
            # convert all maya points into tuples and store in our lists
            for i in range(mayaPoint.length()) :
                p.append((mayaPoint[i][0], mayaPoint[i][1], mayaPoint[i][2]))
                pointList.append((mayaPoint[i][0], mayaPoint[i][1], mayaPoint[i][2]))
            faceList.append(p)
            nFaceVerts.append(mayaPoint.length())
            # next face
            mFaceIt.next()
            
        # make the point list unique
        pointList = list(set(pointList))

        pointDict = {}
        i = 0
        for p in pointList:
            pointDict[p] = i
            i += 1

        faceIndexList = []    
        for f in faceList:
            face = []
            for p in f:
                face.append(pointDict[p])
            faceIndexList.append(tuple(face))

        return pointList, faceList, faceIndexList, nFaceVerts

pl, fl, fil, nfv = convertMeshToRib()

print '['+' '.join([str(x) for x in nfv]) +']'
print '['+' '.join(map(str,[x for t in pl for x in t])) +']'
print '['+' '.join(map(str,[x for t in fil for x in t])) +']'
