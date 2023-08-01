import tools.edge_enhancement
import argparse
from tools.utils import *
import os
from tqdm import tqdm
from glob import glob
import time
import numpy as np
from net import generator, generator_lite
#import tools.edge_enhancement.edge_enhance_from_dir
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

my_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

checkpoint_dir = {'genshin': my_abs_path+'/checkpoint/generator_genshin_weight',
                  'borderland': my_abs_path+'/checkpoint/generator_borderland_weight',
                  'shinchan': my_abs_path+'/checkpoint/generator_shinchan_weight'}


def parse_args():
    desc = "AnimeGANv2"
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('--style_name', type=str, default='genshin',
                        help='what style you want to get')
    parser.add_argument('--if_adjust_brightness', type=int, default=1,
                        help='adjust brightness by the real photo, 1=enable, 0=disable.')
    parser.add_argument('--if_edge_enhancement', type=int, default=0,
                        help='apply edge enahncement before animefy, 1=enable, 0=disable.')
    """checking arguments"""

    return parser.parse_args()


def stats_graph(graph):
    flops = tf.profiler.profile(
        graph, options=tf.profiler.ProfileOptionBuilder.float_operation())
    # params = tf.profiler.profile(graph, options=tf.profiler.ProfileOptionBuilder.trainable_variables_parameter())
    print('FLOPs: {}'.format(flops.total_float_ops))


def test(style_name, if_adjust_brightness, if_edge_enhancement, img_size=[256, 256]):

    # tf.reset_default_graph()
    result_dir = './temp_photos/anime_background/'+style_name
    #result_dir = './temp_photos/result'
    test_files = glob('./temp_photos/target/*.*')

    if if_edge_enhancement == 1:
        tar_dir = './temp_photos/target'
        save_dir = './temp_photos/target/edge'
        tools.edge_enhancement.edge_enhance_from_dir(tar_dir, save_dir)
        test_files = glob('./temp_photos/target/edge/*.*')

    test_real = tf.placeholder(tf.float32, [1, None, None, 3], name='test')
    with tf.variable_scope("generator", reuse=False):
        if 'lite' in checkpoint_dir:
            test_generated = generator_lite.G_net(test_real).fake
        else:
            test_generated = generator.G_net(test_real).fake
    saver = tf.train.Saver()

    gpu_options = tf.GPUOptions(
        allow_growth=True, per_process_gpu_memory_fraction=0.85)
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True, gpu_options=gpu_options)) as sess:
        # tf.global_variables_initializer().run()
        # load model
        ckpt = tf.train.get_checkpoint_state(
            checkpoint_dir[style_name])  # checkpoint file information
        print(checkpoint_dir[style_name])
        if ckpt and ckpt.model_checkpoint_path:
            ckpt_name = os.path.basename(
                ckpt.model_checkpoint_path)  # first line
            print(ckpt_name)
            print(os.path.join(
                checkpoint_dir[style_name], ckpt_name))
            saver.restore(sess, os.path.join(
                checkpoint_dir[style_name], ckpt_name))
            print(
                " [*] Success to read {}".format(os.path.join(checkpoint_dir[style_name], ckpt_name)))
        else:
            print(" [*] Failed to find a checkpoint")
            return
        # stats_graph(tf.get_default_graph())

        begin = time.time()
        for sample_file in tqdm(test_files):
            # print('Processing image: ' + sample_file)
            sample_image = np.asarray(load_test_data(sample_file, img_size))
            
            image_path = os.path.join(
                result_dir, '{0}'.format(os.path.basename(sample_file)))
            fake_img = sess.run(test_generated, feed_dict={
                                test_real: sample_image})

            if if_adjust_brightness == 1:
                save_images(fake_img, image_path, sample_file)
            else:
                save_images(fake_img, image_path, None)
        end = time.time()
        print(f'test-time: {end-begin} s')
        #print(f'one image test time : {(end-begin)/len(test_files)} s')


if __name__ == '__main__':
    arg = parse_args()
    test(arg.style_name, arg.if_adjust_brightness, arg.if_edge_enhancement)
