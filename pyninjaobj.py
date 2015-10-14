# The MIT License (MIT)

# Copyright (c) 2015 Luke Gaynor

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from collections import namedtuple
from pprint import pprint
import struct
import array

HEADER = """# Converted with PyNinjaObj '.rip' to '.obj' converter"""
DEFAULT_MAT = """Ka 0.000000 0.000000 0.000000\nKd 0.376320 0.376320 0.376320\nKs 0.000000 0.000000 0.000000"""

class Vector3():
    """A 3D point"""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "({},{},{})".format(self.x, self.y, self.z)

class Vector2():
    """A 2D point"""
    def __init__(self, u, v):
        self.u = u
        self.v = v

    def __repr__(self):
        return "({},{})".format(self.u, self.v)


def read_str(filehandle):
    buf = b''
    while True:
        byte = filehandle.read(1)
        if byte != b'\0':
            buf += byte
        else:
            break
    return buf.decode("ASCII")

class RipMesh():
    def __init__(self, ripfile):
        v_idx = Vector3(0,0,0)
        vn_idx = Vector3(0,0,0)
        vt_idx = Vector2(0,0)

        rip = open(ripfile, "rb")

        info_header = array.array("L")
        info_header.fromfile(rip, 8)

        signature = info_header[0]
        version = info_header[1]
        face_count = info_header[2]
        vertex_count = info_header[3]
        vertex_size = info_header[4]
        texture_file_count = info_header[5]
        shader_file_count = info_header[6]
        vertex_attribute_count = info_header[7]

        print(version,face_count,vertex_count,vertex_size,texture_file_count,shader_file_count,vertex_attribute_count)

        if signature != 0xDEADC0DE:
            raise NotImplementedError("Sorry, this file signature isn't recognised.")

        if version != 4:
            print("Warning: This tool was written for version 4 .rip files, not version", version)

        pos_idx = 0
        normal_idx = 0
        uv_idx = 0

        vertex_attrib_types = []

        for i in range(0, vertex_attribute_count):
            attrib_type = read_str(rip)
            # print("oo",attrib_type,"<ye")

            attrib_info = array.array("L")
            attrib_info.fromfile(rip, 4)

            attrib_idx = attrib_info[0]
            attrib_offset = attrib_info[1]
            attrib_size = attrib_info[2]
            attrib_element_count = attrib_info[3]

            vertex_attrib = array.array("L")
            vertex_attrib.fromfile(rip, attrib_element_count)

            vertex_attrib_types.extend(vertex_attrib)

            # print(pos_idx, normal_idx, uv_idx, vertex_attrib)
            if attrib_type == "POSITION" and pos_idx == 0:
                v_idx.x = attrib_offset // 4
                v_idx.y = v_idx.x + 1
                v_idx.z = v_idx.x + 2
                # print("adding pos", v_idx)
                pos_idx += 1

            elif attrib_type == "NORMAL" and normal_idx == 0:
                vn_idx.x = attrib_offset // 4
                vn_idx.y = vn_idx.x + 1
                vn_idx.z = vn_idx.x + 2
                # print("adding norm", vn_idx)
                normal_idx += 1

            elif attrib_type == "TEXCOORD" and uv_idx == 0:
                vt_idx.u = attrib_offset // 4
                vt_idx.v = vt_idx.u + 1
                # print("adding uv", vt_idx)
                uv_idx += 1

        self.texture_files = []
        for i in range(0, texture_file_count):
            self.texture_files.append(read_str(rip))
        print(self.texture_files)

        self.shader_files = []
        for i in range(0, shader_file_count):
            self.shader_files.append(read_str(rip))

        self.faces = []
        for x in range(0, face_count):
            face = array.array("L")
            face.fromfile(rip, 3)
            self.faces.append(face)

        self.vertices = []
        self.normals = []
        self.texcoords = []

        for i in range(0, vertex_count):
            v = Vector3(0,0,0)
            vn = Vector3(0,0,0)
            vt = Vector2(0,0)

            for j,element_type in enumerate(vertex_attrib_types):
                pos = 0
                # print(rip.tell())
                # print(element_type)
                if element_type == 0:
                    pos, = struct.unpack("f", rip.read(struct.calcsize("f")))
                elif element_type == 1:
                    pos, = struct.unpack("L", rip.read(struct.calcsize("L")))
                elif element_type == 2:
                    pos, = struct.unpack("l", rip.read(struct.calcsize("l")))

                if j == v_idx.x:
                    v.x = pos
                elif j == v_idx.y:
                    v.y = pos
                elif j == v_idx.z:
                    v.z = pos
                elif j == vn_idx.x:
                    vn.x = pos
                elif j == vn_idx.y:
                    vn.y = pos
                elif j == vn_idx.z:
                    vn.z = pos
                elif j == vt_idx.u:
                    vt.u = pos
                    # print(vt)
                elif j == vt_idx.v:
                    vt.v = 1 - pos

            self.vertices.append(v)
            self.normals.append(vn)
            self.texcoords.append(vt)

        print("Finished reading mesh file")
        rip.close()

def riptoobj(ripfiles, outdir, tga=False, name="convert", exists=False):
    meshes = []
    for ripfile in ripfiles:
        meshes.append(RipMesh(ripfile))

    print("Making OBJ and MTL files")
    objname = outdir + name + ".obj"
    mtlname = outdir + name + ".mtl"

    texset = set()
    for mesh in meshes:
        for tex in mesh.texture_files:
            if tga:
                tex = tex[:-4] + ".tga" # .dds to .tga

            if exists and not os.path.isfile(os.path.join(outdir, tex)):
                # print("Ignoring nonexistant", tex)
                continue
            texset.add(tex)

    pprint(texset)

    objlines = []
    mtllines = []

    objlines.append(HEADER)
    if len(texset) > 0:
        # only need to make an mtl if theres textures
        objlines.append("mtllib " + mtlname)
        mtllines.append(HEADER)

        for tex in texset:
            mtllines.append("newmtl " + tex)
            mtllines.append(DEFAULT_MAT)
            mtllines.append("map_Kd " + tex)
            mtllines.append("")

        last_idx = None

        for idx,mesh in enumerate(meshes):
            objlines.append("o Object" + str(idx))
            for tex in mesh.texture_files:
                if tga:
                    tex = tex[:-4] + ".tga"

                if exists and not os.path.isfile(os.path.join(outdir, tex)):
                    continue # ignore nonexistant materials if specified
                objlines.append("usemtl " + tex)

            for v in mesh.vertices:
                objlines.append("v {} {} {}".format(v.x, v.y, v.z))

            for vn in mesh.normals:
                objlines.append("vn {} {} {}".format(vn.x, vn.y, vn.z))

            for vt in mesh.texcoords:
                objlines.append("vt {} {}".format(vt.u, vt.v))

            if not last_idx:
                last_idx = 1

            highest_idx = 0
            for face in mesh.faces:
                line = ["f"]

                for v in face:
                    v += last_idx
                    highest_idx = v if v > highest_idx else highest_idx
                    line.append("{}/{}/{}".format(v,v,v))
                objlines.append(" ".join(line))

            last_idx = highest_idx+1
            # print(len(mesh.faces), len(mesh.vertices), last_idx)

    with open(objname, "w") as obj:
        obj.write("\n".join(objlines))

    with open(mtlname, "w") as mtl:
        mtl.write("\n".join(mtllines))

    # for tex in mesh.texture_files:
    #     if tga:
    #         tex = tex[:-4] + ".tga"

    # print(vertices)
    # print(normals)
    # print(uvs)
if __name__ == '__main__':
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Converts NinjaRipper .rips into .objs")
    parser.add_argument("rip_path", help="path to the folder containing rip files")

    # parser.add_argument("-o","--output", nargs=1, help="output path and name (not including)")
    parser.add_argument("--tga", help="look for tga textures", action='store_true')
    parser.add_argument("--exists", "-e", help="only include materials for which their texture files exist", action='store_true')
    # parser.add_argument("--whitelist_suffix", "-w", help="only include material's with these suffixes", nargs="+")

    args = parser.parse_args()

    indir = os.path.normpath(args.rip_path)
    out = args.rip_path+os.path.sep

    print("Saving to", os.path.realpath(out))

    paths = []
    for f in os.listdir(indir):
        if f.endswith(".rip"):
            paths.append(indir+os.path.sep+f)

    riptoobj(paths, out, tga=args.tga, exists=args.exists)
