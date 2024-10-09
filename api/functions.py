from sklearn.base import BaseEstimator, TransformerMixin
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
from num2words import num2words
import nltk
import string
import re
import string
import unicodedata

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nlp = spacy.load('es_core_news_sm')

def replace_percentage(text):
    return text.replace('%', ' porciento')

def corregir_codificacion(text, reemplazos):
    for clave, valor in reemplazos.items():
        text = text.replace(clave, valor)
    return text

def remove_non_ascii(text):
    return text.encode('ascii', 'ignore').decode('ascii')

def to_lowercase(text):
    return text.lower()

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def replace_numbers(text):
    def convert(match):
        number = match.group(0).replace(',', '.')
        if '.' in number:
            return num2words(float(number), lang='es').replace(' coma ', 'punto').replace(' ', '')
        else:
            return num2words(int(number), lang='es')
    return re.sub(r'\d+([,.]\d+)?', convert, text)

def remove_stopwords(text):
    stop_words = set(stopwords.words('spanish'))
    return ' '.join([word for word in text.split() if word not in stop_words])

def remove_accents(text):
    nfkd_form = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def lemmatize_verbs(tokens):
    doc = nlp(' '.join(tokens))
    return [token.lemma_ if token.pos_ == 'VERB' else token.text for token in doc]

# Clase de transformador personalizado
class TextPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self):
        # Puedes agregar parámetros si es necesario
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        reemplazos = {
            'ñ':'ni',
            'Ã¡': 'a',
            'Ã©': 'e',
            'Ã­': 'i',
            'Ã³': 'o',
            'Ãº': 'u',
            'Ãñ': 'ni',
            'Ã': 'a',
            'Ã¼': 'u',
            'Ã¢': 'a',
            'Ãª': 'e',
            'Ã ': 'a',  # Para palabras como 'asÃ'
            'Ã¡n': 'an',  # Para casos como 'podrÃan'
            'Ã­a': 'ia',  # Para palabras como 'psiquiatrÃa'
            'Ã±o': 'no',  # Para palabras como 'tamaÃ±o'
            'Ã³n': 'on',  # Para palabras como 'corresponderÃan'
            'Ã­n': 'in',  # Para palabras como 'mÃnimo'
            'Ã¡s': 'as',  # Para palabras como 'paÃs'
            'Ã©s': 'es',  # Para palabras como 'paÃses'
            'Ã³lico': 'olico',  # Para 'holÃstico'
            'Ãºltico': 'ultico',  # Para 'jurÃdico'
            'Ã¡tica': 'atica',  # Para 'polÃtica'
            'Ã': 'a',  # Genérico para cualquier letra mal codificada con 'Ã'
            'Ã±a': 'na',  # Para palabras como 'acompaÃ±ado'
            'Ã¼nica': 'unica',  # Para palabras con diéresis mal codificadas
            'Ã©tica': 'etica',  # Para palabras como 'polÃticas'
            'Ã¡nima': 'anima',  # Para 'mÃnima'
            'Ãºrica': 'urica',  # Para 'empÃrica'
            'Ãºna': 'una',  # Para 'mayorÃa'
            'Ã³r': 'or',  # Para 'estadÃstico'
            'Ã±icos': 'nicos',  # Para 'jurÃnicos'
            'Ãºltico': 'ultico',  # Para 'jurÃltico'
            'Ã¡frica': 'africa',  # Para 'Ãfrica'
            'Ã³nicos': 'onicos',  # Para 'polÃnicos'
            'Ã":': 'a',  # Para casos como 'kuwaitÃes'
            'Ã©tica': 'etica',  # Para palabras con 'polÃtica',
            'Ã±': 'ni'

        }
        processed_texts = []
        for text in X['Textos_espanol']:
            text = replace_percentage(text)
            text = replace_numbers(text)
            text = corregir_codificacion(text, reemplazos)
            text = to_lowercase(text)
            text = remove_punctuation(text)
            text = remove_accents(text)
            text = remove_stopwords(text)
            text = remove_non_ascii(text)
            tokens = word_tokenize(text)
            lemmas = lemmatize_verbs(tokens)
            processed_texts.append(' '.join(lemmas))
        return processed_texts  # Devuelve una lista de cadenas de texto

