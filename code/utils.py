import cv2 as cv
import os
import glob
import numpy as np


def save_img(fname, img):
    cv.imwrite(fname, img)


def load_img(fname):
    img = cv.imread(fname)
    return img


def save_video_frame(vid_name, target_folder='./test_vid_frames', use_memory=True):
    print("Cutting video to frames...")
    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
    assert os.path.exists(target_folder)

    vidcap = cv.VideoCapture(vid_name)
    success, image = vidcap.read()
    if not use_memory:
        count = 0
        while success:
            dest = target_folder + f"/{count}.jpg"
            save_img(dest, image)
            success, image = vidcap.read()
            count += 1
        print("Done saving images in local drive")
        return None
    else:
        image_list = [image]
        count = 0
        while success:
            success, image = vidcap.read()
            if image is not None:
                print(count)
                image_list.append(image)
                count += 1
        result = image_list
        # result = np.asarray(image_list)
        print("Done saving image in memory")
        return result


def construct_video_from_memory(images, target_folder, vid_out):
    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
    assert os.path.exists(target_folder)
    print("Constructing video ...")
    height, width, layers = images[0].shape
    size = (width, height)
    print(size)
    out_path = f'{target_folder}/{vid_out}'
    out = cv.VideoWriter(
        out_path, cv.VideoWriter_fourcc(*'DIVX'), 15, size)
    for i in range(len(images)):
        print(i)
        out.write(images[i])
    out.release()
    print("Done constructing video!")


def construct_video(src_folder, target_folder, vid_out):
    assert os.path.exists(src_folder)
    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
    assert os.path.exists(target_folder)

    path, dirs, files = next(os.walk(src_folder))
    num_frames = len(files)
    img_array = []
    for i in range(num_frames):
        fname = f'{src_folder}/{i}.jpg'
        print(fname)
        img = load_img(fname)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out_path = f'{target_folder}/{vid_out}'
    out = cv.VideoWriter(
        out_path, cv.VideoWriter_fourcc(*'DIVX'), 15, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()


if __name__ == "__main__":
    vid_images = save_video_frame('./test_vid/video.mp4')
    construct_video_from_memory(vid_images, './out', 'testproject.avi')
    # construct_video("./test_vid_processed_frames", "./out", "testproject.avi")
    None