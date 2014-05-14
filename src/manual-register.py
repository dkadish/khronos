from skimage import io, transform

import numpy as np
import matplotlib.pyplot as plt
import os

def main(base_dir):
    BASE_DIR = base_dir

    # Load the set of pictures
    ic = io.ImageCollection(BASE_DIR + '*.JPG')

    # Select points on the first picture
    f, ax = plt.subplots(1,1)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.autoscale(enable=True, axis='both', tight=True);
    plt.tight_layout(pad=0.4, w_pad=0.0, h_pad=0.0)
    ax.imshow(ic[0])

    coords = [plt.ginput(8, timeout=0)]

    plt.close()

    # Load first picture side-by side with second, select points.
    # Scroll through images one-by-one
    for i, img in enumerate(ic[1:]):
        ax1 = plt.subplot2grid((6,10),(0,1), rowspan=6, colspan=9)
        ax0 = plt.subplot2grid((6,10),(0,0))
        
        for ax in [ax0, ax1]:
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
        
        plt.tight_layout(pad=0.4, w_pad=0.0, h_pad=0.0)
        
        #f, (ax0,ax1) = plt.subplots(1,2)
        ax0.imshow(ic[i])
        for coord in coords[i]:
            ax0.scatter(coord[0],coord[1])
        ax1.imshow(img)
        
        coords.append(plt.ginput(8, timeout=0))
        
        plt.close()

    # Use a similarity transformation to transform each one.

    if not os.path.exists(BASE_DIR + 'corrected'):
        os.mkdir(BASE_DIR + 'corrected')

    np.save(BASE_DIR + 'corrected/coords.npy', coords)

    io.imsave(BASE_DIR + 'corrected/0.jpg', ic[0])
    for i, img in enumerate(ic[1:]):
        tf = transform.estimate_transform('similarity', np.array(coords[0]), np.array(coords[i+1]))

    # Use a translation transformation to center both images for display purposes

        img_warped = transform.warp(img, inverse_map=tf,
                                     output_shape=(1728,3072))
        
        print BASE_DIR + 'corrected/%d.jpg' %(i+1)
        print img_warped
        
        io.imsave(BASE_DIR + 'corrected/%d.jpg' %(i+1), img_warped)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Align images')
    parser.add_argument('base_dir', metavar='DIR', help='The directory with the images.')

    args = parser.parse_args()
    main(args.base_dir)
