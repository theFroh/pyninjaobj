# pyninjaobj
A simple Python script which takes Ninjaripper model dumps and converts them into an obj


## Requirements
The script should only require Python 3, and even then would be trivial to move to support Python 2.

## Usage
Assuming Python has been installed, you can invoke this script with the following in a command line/terminal:

  `python pyninjaobj.py [path to folder containing .rip files]`

If Python has been associated with `.py` files, you can also just drag and drop a `rip` folder onto the script to run it.

An `.obj` and accompanying `.mtl` file should be created inside of the `rip` folder. You can import the `.obj` into your favourite 3D editor to inspect/edit/export it.

## Notes *on things I have no control over*
NinjaRipper can't know any mesh object names, hence the bland naming of components. Sorry.

Neither can it differentiate between multiple textures on a single mesh component. Also sorry.

Additionally, it will import **all** a ripped model's textures, which can include non-diffuse ones such as emissive and specular maps -- you will have to clear these out yourself. *Sorry.*
