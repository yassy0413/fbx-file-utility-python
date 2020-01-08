# -*- coding: utf-8 -*-
"""
FBX File Format Utility

Notes
-----
Install FBX SDK)
  http://help.autodesk.com/view/FBX/2020/ENU/?guid=FBX_Developer_Help_scripting_with_python_fbx_installing_python_fbx_html
Latest FBX SDK)
  https://www.autodesk.com/products/fbx/overview -> GET FBX SDK -> FBX Python Bindings
ref)
  https://github.com/segurvita/fbx_sdk_python_sample

"""
import os
import sys
import argparse
import concurrent.futures

from fbx import FbxManager
from fbx import FbxScene
from fbx import FbxImporter
from fbx import FbxExporter

def _build_arguments():
    parser = argparse.ArgumentParser(description='A')
    parser.add_argument('-d', '--target_dir', help='A')
    parser.add_argument('-b', '--binary', help='Target file format is binary', action='store_true')
    parser.add_argument('-a', '--ascii', help='Target file format is ascii', action='store_true')
    parser.add_argument('-v', '--verify', help='A', action='store_true')
    parser.add_argument('-c', '--convert', help='A', action='store_true')
    args = parser.parse_args()

    if args.target_dir is None:
        print(u'Required target directory')
        sys.exit(1)

    if args.binary == args.ascii:
        print(u'Required file format -b(binary) or -a(ascii)')
        sys.exit(1)

    if args.verify == args.convert:
        print(u'Required method -c(convert) or -v(verify)')
        sys.exit(1)

    return args

# https://code.blender.org/2013/08/fbx-binary-file-format-specification/
# https://wiki.fileformat.com/3d/fbx/
FBX_BINARY_SIGNATURE = b"Kaydara FBX Binary  \x00\x1A\x00"
FBX_BINARY_SIGNATURE_LENGTH = len(FBX_BINARY_SIGNATURE)

FBX_MANAGER = FbxManager.Create()
ARGS = _build_arguments()

def _get_file_fomrat(format_name):
    io_plugin_registry = FBX_MANAGER.GetIOPluginRegistry()
    for format_id in range(io_plugin_registry.GetWriterFormatCount()):
        if io_plugin_registry.WriterIsFBX(format_id):
            desc = io_plugin_registry.GetWriterFormatDescription(format_id)
            if format_name in desc:
                return format_id
    # Default format is auto
    return -1

def _is_binary_fbx(path):
    with open(path, 'rb') as file:
        return file.read(FBX_BINARY_SIGNATURE_LENGTH) == FBX_BINARY_SIGNATURE
    return False

def _verify(path):
    if _is_binary_fbx(path) == ARGS.binary:
        print(path)

def _convert(path, file_format_id):
    if _is_binary_fbx(path) != ARGS.binary:
        print(path)
        scene = FbxScene.Create(FBX_MANAGER, "")
        importer = FbxImporter.Create(FBX_MANAGER, "")
        importer.Initialize(path, -1)
        importer.Import(scene)
        importer.Destroy()
        exporter = FbxExporter.Create(FBX_MANAGER, "")
        exporter.Initialize(path, file_format_id)
        exporter.Export(scene)
        exporter.Destroy()
        scene.Destroy()

def _main():
    format_name = 'binary' if ARGS.binary else 'ascii'
    file_format_id = _get_file_fomrat(format_name)

    print(u'directory: ' + ARGS.target_dir)
    if ARGS.verify:
        print(u'find ' + format_name + u' fbx files...')
    else:
        print(u'convert to ' + format_name + u'...')

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for root, _dirs, files in os.walk(ARGS.target_dir):
            for filename in files:
                _title, ext = os.path.splitext(filename)
                if ext == '.fbx':
                    path = os.path.join(root, filename)
                    if ARGS.verify:
                        executor.submit(_verify, path)
                    else:
                        executor.submit(_convert, path, file_format_id)

if __name__ == "__main__":
    _main()
