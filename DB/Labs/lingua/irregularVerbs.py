import global_vars as gl

from token_types import Verb_Token

def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


class IrregularVerb:
	root = ""
	third_person = ""
	present = ""
	past_simple = ""
	past_simple_plural = ""
	past_participle = ""
	past_participle_third_person = ""

	def __init__(self):
		temp_token = Verb_Token("PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER")

		self.root = self.__class__.root
		self.third_person = self.__class__.third_person
		self.present = self.__class__.present
		self.past_simple = self.__class__.past_simple
		self.past_simple_plural = self.__class__.past_simple_plural
		self.past_participle = self.__class__.past_participle
		self.past_participle_third_person = self.__class__.past_participle_third_person

		if self.third_person == "":
			self.third_person = temp_token.verb_form(self.root, gl.VERB_THIRD_PERSON, check_irregulars=False)
		if self.present == "":
			self.present = temp_token.verb_form(self.root, gl.VERB_PRESENT, check_irregulars=False)
		if self.past_simple == "":
			self.past_simple = temp_token.verb_form(self.root, gl.VERB_PAST_SIMPLE, check_irregulars=False)
		if self.past_simple_plural == "":
			self.past_simple_plural = self.past_simple
		if self.past_participle == "":
			self.past_participle = temp_token.verb_form(self.root, gl.VERB_PAST_PARTICIPLE, check_irregulars=False)
		if self.past_participle_third_person == "":
			self.past_participle_third_person = temp_token.verb_form(self.root, gl.VERB_PAST_PARTICIPLE, gl.PERSON_THIRD, check_irregulars=False)

	def form(self, form, person=gl.PERSON_FIRST):
		if form == gl.VERB_ROOT:
			return self.root
		if form == gl.VERB_THIRD_PERSON:
			return self.third_person
		if form == gl.VERB_PRESENT:
			return self.present
		if form == gl.VERB_PAST_SIMPLE:
			if person == gl.PERSON_PLURAL:
				return self.past_simple_plural
			return self.past_simple
		if form == gl.VERB_PAST_PARTICIPLE:
			if person == gl.PERSON_THIRD:
				return self.past_participle_third_person
			return self.past_participle


class AriseVerb(IrregularVerb):
	root = "arise"
	past_simple = "arose"
	past_participle = "arisen"

class AwakeVerb(IrregularVerb):
	root = "awake"
	past_simple = "awoke"
	past_participle = "awoken"

class BackslideVerb(IrregularVerb):
	root = "backslide"
	past_simple = "backslid"
	past_participle = "backslid"

class BeVerb(IrregularVerb):
	root = "be"
	third_person = "is"
	present = "being"
	past_simple = "was"
	past_simple_plural = "were"
	past_participle = "been"

class BearVerb(IrregularVerb):
	root = "bear"
	past_simple = "bore"
	past_participle = "borne"


for verb_class in all_subclasses(IrregularVerb):
	verb = verb_class()
	gl.IRREGULAR_VERBS[verb.root] = verb
