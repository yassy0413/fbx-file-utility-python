# fbx-file-utility-python
Fast convert fbx files in target directory to binary or ascii. or find.

対象フォルダ内にある全てのfbxファイルを、
バイナリフォーマット又はアスキーフォーマットに変換します。

もしくは、対象のフォーマットであるfbxファイルを
検索することができます。

# Setup

## FBX Python Bindings

[Installing Python FBX](http://help.autodesk.com/view/FBX/2020/ENU/?guid=FBX_Developer_Help_scripting_with_python_fbx_installing_python_fbx_html)

[Latest FBX SDK](https://www.autodesk.com/products/fbx/overview) -> GET FBX SDK -> FBX Python Bindings

# Usage

## Convert FBX Binary format to FBX ASCII format
```bash
python fbx_file_format_utility.py -d TARGET_PATH -c -a
```

## Convert FBX ASCII format to FBX Binary format
```bash
python fbx_file_format_utility.py -d TARGET_PATH -c -b
```

## Find FBX Files of ASCII format
```bash
python fbx_file_format_utility.py -d TARGET_PATH -v -a
```

## Find FBX Files of Binary format
```bash
python fbx_file_format_utility.py -d TARGET_PATH -v -b
```

## Force set export fbx file version
```bash
# Export FBXVersion: 7500
python fbx_file_format_utility.py -d TARGET_PATH -v -b -f FBX201600
# Export FBXVersion: 7200
python fbx_file_format_utility.py -d TARGET_PATH -v -b -f FBX201200
```
see [fbxio.h](http://help.autodesk.com/view/FBX/2020/ENU/?guid=FBX_Developer_Help_cpp_ref_fbxio_8h_html)
