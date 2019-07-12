# Hyperscope

[Explore images here](https://momonala.github.io/hyperscope.github.io/)

A Low-Cost Motorized Microscope to generate hyper-resolution microscope images. 

Automated micropscopes offer a wide range of advantages over manual operation. They are particularly useful for easier viewing and operational use, live-cell image aquisition, time lapse experiments, object-tracking, and more. However, Automated microscopes are prohibiively expensive for the average hobbyist, ranging from $10k-$20k. Solutions to adapt a manual micropscope with an automated stage exists, but is still in the price range of $6000 minimum. 

Hyperscope is an attempt to change that, by using 3d printing, easy to find, off-the-shelf components, and open source software  - reducing the cost to less than $100. 

Specifically, Hyperscope firmware and software allows for 3 features: 
 
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
# How it Works:

## Software
### Hyper-Resolution Parnoramics
We can scan across an slide along the x and y axis and take images along the way, and then stitch these images together with [OpenCV's stitching class](https://docs.opencv.org/2.4/modules/stitching/doc/introduction.html). See the link for a detailed description of this pipeline. Stitching can be performed using the `generate_panos.py` file. 

My experiments show that with OpenCV, at least 20% overlap of images is need to get reliable stitching. Since the stitching uses Scale-Invariant-Feature-Transforms (SIFT), the rotation and scale of our images does not matter. 

However, I found that OpenCV's algorithm is optimized for smaller collections of images, and not for recurisve stitching. Recursive or sequential stitching of images results in progressive blurring, caused by overlaying images with slight frame shifts. Instead, its best to stitch images in batches. Ideally, we stitch one entire horizontal row of images at a time, then stitch these large horizontal stacks.

The final panoramic, hyper-resolution image, will likely be up to a giga-pixel in size, so it is not practical to view it in a normal image renderer. Instead, we can make use of OpenSeaDragon, which uses a similar protocol as Google Maps to view and interact with large scale images, by tile-ing the image and rendering it in pieces as needed. 

To make the hyper-resolution image compatible with [OpenSeaDragon (OSD)](https://openseadragon.github.io/#downloadh), you need to covert it into a `.dzi` file, and OSD recommends some ways here. I like the Shell script [MagickSlicer](https://github.com/VoidVolker/MagickSlicer). 

### Firmware for Steppers

To do - write this. 
