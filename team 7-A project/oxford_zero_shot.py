import numpy as np 
import matplotlib.pyplot as plt
import os 
from PIL import Image
from collections import OrderedDict
import torch 
import clip 
from PIL import Image 
from cleaning_oxford_data import sentences, final_image_list, test

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess  = clip.load("ViT-B/32", device=device)
text = clip.tokenize(sentences).to(device)
img_path = "C:\\Users\\gtent\\Desktop\\cours_3A\\MAP583\\Oxford\\oxbuild_images"


quantity = 150
offset = 0
res = 0

for img_name in final_image_list[offset:offset+quantity]:
    image = preprocess(Image.open(os.path.join(img_path, img_name))).unsqueeze(0).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)
        
        logits_per_image, logits_per_text = model(image, text)
        probs = logits_per_image.softmax(dim = -1).cpu().numpy()
        probs *= 100
        sentence = sentences[list(probs[0]).index(max(probs[0]))]
        if test(sentence, img_name):
            res += 1
            # plt.imshow(Image.open(os.path.join(img_path, img_name)).convert("RGB"))
            # plt.show()
            # print(sentence)
            
            
print(res)
print(res/quantity)
