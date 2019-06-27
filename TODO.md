# To Do

## Software 
### Image Stitching
- determine minimum % of image offset needed for stitching (avoid excess) 
- confirm rotation of images is same -> improves horizontal error
    - align stitched image and crop out black on horizontal
- cascade stitches in horizontal batches until final image is reached
    - write an automated algo for this
- test on maximum zoom level
- LATER automatically generate tiles for OpenSeaDragon renderer

### Firmware
Get Serial input working reliably

## Hardware
### Stage Automation
- determine when bounds hit on stage
- print motor-stage interface - timing belts

---
# Later 
### Web Viewer
- Jinja templating for Flask + frontend + OpenSeaDragon
- root site + individual pages for unique images

### AutoFocus
- determine if image is in focus or not, go to right spot if not

### Object Tracking for live cells
- follow a specific sample around (OpenCV Tracking lib)
- selected ROIs (requires GUI)


### Remote Trigger Camera
- hotwire existing trigger OR do within software with tethering cable...
    - once complete, trigger image stitching software
