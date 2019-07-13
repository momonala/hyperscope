# Hyperscope

[Explore images here](https://momonala.github.io/hyperscope.github.io/)

A low-cost motorized microscope for generating hyper-resolution microscope images. 

Automated micropscopes offer a wide range of advantages over manual operation. They are particularly useful for easier viewing and operational use, live-cell image aquisition, time lapse experiments, object-tracking, and more. However, automated microscopes are prohibitively expensive for the average hobbyist, ranging from $10k-$20k. Solutions to adapt a manual micropscope with an automated stage exists, but is still in the price range of $6000 minimum. 

Hyperscope is an attempt to change that, by using 3d printing, easy to find, off-the-shelf components, and open source software  - reducing the cost to less than $100. 

Specifically, Hyperscope firmware and software allows for 3 key-features: 
 
- (TO DO) autmated scanning and photography of a slide
- image stitching for hyper-resolution panaramics of the entire slide
- full manual control

---     
# Installation 
## Dependencies 
-  Python >=3.4
    - `pip install -r requirments.txt`
- [OpenCV](https://opencv.org/) for image processing
    - `conda install -c conda-forge opencv `

--- 
# Usage
```bash
python -m python_hyperscope.generate_panos \
    -i microscope_images/<sample directory>/
```

Saves output image and `.dzi` file directory to `microscope_images/<sample directory>/output`

--- 
# How it Works:

### Hyper-Resolution Parnoramics
We can scan across an slide along the x and y axis and take images along the way, and then stitch these images together with [OpenCV's stitching class](https://docs.opencv.org/2.4/modules/stitching/doc/introduction.html). See the link for a detailed description of this pipeline. Stitching can be performed using the `generate_panos.py` file. Its possible to also stitch using the [AutoStich](http://matthewalunbrown.com/autostitch/autostitch.html) library by Matthew Brown. I've seen slightly better and faster results with this, but there is no API, so it is not possible to automate the process.

My experiments show that with OpenCV, at least 20% overlap of images is need to get reliable stitching. Since the stitching uses Scale-Invariant-Feature-Transforms (SIFT), the rotation and scale of our images does not matter. 

However, I found that OpenCV's algorithm is optimized for smaller collections of images, and not for recurisve stitching. Recursive or sequential stitching of images results in progressive blurring, caused by overlaying images with slight frame shifts. Instead, its best to stitch images in batches. Ideally, we stitch one entire horizontal row of images at a time, then stitch these large horizontal stacks.

The final panoramic, hyper-resolution image, will likely be up to a giga-pixel in size, so it is not practical to view it in a normal image renderer. Instead, we can make use of OpenSeaDragon, which uses a similar protocol as Google Maps to view and interact with large scale images, by tile-ing the image and rendering it in pieces as needed. 

To make the hyper-resolution image compatible with [OpenSeaDragon (OSD)](https://openseadragon.github.io/#downloadh), you need to covert it into a `.dzi` file. I like the Shell script [MagickSlicer](https://github.com/VoidVolker/MagickSlicer). I've incorporated this into the `generate_panos.py` image stitching pipeline.

### Mover Firmware

Its possible to move the slide programatically as well as manual (with a joystick). The hardware calls for an Arudino Mega microcontroller, two NEMA 17 stepper motors, two A4988 drivers, and a camera trigger. Note that my camera trigger is just a Nikon remote shutter release, hot-wired to be triggered from a `PIN_UP` signal from the Arduino ;) Below is a schematic of the hardware.

![hyperscope-hardware-shematic](assets/hyperscope-hardware-shematic.png "hyperscope-hardware-shematic")

For manual control, simply move use the joystick to move in the x and y directions, and click the joystick to take a photo.

For automatic control the slide needs to be position in to be viewing the top right position of the slide. When triggered, it will move one quarter of one turn of the mover dial, and take a photo. The firmware is designed to the specs of my microscope, so it will move the correct number of steps for one row, the move down, and image the next row. This repeats for the range of the entire slide. Variables may need to changed in the firmware to fit your scope.

One blank image is take after each row. This is used as a signal for the panaromaic software. All images taken in one slide can just be moved to one directory in `/microscope_images/<sample-dir>` and the software will automatically detect the rows and stitch accordingly. 