#!/bin/python3

from cltk.stem.lemma import LemmaReplacer
from cltk.corpus.utils.formatter import cltk_normalize

lemmatizer = LemmaReplacer('greek')

text = """
μῆνιν ἄειδε θεὰ Πηληϊάδεω ̓Αχιλῆος
οὐλομένην, ἣ μυρί' ̓Αχαιοῖς ἄλγε' ἔθηκε,
πολλὰς δ' ἰφθίμους ψυχὰς ̓́Αϊδι προί̈αψεν
ἡρώων, αὐτοὺς δὲ ἑλώρια τεῦχε κύνεσσιν
οἰωνοῖσί τε πᾶσι, Διὸς δ' ἐτελείετο βουλή,
ἐξ οὗ δὴ τὰ πρῶτα διαστήτην ἐρίσαντε
Ατρεί̈δης τε ἄναξ ἀνδρῶν καὶ δῖος ̓Αχιλλεύς.
"""

#print(lemmatizer.lemmatize(text))
print(lemmatizer.lemmatize("Μῆνιν ἄειδε, θεά"))
print(lemmatizer.lemmatize(cltk_normalize("μῆνιν ἄειδε θεὰ Πηληϊάδεω ̓Αχιλῆος")))
# ... doesn't work without the normalization



