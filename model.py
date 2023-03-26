import torch
import torchvision.transforms as T
from PIL import Image
import matplotlib.pyplot as plt
from model_defined import EncoderDecoder, Vocabulary

device = "cuda" if torch.cuda.is_available() else "cpu"
model = EncoderDecoder(
    embed_size=300,
    vocab_size =100,
    attention_dim=256,
    encoder_dim=2048,
    decoder_dim=512
).to(device)

checkpoint = torch.load("attention_model_state.pth", map_location=torch.device('cpu'))
model.load_state_dict(checkpoint, strict = False)
# optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
# epoch = checkpoint['num_epochs']
# loss = checkpoint['loss']
vocab_size=checkpoint['vocab_size']


image = Image.open("dfdfdf.jpg")
transforms = T.Compose([
    T.Resize(226),                     
    T.RandomCrop(224),                 
    T.ToTensor(),                               
    T.Normalize((0.485, 0.456, 0.406),(0.229, 0.224, 0.225))
])
image = transforms(image).unsqueeze(0).to(device)


model.eval()
with torch.no_grad():
    features = model.encoder(image.to(device))
    print(features)
    caps, alphas = model.decoder.generate_caption(features, vocab=Vocabulary(5))
    caption = ' '.join(caps)
    print(caption)
