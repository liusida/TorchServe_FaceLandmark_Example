# Use face_alignment locally
# need to `pip install face_alignment skimage` and also torch and other dependencies
import face_alignment
from skimage import io
import torch
from helper.show_pred import show_pred

# Run the 3D face alignment on a test image, without CUDA.
fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._3D, device='cpu', flip_input=True)
input_img = io.imread('assets/sida_1.png')
print("input_img.shape: ", input_img.shape)

from torchvision.utils import save_image
x = torch.tensor(input_img, dtype=torch.float)
x1 = x.permute(2,0,1)
x1 /= 255.
save_image(x1, './debug/input-local.png')

preds = fa.get_landmarks(input_img)[-1]
show_pred(preds, input_img, filename="./debug/output-local.png")