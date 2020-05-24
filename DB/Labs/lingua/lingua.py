import random
import re

import global_vars as gl

import irregularVerbs

from token_types import Token, Verb_Token, Capitalize_Token

NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
HEX = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
VOWELS = ["a", "e", "i", "o", "u", "y"]
CONSONANTS = [
			"b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p",
			"q", "r", "s", "t", "v", "x", "z"
		]

NOUNS = ["person", "dog", "cat", "snail", "shark", "fish", "lover", "hater", "nobody"]
ADJECTIVES = ["robust", "quick", "fast", "slow", "another", "&NOUN&-loving", "&NOUN&-hating"]
ADVERBS = ["happily", "&ADJECTIVE&ly"]
VERBS = ["transport", "teleport", "gnaw", "create", "arise", "awake", "backslide", "be", "bear"]

SYLLABLES = ["&CONSONANT&&VOWEL&", "&CONSONANT&&CONSONANT&&VOWEL&", "&CONSONANT&&VOWEL&&VOWEL&"]
WORDS = ["&SYLLABLE&", "&SYLLABLE&&SYLLABLE&", "&SYLLABLE&&SYLLABLE&&SYLLABLE&", "&SYLLABLE&&SYLLABLE&&SYLLABLE&&SYLLABLE&"]
PATTERNS = ["&ADJECTIVE& &NOUN&", "&NOUN&"]
SENTENCES = ["&PATTERN& &VERB_3RD& &PATTERN&", "&PATTERN& &ADVERB& &VERB_P& &PATTERN&"]

DELIMETERS = [".", ",", "!", "?", ";", "", ":"]
SENTENCE_ENDS = [".", "!", "?"]

TEXTS = [
	"&CAPITALIZE&&SENTENCE&&SENTENCE_END&",
	"&CAPITALIZE&&SENTENCE&&DELIMETER& &SENTENCE&&SENTENCE_END&",
	"&CAPITALIZE&&SENTENCE&&DELIMETER& &SENTENCE&&DELIMETER& &SENTENCE&&SENTENCE_END&"]

DEF_LOOKUP = {
	"NOUN": {
		"examplars": NOUNS,
	},
	"ADJECTIVE": {
		"examplars": ADJECTIVES,
	},
	"ADVERB": {
		"examplars": ADVERBS,
	},
	"VERB": {
		"examplars": VERBS,
		"token_type": Verb_Token,
	},
	"SYLLABLE": {
		"examplars": SYLLABLES,
	},
	"WORD": {
		"examplars": WORDS,
	},
	"PATTERN": {
		"examplars": PATTERNS,
	},
	"SENTENCE": {
		"examplars": SENTENCES,
	},
	"NUMBER": {
		"examplars": NUMBERS,
	},
	"HEX": {
		"examplars": HEX,
	},
	"VOWEL": {
		"examplars": VOWELS,
	},
	"CONSONANT": {
		"examplars": CONSONANTS,
	},
	"DELIMETER": {
		"examplars": DELIMETERS,
	},
	"SENTENCE_END": {
		"examplars": SENTENCE_ENDS,
	},
	"TEXT": {
		"examplars": TEXTS,
	},
	"CAPITALIZE": {
		"technical": True,
		"token_type": Capitalize_Token,
	},
}


class Lingua:
	def __init__(self, lookup=DEF_LOOKUP, debug=False):
		self.debug = debug
		self.debug_msg(str(debug))

		self.PARSE_SYMBOL = "&"

		self.lookup = lookup

		self.parse_tokens = []
		self.proper_tokens = []
		self.tech_tokens = []

	def add_lookup(self, token_key, token_obj, force=False):
		if not force and token_key in self.lookup.keys():
			self.lookup[token_key]["examplars"] += token_obj["examplars"]
		else:
			self.lookup[token_key] = token_obj

	def init(self):
		for token_key in self.lookup.keys():
			token_obj = self.lookup[token_key]

			self.make_token(token_key, token_obj, self.parse_tokens)

	def debug_msg(self, msg):
		if self.debug:
			print("DEBUG: " + msg)

	def check_proper(self, msg):
		return msg.find(self.PARSE_SYMBOL) == -1

	def make_token(self, key, token_obj, to_list, list_key="examplars"):
		token_type = Token
		if "token_type" in token_obj.keys():
			token_type = token_obj["token_type"]

		if "technical" in token_obj.keys():
			self.tech_tokens.append(token_type(key, self.PARSE_SYMBOL))
			return

		if list_key == "examplars":
			self.gen_proper(key, token_obj, token_type=token_type)

		if len(token_obj[list_key]) == 0:
			self.debug_msg(key + "_" + list_key + " has no elements. Some tokens may not be replaced.")
			return
		to_list.append(token_type(key, self.PARSE_SYMBOL, token_obj[list_key]))

	def gen_proper(self, key, token_obj, token_type=Token):
		token_obj["proper"] = []
		for item in token_obj["examplars"]:
			if self.check_proper(item):
				token_obj["proper"].append(item)
		self.make_token(key, token_obj, self.proper_tokens, list_key="proper")

	def process_with_tokens(self, msg, tokens):
		for token in tokens:
			msg = token.process(msg)
		return msg

	def parse(self, msg, iterations_lim=20):
		old_msg = None
		while msg != old_msg and iterations_lim > 0:
			old_msg = msg
			msg = self.process_with_tokens(msg, self.parse_tokens)
			iterations_lim -= 1

		# It stopped "parsing" abruptly. There may be some unparsed tokens.
		if iterations_lim <= 0:
			msg = self.process_with_tokens(msg, self.proper_tokens)

		# Capitalization tokens, and other misc.
		msg = self.process_with_tokens(msg, self.tech_tokens)
		return msg

	def gen_text(self, min_len=50):
		txt = ""
		while len(txt) <= min_len:
			txt += self.parse("&TEXT&") + " "
		txt += self.parse("&TEXT&")
		return txt


if __name__ == "__main__":
	parser = Lingua()
	parser.init()

	# print(parser.parse("&WORD& &WORD& &WORD&&SENTENCE_END&"))
	print(parser.gen_text(1000))
