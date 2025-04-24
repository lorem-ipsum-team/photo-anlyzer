import string
import torch
from transformers import AutoTokenizer, AutoModel
import nltk
from nltk.corpus import stopwords
from nltk import pos_tag, word_tokenize
import numpy as np


class TextProcessor:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('stopwords')
        nltk.download('punkt_tab')
        nltk.download('averaged_perceptron_tagger_eng')

        if torch.mps.is_available():
            dev_name = 'mps'
        elif torch.cuda.is_available():
            dev_name = 'cuda'
        else:
            dev_name = 'cpu'

        self._device = torch.device(dev_name)
        self._tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self._text_model = AutoModel.from_pretrained("bert-base-uncased")\
            .to(self._device)

    def _clean_word(self, word):
        return word.lower().strip(string.punctuation)

    def _get_mean_embedding(self, tokens, attention_mask):
        """
        Computes mean-pooled BERT embedding (excluding [PAD] tokens).
        """
        with torch.no_grad():
            outputs = self._text_model(
                input_ids=tokens, attention_mask=attention_mask)
            # (batch_size, seq_len, hidden_size)
            last_hidden = outputs.last_hidden_state
            mask = attention_mask.unsqueeze(
                -1).expand(last_hidden.size()).float()
            summed = torch.sum(last_hidden * mask, dim=1)
            counts = torch.clamp(mask.sum(1), min=1e-9)
            mean_pooled = summed / counts
            return mean_pooled.cpu().numpy()

    def process_text(self, text: str, top_n: int = 5):
        stop_words = stopwords.words('english')
        stop_words.extend(stopwords.words('russian'))
        stop_words = set(stop_words)
        negation_words = {'dont', 'not', 'no', 'never'}  # Слова-отрицания

        # Токенизация и POS-теги
        raw_words = word_tokenize(text)
        tagged = pos_tag(raw_words)

        # Оставляем только существительные/глаголы и убираем стоп-слова
        filtered_words = []
        for i, (word, tag) in enumerate(tagged):
            word_clean = self._clean_word(word)
            # Проверка на слова, не являющиеся стоп-словами или частями отрицания
            if word_clean and word_clean not in stop_words and word_clean not in negation_words and tag.startswith(('NN', 'VB')):
                # Проверка на отрицание перед словом
                if i > 0 and tagged[i-1][0].lower() in negation_words:
                    continue  # Если перед словом есть отрицание, исключаем его
                filtered_words.append(word_clean)

        # Если нет слов после фильтрации, возвращаем пустой список
        if not filtered_words:
            return []

        # Embedding текста целиком
        sentence_inputs = self._tokenizer(
            text, return_tensors="pt", truncation=True, max_length=128).to(self._device)
        sentence_emb = self._get_mean_embedding(
            sentence_inputs['input_ids'], sentence_inputs['attention_mask'])

        # Embeddings для слов
        word_embs = []
        for word in filtered_words:
            inputs = self._tokenizer(
                word, return_tensors="pt").to(self._device)
            emb = self._get_mean_embedding(
                inputs['input_ids'], inputs['attention_mask'])
            word_embs.append(emb[0])

        word_embs = np.stack(word_embs)
        sims = np.dot(word_embs, sentence_emb.T).squeeze()

        top_indices = sims.argsort()[::-1][:top_n]
        tags = [filtered_words[i] for i in top_indices]

        # Возвращаем уникальные теги по убыванию их значимости
        return list(dict.fromkeys(tags))  # Уникальные в порядке важности
