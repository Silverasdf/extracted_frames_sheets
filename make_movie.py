import cv2
import numpy as np

# for image in images:
#     image = cv2.imread(os.path.join(image_folder, image))
#     image = cv2.resize(image, (width, height))
#     video.write(image)

# fc = cv2.VideoWriter_fourcc(*"mp4v")
# video = cv2.VideoWriter("1.mp4", fc, 0.25, (500, 500))

# for idx in range(10):
#     color = np.random.randint(0, 255, size=3)
#     if idx in [0, 2, 3]:  # only 3 frames will be in the final video
#         image = np.full((500, 500, 3), fill_value=color, dtype=np.uint8)
#     else:
#         # slighly different size
#         image = np.full((400, 500, 3), fill_value=color, dtype=np.uint8)

#     video.write(image)

import os

def images_to_video(image_folder, video_name, fps):
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg") or img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
for i in range(112, 116, 1):
    print("Processing sequence: ", i)
    image_folder = 'sequences/000'+str(i+1)+'/'
    video_name = 'outputs/tmp/output_video'+str(i+1)+'.mp4'
    fps = 30
    try:
        images_to_video(image_folder, video_name, fps)
    except Exception as e:
        continue