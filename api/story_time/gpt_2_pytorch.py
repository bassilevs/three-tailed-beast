from pytorch_transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch


class Model:
    def __init__(self):
        super(Model, self).__init__()
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._model = None
        self._tokenizer = None
        self.load()

    def get_next_word(self, text):
        """Get the next top word prediction based on text."""
        indexed_tokens = self._tokenizer.encode(text)
        tokens_tensor = torch.tensor([indexed_tokens])

        self._model.eval()
        tokens_tensor = tokens_tensor.to(self._device)
        self._model.to(self._device)

        with torch.no_grad():
            outputs = self._model(tokens_tensor)
            predictions = outputs[0]

        probs = predictions[0, -1, :]
        top_next = [self._tokenizer.decode(i.item()).strip() for i in probs.topk(10)[1]]
        old_text = text.split()

        for item in top_next:
            if item != old_text[-1]:
                return item

    def get_next_n_words(self, curr_text, n):
        """Get the next n words for curr_text"""
        temp_text = curr_text + ""
        print("before", temp_text, n)
        for i in range(n):
            next_word = self.get_next_word(temp_text)
            print(next_word)
            if next_word in ['.', ',', '!', '?', '', ' ']:
                temp_text += next_word
                next_word = self.get_next_word(temp_text)
                print("next", next_word)
            temp_text += " " + next_word

        print("final", temp_text)
        return temp_text[len(curr_text):]

    def load(self):
        try:
            self._tokenizer = GPT2Tokenizer.from_pretrained("gpt2-medium")
            self._model = GPT2LMHeadModel.from_pretrained("gpt2-medium")
        except:
            self._model = None
        return self


model = Model()


def get_model():
    return model
