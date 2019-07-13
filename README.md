# Hyperscope

A low-cost motorized microscope for generating hyper-resolution microscope images. 

[Explore sample images here](https://momonala.github.io/hyperscope.github.io/)

Automated micropscopes offer a wide range of advantages over manual operation. They are particularly useful for easier viewing and operational use, live-cell image aquisition, time lapse experiments, object-tracking, and more. However, automated microscopes are prohibitively expensive for the average hobbyist, ranging from $10k-$20k. Solutions to adapt a manual micropscope with an automated stage exists, but is still in the price range of $6000 minimum. 

Hyperscope is an attempt to change that, by using 3d printing, easy to find, off-the-shelf components, and open source software  - reducing the cost to less than $100. 

Specifically, Hyperscope firmware and software allows for 2 key-features: 
 
- automatic generation of hyper-resolution panaramics of an entire slide
- (TO DO) automatic scanning and photography of a slide

---     
# Installation 
## Dependencies 
-  Python >=3.4
    - `pip install -r requirments.txt`
- [OpenCV](https://opencv.org/) for image processing
    - `conda install -c conda-forge opencv `

--- 
# How it Works:

## Automatically Generating Hyper-Resolution Panoramics

To generate the hyper-resolution panoramics, we need to scan across a slide in the x and y directions and take a grid of images. These images are organized by row and stitched together in these row-batches. The long row-images are stitched into a large final panoramic, and this final image is sliced according to the [DZI protocol](https://openseadragon.github.io/examples/tilesource-dzi/) for rendering with the [OpenSeaDragon (OSD)](https://openseadragon.github.io/#downloadh) renderer. This pipeline is fully automated into the [`python_hyperscope/generate_panos.py`](python_hyperscope/generate_panos.py) script. 

#### Usage
```bash
python -m python_hyperscope.generate_panos \
    --input microscope_images/<sample directory>
```

Saves output image and `.dzi` file directory to `microscope_images/<sample directory>/output`

Images are stitched together, utilizing [OpenCV's stitching class](https://docs.opencv.org/2.4/modules/stitching/doc/introduction.html). See the link for a detailed description of this pipeline.

Its also possible to also stitch using the [AutoStich](http://matthewalunbrown.com/autostitch/autostitch.html) library by Matthew Brown. I've noticed that library can handle more edge cases, but there is no API, so it is not possible to programtically automate the stitching.

My experiments show that with OpenCV, at least 20% overlap of images is need to get reliable stitching. Since the stitching uses [Scale-Invariant-Feature-Transforms (SIFT)](https://en.wikipedia.org/wiki/Scale-invariant_feature_transform), the rotation and scale of our images does not matter. 

However, I found that OpenCV's algorithm is optimized for smaller collections of images, and not for recurisve stitching. Recursive or sequential stitching of images results in progressive blurring, caused by overlaying images with slight frame shifts. Instead, its best to stitch images in batches. Ideally, we stitch one entire horizontal row of images at a time, then stitch these large horizontal stacks, which is built into my pipeline.

The final panoramic, hyper-resolution image, will likely be up to a giga-pixel in size, so it is not practical to view it in a normal image renderer. Instead, we can make use of OSD, which uses a similar protocol as Google Maps to view and interact with large scale images, by tile-ing the image and rendering it in pieces as needed. 

To make the hyper-resolution image compatible with OSD, you need to covert it into a DZI format. I use the Shell script [MagickSlicer by VoidVolker](https://github.com/VoidVolker/MagickSlicer).

## Mover Automation

The hardware enables both programatic and manual (with a joystick) control of the slide movers. 

Materials list:
     
 - Arudino Mega micro-controller
 - two NEMA 17 stepper motors
 - two A4988 stepper drivers
 - two timing belts
 - joystick - 2 axis analog output, z-axis digital output
 - remote camera trigger
 
All interfaces between these parts and the microscope were 3d printed, and the parts can be found in the [hardware](/hardware) directory. Note that my camera trigger is just a Nikon remote shutter release, hot-wired to be triggered from a `PIN_UP` signal from the Arduino ;) Below is a schematic of the hardware.

![hyperscope-hardware-shematic](assets/hyperscope-hardware-shematic.png "hyperscope-hardware-shematic")

For manual control, simply move use the joystick to move in the x and y directions, and click the joystick to take a photo.

For automatic control the slide needs to be position in to be viewing the top right position of the slide. When triggered, it will move one quarter of one turn of the mover dial, and take a photo. The firmware is designed to the specs of my microscope, so it will move the correct number of steps for one row, the move down, and image the next row. This repeats for the range of the entire slide. Variables may need to changed in the firmware to fit your scope.

One blank image is take after each row. This is used as a signal for the panaromaic software. All images taken in one slide can just be moved to one directory in `/microscope_images/<sample-dir>` and the software will automatically detect the rows and stitch accordingly. 