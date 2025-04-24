import torch
from facenet_pytorch import MTCNN, InceptionResnetV1


class FacenetProcessor:
    def __init__(self):
        if torch.cuda.is_available():
            dev_name = 'cuda'
        else:
            dev_name = 'cpu'

        self._device = torch.device(dev_name)
        self._mtcnn = MTCNN(keep_all=False, device=self._device)
        self._resnet = InceptionResnetV1(pretrained='vggface2')\
            .eval().to(self._device)

    def process_image(self, image):
        face = self._mtcnn(image)

        if face is None:
            return None

        face = face.unsqueeze(0).to(self._device)
        embedding = self._resnet(face).detach().cpu().numpy()
        return embedding
