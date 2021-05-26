import time
from ts.torch_handler.vision_handler import VisionHandler
from torchvision import transforms

import face_alignment

class FaceHandler(VisionHandler):

    # self.image_processing will be used to preprocess the image in the requests.
    image_processing = transforms.Compose([
        # transforms.Resize(256),
        # transforms.CenterCrop(224),
        transforms.ToTensor(),
        # transforms.Normalize(mean=[0.485, 0.456, 0.406],
        #                      std=[0.229, 0.224, 0.225])
    ])

    def __init__(self) -> None:
        """
        Initilize a new instance.
        This will happen when the service starts.
        """
        print(f"HANDLER>__init__>")
        super().__init__()
        self.engine = face_alignment.FaceAlignment(face_alignment.LandmarksType._3D, device='cpu', flip_input=True)
        print(f"HANDLER>init> self.engine: {self.engine}")
        self.save_image_for_debug = True
        self.num_requests = 0

    def initialize(self, ctx):
        """
        Initialize the context.
        This will happen when we register the model.
        """
        print(f"HANDLER>initialize> ctx: {ctx}")
        super().initialize(ctx)
        print(f"HANDLER>initialize> self.model: {self.model}")

    def preprocess(self, requests):
        """
        This will happen when a client sents an API request.
        """
        print(f"HANDLER>preprocess> requests[0].keys(): {requests[0].keys()}")
        
        x = super().preprocess(requests)
        print(f"HANDLER>preprocess> x.shape: {x.shape}")
        
        self.num_requests = len(x)
        x = x[0] # Only take the first request, because processing the request is slow, it'll be too slow if there are multiple requests.
        x = x.permute(1,2,0) # package face_alignment wants the WHC format instead of the CWH format.
        x *= 255. # package face_alignment wants pixel values to be in [0,255] instead of [0,1]
        print(f"HANDLER>preprocess> after permute > x.shape: {x.shape}")
        return x

    def inference(self, x):
        """
        Process the request. Make predictions.
        This will happen after self.preprocess().
        """
        print(f"HANDLER>inference> x.shape: {x.shape}")

        if self.save_image_for_debug: # save image if needed
            from torchvision.utils import save_image
            x1 = x.permute(2,0,1).clone()
            x1 /= 255.
            save_image(x1, '/tmp/debug/img-docker.png') # /tmp/debug in container is mapped to ./debug on the local machine.

        # Every sophisticated thing happens here:
        start_time = time.time()
        preds = self.engine.get_landmarks(x)
        end_time = time.time()
        print(f"HANDLER>inference> get_landmarks takes {end_time-start_time} sec.")

        print(f"HANDLER>inference> len(preds): {len(preds)}")
        return preds

    def postprocess(self, y):
        """
        Construct the response after we have the results.
        This will happen after self.inference().
        """
        print(f"HANDLER>postprocess> len(y): {len(y)}")

        if len(y)==0: # there's no face
            response = [{
                "provider": "star-lab",
                "status": -1,
                "message": "no face detected",
            }]
            return response
        
        print(f"HANDLER>postprocess> y[0].shape: {y[0].shape}")
        # convert landmarks (lms) from numpy array into lists
        lms = []
        for lm in y:
            lms.append(lm.tolist())
        
        # Only give real response to the first request.
        response = [{
            "provider": "star-lab",
            "landmarks": lms,
        }]
        # Padding empty response to be aligned with the requests.
        for i in range(self.num_requests-1):
            response.append({})

        return response


if __name__=="__main__":
    #TODO: write a test case
    fa = FaceHandler()
