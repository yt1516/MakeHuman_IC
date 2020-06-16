# Instructions

This repository contains a full **windows** version of **MakeHuman 1.1.1**.  

For the vanilla version, please go to [the official MakeHuman website](http://www.makehumancommunity.org/content/downloads.html)

# Usage

Clone or download this repository, double click the **makehuman.exe** file to run the application. 


## Controls

 - Rotation: Hold and drag with the **left mouse button**.
 - Panning: Hold and drag with the **scroll wheel**.
 - Zoom: **Scroll wheel**.
 - Quick zoom: Hold and drag with the **right mouse button**.


## Model Structure

The human avatar is composed of **multiple separate meshes**. 

The **base mesh** is the body, *excluding* eyeballs, tongues, teeth, eyebrows, eyelashes and hair, which may be added separately.

## Demography Mesh

The default control tab allows customisation of the demographic features of the avatar. 

Click and drag the sliders on the left panel to edit the **base mesh** of demography-related body and face ratios.

## Demography Appearance

Navigate to **Materials** on the control tab to select a skin for the **base mesh** of the avatar.

Navigate to **Geometries** to add or change **peripherals meshes**, including clothes, eye colours, hair style, teeth, eyebrow styles, eyelashes, and tongue. 

**Topologies**: Leave topology as **None** unless specific body types (muscular) or organs (genitalia) are required. 

**Conflicts between the macro base mesh and topology mesh may cause rendering issues.**

## Plugins

Navigate to **Settings** and select **Plugins**. Tick the plugins to use. 

Two plugins are included in this package: **mhx2** and **FACSHuman**, and both are enabled by default.

FACSHuman is a Facial Action Coding System (FACS) based facial expression generation plugin that allows individual action unit (AU) intensity controls. Please refer to [The FACS Guidebook](https://imotions.com/blog/facial-action-coding-system/), and [Tian et al. 2001](https://ieeexplore.ieee.org/document/908962) for more information about FACS.

MHX2 is a custom file saving plugin to interface MakeHuman with Blender. It transfers body and face rigs from MakeHuman to Blender. 


Original repositories:

FACSHuman: [https://github.com/montybot/FACSHuman](https://github.com/montybot/FACSHuman) 

MHX2: [https://github.com/makehumancommunity/mhx2-makehuman-exchange](https://github.com/makehumancommunity/mhx2-makehuman-exchange)

## Save/Export File

Navigate to **Files** tab, and choose Save or Export.

The default file type when saving the file is a MakeHuman file, which contains the configuration of the human avatar. 

A folder named **textures** is automatically generated with any types of export, containing UV and normal maps of the mesh.

### mhx2
With the **mhx2** plugin enabled, the avatar mesh, textures, pose and facial expressions can be saved as a .mhx2 file. 

### fbx
A common file format that interfaces with Blender, Cinema 4D, 3D Max, and Autodesk Maya. 

### obj/stl - NOT RECOMMENDED
Common mesh formats for 3D files. The exported models are surface mesh and may contain voids that need to be filled. **It is better to export as mhx2, open in Blender, and export stl or obj from Blender.**
