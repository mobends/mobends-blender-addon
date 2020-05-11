# Mo' Bends Blender Addon
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/powered-by-oxygen.svg)](https://forthebadge.com)

This script is an addon for Blender. It exports animation data in a custom binary format. The exported files can then be used for making custom BendsPacks for the Minecraft Mo' Bends mod, or for any other animation related project.

# Installation

To install this addon into Blender, just download the latest release .zip package, which should be
[this one](https://github.com/mobends/mobends-blender-addon/releases/download/v0.1/io_anim_mobends_0.1.zip).

In Blender, open up `Preferences`, and in the addons tab use the `Install...` action.
There should be plenty of tutorials on how to install Blender addons out there, I'm sure you'll figure it out <3.

# Format
All values are encoded in big endian.
```ebnf
(* basic building blocks *)
digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
hexdigit = digit | "A" | "B" | "C" | "D" | "E" | "F" ;

byte = hexdigit * 2 ;
nonzero byte = byte - "00" ;
int = byte * 4 ;
float = byte * 4 ;
string = { nonzero byte }, "\0" ;

(* properties *)
version = int ;
amount of bones = int ;
amount of frames = int ;
(*
    bit 1 determines if position is encoded
    bit 2 determines if rotation is encoded
    bit 3 determines if scale is encoded
*)
property flags = byte ;

position = float * 3 ;
rotation = float * 4 ;
scale = float * 3 ;
frame = property flags, [ position ], [ rotation ], [ scale ] ;
bone = string, { frame } ;

(* structure of the whole file *)
file = version,
       amount of bones,
       amount of frames,
       { bone } ;

```
