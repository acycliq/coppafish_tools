import tifffile
import os
import numpy as np
import napari
from if_registration import (register_if,
                              apply_transform,
                              extract_raw,
                              convert_notebook_coords_to_zeta)
from coppafish import Notebook
from zetastitcher import stitch_align, stitch_fuse


def extract_step():
    nb_file = r'/media/dimitris/My Passport/data/Christina/test_coppafish-tools/output/notebook.npz'
    if_nd2_dir = r'/media/dimitris/My Passport/data/Christina/test_coppafish-tools/astro-NLF_488-p62_594-GFAP_647-Iba1.nd2'
    if_output_dir = r'/media/dimitris/My Passport/data/Christina/test_coppafish-tools/if_reg_output'
    extracted_dir = r'/media/dimitris/My Passport/data/Christina/test_coppafish-tools/tiles/extract/'
    nb = Notebook(nb_file)

    extract_raw(nb=nb, save_dir=if_output_dir,
                read_dir=if_nd2_dir,
                use_tiles=nb.basic_info.use_tiles,
                use_channels=[0],
                extracted_dir=extracted_dir)


def zetastitcher_step():
    opts = {'yml_file': '/media/dimitris/My Passport/data/Christina/test_coppafish-tools/if_reg_output/if/channel_0'}
    stitch_fuse(opts)


def register_step():
    path = '/media/dimitris/My Passport/data/Christina/test_coppafish-tools/if_reg_output'
    if_dir = os.path.join(path, 'if','channel_0', 'fused.tif')
    seq_dir = os.path.join(path, 'seq', 'channel_0', 'fused.tif')
    if_save_dir = os.path.join(path, 'if', 'channel_0', 'stitched_IFr_DAPI_aligned.tif')

    if_im = tifffile.imread(if_dir)[:, ::4, ::4]
    seq_im = tifffile.imread(seq_dir)[:, ::4, ::4]
    np.shape(if_im)

    reg_parameters = {'subvolume_size': [8, 512, 512],
                      'r_threshold': 0.8,
                      'overlap': 0.1,
                      'registration_type':'subvolume'}

    transform_save_dir = os.path.join(path, 'if', 'channel_0')
    transform = register_if(seq_im, if_im,
                            downsample_factor_yx=4,
                            transform_save_dir=transform_save_dir,
                            reg_parameters=reg_parameters)

    # if_dir = os.path.join(path, 'if', 'channel_9', 'fused.tif')
    # if_save_dir = os.path.join(path, 'if', 'channel_9')
    apply_transform(im_dir=if_dir, transform=transform, save_dir=if_save_dir)


def app():
    extract_step()
    zetastitcher_step()
    register_step()




if __name__ == "__main__":
    v = napari.Viewer()
    app()
    print('Done')