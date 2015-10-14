# pyninjaobj
A simple Python script which takes Ninjaripper model dumps and converts them into an obj


## Requirements
The script should only require Python 3, and even then would be trivial to move to support Python 2.

## Usage
Assuming Python has been installed, you can invoke this script with the following in a command line/terminal:

  `python pyninjaobj.py [path to folder containing .rip files]`

If Python has been associated with `.py` files, you can also just drag and drop a `rip` folder onto the script to run it.

An `.obj` and accompanying `.mtl` file should be created inside of the `rip` folder. You can import the `.obj` into your favourite 3D editor to inspect/edit/export it.

## Usage for Dawn of War rips
A lot of you guys will be using this for converting rips from Dawn of War, so to help give users having trouble a little help, I've included a Windows `.bat` file; ``dow_rip.bat``.

All the batch file does is run the script as follows:

    python pyninjaobj.py --tga --exists [drag and dropped folder]

This means **it expects that the textures you wish to use are in `.tga` format, and that they exist**. Any textures that aren't there or aren't in the `.tga` format will be ignored completely.

To convert a typical rip from Dawn of War's army painter:

1. Use IrfanView (See below) or Photoshop or GIMP to convert *only* the `.dds` textures which are normal colour (diffuse texture maps). Usually these have names which end in `_1`, but its safer to check by eye.
2. Drag and drop the rip folder onto `dow_rip.bat`.
3. Import the `convert.obj` into Blender, fix weird rotations and positions, you're done!

#### Example of step one using IrfanView:
![IrfanView Thumbnails](https://i.imgur.com/2hkioEx.png)
*By drag and dropping the rip folder onto IrfanView, I can see all the textures at once. I've selected only the colour diffuse maps here. Note the similar looking other texture maps -- we just want the diffuse ones.*

![IrfanView Batch Conversion](https://i.imgur.com/QCGKLCu.png)
*By right clicking and selecting "Start batch dialog with selected files..." I'm shown this window. The important things to note is the Output Format and clicking "Use current (look in)`directory"*

## Arguments
    usage: pyninjaobj.py [-h] [--tga] [--exists] rip_path

    Converts NinjaRipper .rips into .objs

    positional arguments:
      rip_path      path to the folder containing rip files

    optional arguments:
      -h, --help    show this help message and exit
      --tga         look for tga textures
      --exists, -e  only include materials for which their texture files exist

## Notes *on things I have no control over*
NinjaRipper can't know any mesh object names, hence the bland naming of components. Sorry.

In Dawn of War's army painter, many models (especially those in mods) have details added in a way that mess up positioning and rotation in Ninjaripper. This isn't the scripts fault, you'll just have to fix them yourself in Blender. Sorry.

Neither can it differentiate between multiple textures on a single mesh component. Also sorry.

Additionally, it will import **all** a ripped model's textures, which can include non-diffuse ones such as emissive and specular maps -- you will have to clear these out yourself. *Sorry.*
