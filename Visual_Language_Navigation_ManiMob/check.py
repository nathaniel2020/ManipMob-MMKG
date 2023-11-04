import clip
import torch.nn.functional as F
a = "to put the eggs in"
model, preprocess = clip.load("ViT-B/32", device="cuda")
text = clip.tokenize([a]).to("cuda")
text_features_1 = model.encode_text(text).squeeze(0)
b = "found_in_cupboard"
text = clip.tokenize([b]).to("cuda")
text_features_2 = model.encode_text(text).squeeze(0)
c = F.cosine_similarity(text_features_1, text_features_2, dim=0).item()
print(c)