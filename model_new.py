import torch
from PIL import Image
import torchvision.transforms as transforms
from model_new2 import EncoderCNN, DecoderRNN
import pickle


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class Vocabulary(object):
  # Simple vocabulary wrapper
  def __init__(self):
    self.word2idx = {}
    self.idx2word = {}
    self.idx = 0

  def add_word(self, word):
    if not word in self.word2idx:
      self.word2idx[word] = self.idx
      self.idx2word[self.idx] = word
      self.idx += 1

  def __call__(self, word):
    if not word in self.word2idx:
      return self.word2idx['<UNK>']
    return self.word2idx[word]

  def __len__(self):
    return len(self.word2idx)


def load_image(image_path, transform=None):
    image = Image.open(image_path).convert('RGB')
    image = image.resize([224, 224], Image.Resampling.LANCZOS)

    if transform is not None:
        image = transform(image).unsqueeze(0)
    
    return image


class ImageCaptioning:
    def __init__(self):
        self.encoder_path = "nic_encoder_ResNet101.ckpt" # path for trained encoder
        self.decoder_path = "nic_decoder_ResNet101.ckpt" # path for trained decoder
    
        # Model parameters (should be same as paramters in train.py)
        self.embed_size = 256 # dimension of word embedding vectors
        self.hidden_size = 512 # dimension of lstm hidden states
        self.num_layers = 1 # number of layers in lstm

        # 이미지 전처리(image preprocessing)
        self.transform = transforms.Compose([
            transforms.ToTensor(), 
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))])

        # Load vocabulary wrapper
        # with open("vocab.pkl", 'rb') as f:
        #   self.vocab = pickle.load(f)
        self.vocab = pickle.load(open("vocab (2).pkl", 'rb'))

        # Build models
        self.encoder = EncoderCNN(self.embed_size).eval() # eval mode (batchnorm uses moving mean/variance)
        self.decoder = DecoderRNN(self.embed_size, self.hidden_size, len(self.vocab), self.num_layers)
        self.encoder = self.encoder.to(device)
        self.decoder = self.decoder.to(device)

        # Load the trained model parameters
        self.encoder.load_state_dict(torch.load(self.encoder_path, map_location=torch.device('cpu')))
        self.decoder.load_state_dict(torch.load(self.decoder_path, map_location=torch.device('cpu')))


    def generate_captions(self, input_file):
        # Prepare an image
        image = load_image(input_file, self.transform)
        image_tensor = image.to(device)

        # Generate an caption from the image
        feature = self.encoder(image_tensor)
        sampled_ids = self.decoder.sample(feature)
        sampled_ids = sampled_ids[0].cpu().numpy() # (1, max_seq_length) -> (max_seq_length)

        # Convert word_ids to words
        sampled_caption = []
        for word_id in sampled_ids: # 하나씩 단어 인덱스를 확인하며
            word = self.vocab.idx2word[word_id] # 단어 문자열로 바꾸어 삽입
            sampled_caption.append(word)
            if word == '':
                break
        sentence = ' '.join(sampled_caption)

        print(sentence)
        return sentence
    

