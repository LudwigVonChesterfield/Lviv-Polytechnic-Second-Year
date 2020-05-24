import random

import global_vars as gl

class Token:
	def __init__(self, key, symbol, lookup):
		self.replace_key = symbol + key + symbol
		self.lookup = lookup

	def process(self, msg):
		old_msg = msg
		msg = msg.replace(self.replace_key, random.choice(self.lookup), 1)
		if msg != old_msg:
			self.process(msg)
		return msg


class Verb_Token:
	def __init__(self, key, symbol, lookup):
		self.verb_root_pat = symbol + key + symbol
		self.verb_third_pers_pat = symbol + key + "_3RD" + symbol
		self.verb_present_pat = symbol + key + "_P" + symbol
		self.verb_past_simple_pat = symbol + key + "_PS" + symbol
		self.verb_past_participle_pat = symbol + key + "_PP" + symbol
		self.verb_past_participle_third_pers_pat = symbol + key + "_PP_3RD" + symbol

		self.lookup = lookup

	def process(self, msg):
		old_msg = msg
		has_changed = msg
		verb = random.choice(self.lookup)

		msg = msg.replace(self.verb_root_pat, verb, 1)
		if has_changed != msg:
			verb = random.choice(self.lookup)
			has_changed = msg

		msg = msg.replace(self.verb_third_pers_pat, self.verb_form(verb, gl.VERB_THIRD_PERSON), 1)
		if has_changed != msg:
			verb = random.choice(self.lookup)
			has_changed = msg

		msg = msg.replace(self.verb_present_pat, self.verb_form(verb, gl.VERB_PRESENT), 1)
		if has_changed != msg:
			verb = random.choice(self.lookup)
			has_changed = msg

		msg = msg.replace(self.verb_past_simple_pat, self.verb_form(verb, gl.VERB_PAST_SIMPLE), 1)
		if has_changed != msg:
			verb = random.choice(self.lookup)
			has_changed = msg

		msg = msg.replace(self.verb_past_participle_pat, self.verb_form(verb, gl.VERB_PAST_PARTICIPLE), 1)
		if has_changed != msg:
			verb = random.choice(self.lookup)
			has_changed = msg

		msg = msg.replace(self.verb_past_participle_third_pers_pat, self.verb_form(verb, gl.VERB_PAST_PARTICIPLE, gl.PERSON_THIRD), 1)
		if has_changed != msg:
			verb = random.choice(self.lookup)
			has_changed = msg

		if msg != old_msg:
			self.process(msg)
		return msg

	def verb_form(self, verb, form, person=gl.PERSON_FIRST, check_irregulars=True):
		if check_irregulars and verb in gl.IRREGULAR_VERBS.keys():
			return gl.IRREGULAR_VERBS[verb].form(form, person)

		if form == gl.VERB_ROOT:
			return verb
		if form == gl.VERB_THIRD_PERSON:
			return verb + "s"
		if form == gl.VERB_PRESENT:
			if verb[len(verb) - 1] == "e":
				verb = verb[:-1]
			return verb + "ing"
		if form == gl.VERB_PAST_SIMPLE:
			suffix = "ed"
			if verb[len(verb) - 1] == "e":
				suffix = "d"
			return verb + suffix
		if form == gl.VERB_PAST_PARTICIPLE:
			have_word = "have"
			if person == gl.PERSON_THIRD:
				have_word = "has"
			suffix = "ed"
			if verb[len(verb) - 1] == "e":
				suffix = "d"
			return have_word + " " + verb + suffix


class Capitalize_Token(Token):
	def __init__(self, key, symbol):
		self.split_key = symbol + key + symbol

	def process(self, msg):
		split_capitalization = msg.split(self.split_key)
		return ''.join([sub.capitalize() for sub in split_capitalization])
