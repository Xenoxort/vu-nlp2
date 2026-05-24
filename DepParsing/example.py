import torch
from parser_model import ParserModel
from parser_transitions import minibatch_parse
from utils.parser_utils import load_and_preprocess_data, ModelWrapper


parser, embeddings, train_data, dev_data, test_data = load_and_preprocess_data(False)

model = ParserModel(embeddings)
model.load_state_dict(torch.load("results/20260516_210247/model.weights", map_location="cpu"))
model.eval()
parser.model = model

words = ["The", "university", "blocked", "the", "acquisition", ",", "citing", "concerns", "about", "the", "risks", "involved", "."]
pos = ["DT", "NN", "VBD", "DT", "NN", ",", "VBG", "NNS", "IN", "DT", "NNS", "VBN", "."]

example = {
    "word": words,
    "pos": pos,
    "head": [0] * len(words),
    "label": [parser.root_label] * len(words),
}

vec = parser.vectorize([example])
sentence = [i + 1 for i in range(len(words))]
wrapper = ModelWrapper(parser, vec, {id(sentence): 0})
deps = minibatch_parse([sentence], wrapper, 1)[0]

print("Tokens:")
for i, (word, tag) in enumerate(zip(words, pos), start=1):
    print(f"{i:>2}. {word:<15} POS={tag}")

print("\nPredicted dependencies:")
for head, dep in deps:
    head_word = "ROOT" if head == 0 else words[head - 1]
    dep_word = words[dep - 1]
    dep_pos = pos[dep - 1]
    print(f"{head_word} -> {dep_word} ({dep_pos})")
