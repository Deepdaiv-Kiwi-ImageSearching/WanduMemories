# import torch
# import torchvision.transforms as T
# from PIL import Image
# import matplotlib.pyplot as plt
# from model_defined import EncoderDecoder, Vocabulary


# checkpoint = torch.load("attention_model_state.pth", map_location=torch.device('cpu'))
# device = "cuda" if torch.cuda.is_available() else "cpu"
# model = EncoderDecoder(
#     embed_size=checkpoint['embed_size'],
#     vocab_size =checkpoint['vocab_size'],
#     attention_dim=checkpoint['attention_dim'],
#     encoder_dim=checkpoint['encoder_dim'],
#     decoder_dim=checkpoint['decoder_dim']
# ).to(device)


# model.load_state_dict(checkpoint, strict = False)
# # optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
# # epoch = checkpoint['num_epochs']
# # loss = checkpoint['loss']
# vocab_size=checkpoint['vocab_size']
# # print(vocab_size)


# image = Image.open("1.jpg")
# transforms = T.Compose([
#     T.Resize(226),                     
#     T.RandomCrop(224),                 
#     T.ToTensor(),                               
#     T.Normalize((0.485, 0.456, 0.406),(0.229, 0.224, 0.225))
# ])
# image = transforms(image).unsqueeze(0).to(device)
# print(checkpoint)

# model.eval()
# with torch.no_grad():
#     features = model.encoder(image.to(device))
#     caps, alphas = model.decoder.generate_caption(features, vocab=Vocabulary(2))
#     caption = ' '.join(caps)
#     # print(caption)
