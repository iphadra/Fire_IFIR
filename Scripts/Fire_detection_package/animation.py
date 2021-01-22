import moviepy.editor as mp
import imageio
import os


def create_gif(path="", duration=0.5, name="Fire", delete_images=True):
    print("Creando gif")
    filenames = sorted(os.listdir(path))
    images = []
    for filename in filenames:
        images.append(imageio.imread(path+filename))
    output_file = path+name+'.gif'
    imageio.mimsave(output_file, images, duration=duration)
    if delete_images:
        os.system("rm "+path+"*.png")


def movie_maker(path="", name="Fire", delete_gif=True):
    clip = mp.VideoFileClip(path+name+'.gif')
    clip.write_videofile(path+name+".mp4")
    if delete_gif:
        os.system("rm "+path+"*.gif")
