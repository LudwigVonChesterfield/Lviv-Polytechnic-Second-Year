import random
import datetime

from lingua import Lingua

NOUNS = {
	"examplars":  ["database", "software", "hardware", "frontend", "backend", "coffee", "some&NOUN&", "king", "body", "no&NOUN&", "anonymous", "bot", "not-a-&NOUN&", "total&CAPITALIZE&&NOUN&"],
}
ADJECTIVES = {
	"examplars": ["cool", "robust", "responsible", "readable", "random", "feeling", "enjoyable", "unreal", "real", "rational", "irrational", "subprime", "&COLOR&"],
}

COLORS = {
	"examplars": ["red", "orange", "yellow", "green", "cyan", "blue", "violet", "gray", "black", "white"],
}

EMAILS = {
	"examplars": ["yahoo", "inbox", "gmail", "fastmail", "sendreceive"],
}
DOMAINS = {
	"examplars": ["com", "org", "net", "mail"],
}

PATTERNS = {
	"examplars": ["&CAPITALIZE&&NOUN&", "&ADJECTIVE&&NOUN&", "&CAPITALIZE&&ADJECTIVE&&CAPITALIZE&&NOUN&"],
}

LANGUAGES = {
	"examplars": ["&NAME&Script", "&LANGUAGE&+", "&LANGUAGE&++", "&CONSONANT&", "&NOUN&", "&SYLLABLE&"]
}

TAKEN_USERNAMES = []
TAKEN_EMAILS = []
TAKEN_TAGS = []
TAKEN_GROUPNAMES = []

USERS = []
TAGS = []
NOTES = []
GROUPS = []
PERMISSIONS = []
TEAMS = []

parser = Lingua()
parser.add_lookup("NOUN", NOUNS)
parser.add_lookup("ADJECTIVE", ADJECTIVES)
parser.add_lookup("EMAIL", EMAILS)
parser.add_lookup("DOMAIN", DOMAINS)
parser.add_lookup("COLOR", COLORS)
parser.add_lookup("PATTERN", PATTERNS, force=True)
parser.add_lookup("LANGUAGE", LANGUAGES)
parser.init()

def parse(msg):
	return parser.parse(msg)


def gen_hexcolor():
	return parse("#&HEX&&HEX&&HEX&&HEX&&HEX&&HEX&")


def add_relation(table, id1, id2, field1, field2):
	return "INSERT INTO " + table + " (" + field1 + ", " + field2 + ") VALUES (" + str(id1) + ", " + str(id2) + ");" 


def str2date(txt):
	return "FROM_UNIXTIME(" + txt + ")"


class User:
	def __init__(self):
		self.id = None

		self.super_secret = self.gen_super_secret()
		self.secret_salt = self.gen_salt()

		self.name = self.gen_username()
		self.email = self.gen_email()

		self.google_id = random.randint(1000000, 9999999)
		self.discord_id = random.randint(1000000, 9999999)
		self.facebook_id = random.randint(1000000, 9999999)
		self.permission = 0
		if random.randint(0, 100) >= 10:
			self.permission += random.randint(1, 10)

	def gen_username(self):
		n = parse("&PATTERN&")
		while n in TAKEN_USERNAMES:
			n = parse("&PATTERN&")
		TAKEN_USERNAMES.append(n)
		return n

	def gen_email(self):
		e = parse("&NOUN&@&EMAIL&.&DOMAIN&")
		while e in TAKEN_EMAILS:
			e = parse("&NOUN&@&EMAIL&.&DOMAIN&")
		TAKEN_EMAILS.append(e)
		return e

	def gen_super_secret(self):
		s = parse("&WORD&&WORD&&WORD&&WORD&&WORD&&WORD&&WORD&&WORD&&WORD&&WORD&")
		return s

	def gen_salt(self):
		s = parse("&WORD&&WORD&&WORD&&WORD&&WORD&&WORD&&WORD&&WORD&&WORD&&WORD&")
		return s

	def gen_relations(self):
		return

	def serialize(self):
		return "INSERT INTO user (super_secret, secret_salt, name, email, google_id, discord_id, facebook_id, permission) VALUES" + 
		" (\"" + self.super_secret + ", " self.secret_salt + ", " + self.name + ", " + self.email + ", " + str(google_id) + ", " + str(discord_id) + ", " +
		str(facebook_id) + ", " + str(permission) "\");"


class Test_Case:



class Language:



class Solution:



class Review:



class Result:



class Comment:



class Profile_Picture:



class Source:




# SET THIS TO REGULATE HOW MANY ENTRIES WILL BE IN DATABASE.
user_am = 5

test_case = 

tag_am = int(user_am * 1.5)

notes_am = int(user_am * 5)
permissions_am = int(notes_am * 2)

groups_am = int(user_am * 0.9)
teams_am = int(groups_am * 2.5)

for i in range(user_am):
	u = User()
	u.id = i + 1
	USERS.append(u)

for i in range(tag_am):
	t = Tag()
	t.id = i + 1
	TAGS.append(t)

for i in range(notes_am):
	n = Note()
	n.id = i + 1
	NOTES.append(n)

for i in range(permissions_am):
	p = Permission()
	p.id = i + 1
	PERMISSIONS.append(p)

for i in range(groups_am):
	g = Group()
	g.id = i + 1
	GROUPS.append(g)

for i in range(teams_am):
	t = Team()
	t.id = i + 1
	TEAMS.append(t)



for user in USERS:
	user.gen_relations()


def main():
	with open('populateScript.sql', 'w+') as f:
		dump = ""

		dump += "-- USERS ARE HERE\n"
		dump += "DELETE FROM user;\n"
		for user in USERS:
			dump += user.serialize() + "\n"

		dump += "\n-- TAGS ARE HERE\n"
		dump += "DELETE FROM tag;\n"
		for tag in TAGS:
			dump += tag.serialize() + "\n"

		dump += "\n-- NOTES ARE HERE\n"
		dump += "DELETE FROM note;\n"
		for note in NOTES:
			dump += note.serialize() + "\n"

		dump += "\n-- PERMISSIONS ARE HERE\n"
		dump += "DELETE FROM permission;\n"
		for permission in PERMISSIONS:
			dump += permission.serialize() + "\n"

		dump += "\n-- GROUPS ARE HERE\n"
		dump += "DELETE FROM note_group;\n"
		for group in GROUPS:
			dump += group.serialize() + "\n"

		dump += "\n-- TEAMS ARE HERE\n"
		dump += "DELETE FROM team;\n"
		for team in TEAMS:
			dump += team.serialize() + "\n"

		dump += "\n-- USER-GROUPS RELATIONS ARE HERE\n"
		dump += "DELETE FROM user_note_groups;\n"
		for user in USERS:
			for group in user.my_groups:
				dump += add_relation("user_note_groups", user.id, group.id, "id_user", "id_note_groups") + "\n"

		dump += "\n-- USER-TEAMS RELATIONS ARE HERE\n"
		dump += "DELETE FROM user_teams;\n"
		for user in USERS:
			for team in user.my_teams:
				dump += add_relation("user_teams", user.id, team.id, "id_user", "id_team") + "\n"

		dump += "\n-- USER-NOTES RELATIONS ARE HERE\n"
		dump += "DELETE FROM user_notes;\n"
		for user in USERS:
			for note in user.my_notes:
				dump += add_relation("user_notes", user.id, note.id, "id_user", "id_note") + "\n"

		dump += "\n-- NOTE-TAGS RELATIONS ARE HERE\n"
		dump += "DELETE FROM note_tags;\n"
		for note in NOTES:
			for tag in note.my_tags:
				dump += add_relation("note_tags", note.id, tag.id, "note_id", "tag_id") + "\n"

		dump += "\n-- USER-PERMISSIONS RELATIONS ARE HERE\n"
		dump += "DELETE FROM user_permissions;\n"
		for user in USERS:
			for permission in user.my_permissions:
				dump += add_relation("user_permissions", user.id, permission.id, "user_id", "permission_id") + "\n"

		dump += "\n-- GROUP-PERMISSIONS RELATIONS ARE HERE\n"
		dump += "DELETE FROM note_group_permissions;\n"
		for group in GROUPS:
			for permission in group.my_permissions:
				dump += add_relation("note_group_permissions", group.id, permission.id, "note_group_id", "permission_id") + "\n"

		dump += "\n-- TEAM-PERMISSIONS RELATIONS ARE HERE\n"
		dump += "DELETE FROM team_permissions;\n"
		for team in TEAMS:
			for permission in team.my_permissions:
				dump += add_relation("team_permissions", team.id, permission.id, "team_id", "permission_id") + "\n"

		f.write(dump)

main()
