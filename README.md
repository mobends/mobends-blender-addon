# Mo' Bends Blender Addon
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/powered-by-oxygen.svg)](https://forthebadge.com)

This script is an addon for Blender. It exports animation data in JSON. The exported files can then be used for making custom BendsPacks for the Minecraft Mo' Bends mod, or for any other animation related project.

# Installation

To install this addon into Blender, just download the latest release .zip package, which should be
[this one](https://github.com/mobends/mobends-blender-addon/releases/download/v0.1/io_anim_mobends_0.1.zip).

In Blender, open up `Preferences`, and in the addons tab use the `Install...` action.
There should be plenty of tutorials on how to install Blender addons out there, I'm sure you'll figure it out <3.

# Format
```jsonc
{
    // This holds the version of the format.
    "version": "${version_of_format}"
    // This holds the version of Blender that this has been generated with.
    "meta": "${version_of_blender}",
    // This holds a dictionary of armatures
    "armatures": {
        "${name_of_armature}": {
            "bones": {
                "${bone_name}": {
                      "keyframes": [
                          {
                              "position": [ 1.0, 2.0, 3.0 ],
                              "rotation": [ 0.0, 0.0, 0.0, 1.0 ],
                              "scale": [ 1.0, 1.0, 1.0 ]
                          }
                          ...
                      ] // end keyframes
                },
                ...
            } // end bones
        },
        ...
    } // end armatures
}
```
