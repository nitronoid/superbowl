#!/usr/bin/python

import sys
import maya.OpenMaya as om


def get_selection_it():
    # get the active selection
    selection = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(selection)
    return om.MItSelectionList(selection, om.MFn.kMesh)


def get_face_it(obj_it):
    # get dagPath
    dag_path = om.MDagPath()
    obj_it.getDagPath(dag_path)
    return om.MItMeshPolygon(dag_path)


def mpoint_to_tuple(maya_point):
    return tuple([maya_point[0], maya_point[1], maya_point[2]])


def index_map(pset):
    imap = {}
    i = 0
    for p in pset:
        imap[p] = i
        i += 1
    return imap


def face_index(face_list, point_index):
    face_index_list = []
    for f in face_list:
        face = []
        for p in f:
            face.append(point_index[p])
        face_index_list.append(tuple(face))
    return face_index_list


def get_mesh_data():
    # get an iterator for all selected objects
    selected_obj_it = get_selection_it()

    # iterate over all selected
    while not selected_obj_it.isDone():
        # get an iterator for this objects faces
        maya_face_it = get_face_it(selected_obj_it)

        # create arrays to store faces and points
        face_list = []
        point_set = set()
        n_face_verts = []

        while not maya_face_it.isDone():
            # create a maya point array to store data
            maya_point_arr = om.MPointArray()
            # get the points of this face
            maya_face_it.getPoints(maya_point_arr)

            face = []
            # convert all maya points into tuples and store in our lists
            for i in range(maya_point_arr.length()):
                point = mpoint_to_tuple(maya_point_arr[i])
                face.append(point)
                point_set.add(point)

            face_list.append(face)
            n_face_verts.append(maya_point_arr.length())
            # next face
            maya_face_it.next()

        # map points to their index in the set
        point_dict = index_map(point_set)

        # create a point indexing list of faces
        face_index_list = face_index(face_list, point_dict)

        # return all useful info
        return point_set, face_list, face_index_list, n_face_verts


def pretty_out(n_verts, face_index_list, point_list, tab_ammount):
    tabs = '\t' * tab_ammount
    pretty = ['[' + ' '.join([str(x) for x in n_verts]) + ']',
              '[' + ' '.join(map(str, [x for t in face_index_list for x in t])) + ']',
              '"P"',
              '[' + ' '.join(map(str, [x for t in point_list for x in t])) + ']'
              ]
    return tabs + ('\n' + tabs).join(pretty)


def mesh_to_rib(file_name):
    # gather data about selected meshes
    pl, fl, fil, nfv = get_mesh_data()
    out_file = open(file_name, "w")
    out_file.write('AttributeBegin\n\tTransformBegin\n\t\tSubdivisionMesh "catmull-clark"\n')
    out_file.write(pretty_out(nfv, fil, pl, 2))
    out_file.write('\n\tTransformEnd\nAttributeEnd')
    out_file.close()
