# Hyperscope

[Explore images here](https://momonala.github.io/hyperscope.github.io/)

A Low-Cost Motorized Microscope to generate imagery for hyper-resolution microscopy and image-stacking for increased depth of field. 

Automated micropscopes offer a wide range of advantages over manual operation. They are particularly useful for easier viewing and operational use, live-cell image aquisition, time lapse experiments, object-tracking, and more. However, Automated microscopes are prohibiively expensive for the average hobbyist, ranging from $10k-$20k. Solutions to adapt a manual micropscope with an automated stage exists, but is still in the price range of $6000 minimum. 

Hyperscope is an attempt to change that, by using 3d printing, easy to find, off-the-shelf components, and open source software  - reducing the cost to less than $100. 

Specifically, Hyperscope firmware and software allows for 3 features: 
 
- (TO DO) autmated scanning and photography of a slide
    - image stitching for hyper-resolution panaramics of the entire slide
    - (TO DO) focus stacking for increased depth of field imagry of samples

---     
# Installation 
## Dependencies 
-  Python >=3.4
    - `pip install -r requirments.txt`
- [OpenCV](https://opencv.org/) for image processing
    - `conda install -c conda-forge opencv ` (recommended to use Conda)

--- 
# How it Works:

## Software
### Hyper-Resolution Parnoramics
We can scan across an slide and take images along the way, and then stitch these images together using [OpenCV's stitching class](https://docs.opencv.org/2.4/modules/stitching/doc/introduction.html). See the link for a detailed description of this pipeline. Stitching can be performed using the `generate_panos.py` file. 

TO DO: give specifics about how to run the files, edit parameters etc. 

The final panormic, hyper-resolution image, will likely be up to a giga-pixel in size, so it is not practical to view it in a normal image renderer. Instead, we can make use of OpenSeaDragon, which uses a similar protocol as Google Maps to view and interact with large scale images, by tile-ing the image and rendering it in pieces as needed. 

To make the hyper-resolution image compatible with [OpenSeaDragon](https://openseadragon.github.io/#downloadh), we need to covert it into a `.dzi` file, and OSD recommends some ways here. I like the Shell script [MagickSlicer](https://github.com/VoidVolker/MagickSlicer). 

Once you create the `.dzi` files, place them in `templates/dzi`, TO DO run the Flask app `app.py`, and navigate to your image of interest on your local host :-) 

### Image Stacking

### Firmware for Steppers

