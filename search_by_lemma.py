#!/bin/python3

from cltk.corpus.utils.importer import CorpusImporter
from cltk.corpus.readers import get_corpus_reader
from cltk.stem.lemma import LemmaReplacer
from cltk.corpus.utils.formatter import cltk_normalize
from cltk.tag.pos import POSTag
import nltk
import re,sys

if False: # first time
  corpus_importer = CorpusImporter('greek')
  corpus_importer.import_corpus('greek_text_perseus')
  corpus_importer.import_corpus('greek_text_tesserae')
  nltk.download('punkt')


lemmatizer = LemmaReplacer('greek')

tagger = POSTag('greek')

def main():
  if len(sys.argv)<2:
    print("Please supply an inflected word on the command line. Example: search_by_lemma.py κύνεσσιν\n")
    sys.exit()
  infl = sys.argv[1]
  #infl = "κύνεσσιν" # inflected form of work we're looking up
  lem = lemmatize(infl)[0] # lemmatized
  print("searching for "+lem+" <- "+infl)
  index = {}
  for work in ["iliad","odyssey"]:
    for book in range(1,24+1): # ranges from 1 to 24
      filename = 'texts/homer.'+work+'.part.'+str(book)+'.tess'
      #print(filename)
      reader = get_corpus_reader( corpus_name = 'greek_text_tesserae', language = 'greek')
      reader._fileids = [filename]
      sentences = list(reader.sents([filename]))
      sentences = [cltk_normalize(s) for s in sentences]
      count_sentences = 0
      for s in sentences:
        count_sentences = count_sentences+1
        no_punct = re.sub(r"[,;:\.']",'',s) # remove punctuation, which lemmatizer treats as independent words
        words = re.split("\s+", no_punct)
        count_words = 0
        for word in lemmatize(no_punct):
          count_words = count_words+1
          if lem==word:
            i = count_words-1
            w = words[i]
            context = " ".join(words[max(i-3,0):min(i+4,len(words)-1)])
            #context = re.sub(re.compile("("+w+")"),r"__\1__",context) # ... surround with __ __
            pos_tagged = tagger.tag_tnt(no_punct)
            # ... tag words in sentence with parts of speech, https://github.com/cltk/tutorials/blob/master/8%20Part-of-speech%20tagging.ipynb
            # for descriptions of what the POS tags mean, see https://linguistics.stackexchange.com/questions/12803/what-do-the-labels-mean-in-this-latin-pos-tagging
            describe = w
            for t in pos_tagged:
              if t[0]==w:
                describe = t[0]+" "+pos_tag_to_description(t[1])
                break
            print(work+" "+str(book)+", sentence "+str(count_sentences)+", word "+str(count_words)+": "+describe+"    "+context)
            if w in index:
              index[w] += 1
            else:
              index[w] = 1
        #sys.exit()
  for w in sorted(list(index.keys())):
    print(str(index[w])+" "+w)

def pos_tag_to_description(tag):
  # example: N-P---NA-
  # https://github.com/cltk/latin_treebank_perseus
  tag = tag.lower()
  part_of_speech = tag[0]
  person = tag[1]
  number = tag[2]
  tense = tag[3]
  mood = tag[4]
  voice = tag[5]
  gender = tag[6]
  case = tag[7]
  degree = tag[8]
  d = []
  d = h(d,{'n':'noun','v':'verb'},part_of_speech)
  d = h(d,{'1':'1st p.','1':'2nd p.','3':'3rd p.'},person)
  d = h(d,{'s':'sing.','p':'pl.'},number)
  d = h(d,{'m':'masc.','d':'fem.','n':'neut.'},gender)
  d = h(d,{'n':'nom.','g':'gen.','d':'dat.','a':'acc.','b':'abl.','v':'voc.','l':'loc.'},case)
  return ' '.join(d)

def h(d,dict,key):
  if key=='-':
    return d
  if key in dict:
    s = dict[key]
  else:
    s = key
  return d+[s]

def lemmatize(s):
  # returns an array
  return lemmatizer.lemmatize(cltk_normalize(s))
  # ... without the normalization, it often fails silently
  #     https://github.com/cltk/cltk/issues/968

main()
