#!/bin/python3

from cltk.corpus.utils.importer import CorpusImporter
from cltk.corpus.readers import get_corpus_reader
from cltk.stem.lemma import LemmaReplacer
from cltk.corpus.utils.formatter import cltk_normalize
from cltk.tag.pos import POSTag
import nltk

corpus_importer = CorpusImporter('greek')
corpus_importer.import_corpus('greek_text_perseus')
corpus_importer.import_corpus('greek_text_tesserae')
nltk.download('punkt')
