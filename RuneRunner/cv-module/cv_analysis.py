import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50
from PIL import Image
from dotenv import load_dotenv
import os
import logging

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CVAnalysis:
    def __init__(self):
        self.model = resnet50(pretrained=True)
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def analyze_image(self, image_bytes):
        image = Image.open(io.BytesIO(image_bytes))
        image_tensor = self.transform(image).unsqueeze(0)
        
        with torch.no_grad():
            output = self.model(image_tensor)
        
        _, predicted = torch.max(output, 1)
        logging.info(f"Bild analysiert: Klasse {predicted.item()}")
        return predicted.item()

    def detect_text(self, image_bytes):
        # Hier würden Sie OCR-Logik implementieren, z.B. mit Tesseract
        logging.info("Texterkennungs-Funktion aufgerufen")
        return "Beispieltext aus dem Bild"

if __name__ == "__main__":
    cv_model = CVAnalysis()
    # Hier müssten Sie den Pfad zu einem Testbild angeben
    test_image_path = "path/to/test/image.jpg"
    result = cv_model.analyze_image(test_image_path)
    print(f"Analyseergebnis: {result}")
