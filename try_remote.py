# Use face_alignment remotely
# need `pip install requests`
import json, time
import requests

# url = "http://try.star-lab.ai:9003/predictions/face_lm_3d"
url = "http://localhost:9003/predictions/face_lm_3d"
img_path = "./assets/sida_1.png"
headers = {
  'Content-Type': 'image/png'
}

# Read the image into memory, in the format of bytes.
with open(img_path, "rb") as f:
    payload=f.read()

# Send the request.
start = time.time()
response = requests.request("POST", url, headers=headers, data=payload)
end = time.time()
print(f"time: {end-start}")

# Parse the response.
response = json.loads(response.text)
# print(response)

# Visualize the results.
import collections, os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import image

def plot(preds, input_img, only_2d=True):
    """
    plot the original image and the landmarks.
    ignoring the depth, only use [x,y] (2D) in the response.
    """
    preds = np.array(preds)
    plot_style = dict(marker='o',
                    markersize=4,
                    linestyle='-',
                    lw=2)

    pred_type = collections.namedtuple('prediction_type', ['slice', 'color'])
    pred_types = {'face': pred_type(slice(0, 17), (0.682, 0.780, 0.909, 0.5)),
                'eyebrow1': pred_type(slice(17, 22), (1.0, 0.498, 0.055, 0.4)),
                'eyebrow2': pred_type(slice(22, 27), (1.0, 0.498, 0.055, 0.4)),
                'nose': pred_type(slice(27, 31), (0.345, 0.239, 0.443, 0.4)),
                'nostril': pred_type(slice(31, 36), (0.345, 0.239, 0.443, 0.4)),
                'eye1': pred_type(slice(36, 42), (0.596, 0.875, 0.541, 0.3)),
                'eye2': pred_type(slice(42, 48), (0.596, 0.875, 0.541, 0.3)),
                'lips': pred_type(slice(48, 60), (0.596, 0.875, 0.541, 0.3)),
                'teeth': pred_type(slice(60, 68), (0.596, 0.875, 0.541, 0.4))
                }

    fig = plt.figure()
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    # ax = fig.add_subplot(1, 1 if only_2d else 2, 1)
    ax.imshow(input_img)

    for pred_type in pred_types.values():
        ax.plot(preds[pred_type.slice, 0],
                preds[pred_type.slice, 1],
                color=pred_type.color, **plot_style)

    ax.axis('off')
    os.makedirs("debug", exist_ok=True)
    plt.savefig("debug/output-remote.png", dpi=50)

# Read the image again in the format of numpy array, for plotting purpose.
np_img = image.imread(img_path)
plot(response['landmarks'][0], np_img)