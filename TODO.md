# To Do

## Software 
### Image Stitching
- confirm rotation of images is same
- perform image stitching given a directory
    - handle for frames w/ no sample (appears as duplicate frames?)
- automatically generate tiles for OpenSeaDragon renderer

### Web Viewer
- Jinja templating for Flask + frontend + OpenSeaDragon
- root site + individual pages for unique images

### Firmware
- C++ code for focus and stage steppers
    - manual movement
    - autmated scanning across a stage
        - single focus plane
        - LATER image stacking on multiple planes
    - LATER selected ROIs (requires GUI)
    - LATER object tracking (requires OpenCV)

## Hardware
### Stage Automation
- Fully replaceable stage?
     - edit OpenSCAD designs
     - small CD Steppers + linear guide rails
     - drive with Arduino Mega + 5V DC

### Focus Automation
- large steppers, driven by Arduino Mega + 12V DC
- 3d print holders (OpenSCAD? or Autodesk?)

### Remote Trigger Camera
- hotwire existing trigger OR do within software with tethering cable...
    - once complete, trigger image stitching software
