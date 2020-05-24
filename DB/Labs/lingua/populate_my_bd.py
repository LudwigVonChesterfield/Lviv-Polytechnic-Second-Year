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

		self.username = self.gen_username()
		self.email = self.gen_email()

		self.my_permissions = []
		self.my_teams = []
		self.my_groups = []
		self.my_notes = []

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

	def add_note(self, note):
		self.my_notes.append(note)

	def gen_relations(self):
		group_am = random.randint(0, int((len(GROUPS) - 1) * 0.3))
		for i in range(group_am):
			group = random.choice(GROUPS)
			self.my_groups.append(group)

			for team in group.my_teams:
				if random.randint(0, 100) <= 30:
					self.my_teams.append(team)

		for note in self.my_notes:
			self.my_permissions += note.my_permissions
			_tags = [] + TAGS
			for i in range(5):
				if random.randint(0, 100) <= 30:
					tag = random.choice(_tags)
					note.my_tags.append(tag)
					_tags.remove(tag)

		for group in self.my_groups:
			for perm in self.my_permissions:
				if random.randint(0, 100) <= 30:
					group.my_permissions.append(perm)
					for team in  group.my_teams:
						if random.randint(0, 100) <= 30:
							team.my_permissions.append(perm)

	def serialize(self):
		return "INSERT INTO user (username, email) VALUES (\"" + self.username + "\", \"" + self.email + "\");"


class Tag:
	def __init__(self):
		self.id = None

		self.name = self.gen_name()
		self.color = gen_hexcolor()
		self.background = gen_hexcolor()
		self.priority = random.randint(0, 10)

	def gen_name(self):
		n = parse("&PATTERN&")
		while n in TAKEN_TAGS:
			n = parse("&PATTERN&")
		TAKEN_TAGS.append(n)
		return n

	def serialize(self):
		return "INSERT INTO tag (name, color, background, priority) VALUES (\"" + self.name + "\", \"" + self.color + "\", \"" + self.background + "\", " + str(self.priority) + ");"


class Note:
	def __init__(self):
		self.id = None

		self.content = self.gen_sentence()
		self.created = random.randint(1576140000, 1577144800)

		author = random.choice(USERS)
		author.add_note(self)

		self.my_permissions = []
		self.my_tags = []

	def gen_sentence(self, sent_len=100):
		return parser.gen_text(sent_len)

	def add_permission(self, permission):
		self.my_permissions.append(permission)

	def serialize(self):
		return "INSERT INTO note (content, created) VALUES (\"" + self.content + "\", " + str2date(str(self.created)) + ");"


class Group:
	def __init__(self):
		self.id = None

		self.name = self.gen_name()

		self.my_teams = []
		self.my_permissions = []

	def gen_name(self):
		n = parse("&NOUN&&VERB&")
		while n in TAKEN_GROUPNAMES:
			n = parse("&NOUN&&VERB&")
		TAKEN_GROUPNAMES.append(n)
		return n

	def add_team(self, team):
		self.my_teams.append(team)

	def serialize(self):
		return "INSERT INTO note_group (name) VALUES (\"" + self.name + "\");"


class Permission:
	def __init__(self):
		self.id = None

		note = random.choice(NOTES)

		self.note_id = note.id
		self.permission = self.gen_name()

		note.add_permission(self)

	def gen_name(self):
		n = parse("&COLOR&&VERB&")
		return n

	def serialize(self):
		return "INSERT INTO permission (note_id, permission) VALUES (" + str(self.note_id) + ", \"" + self.permission + "\");"

class Team:
	def __init__(self):
		self.id = None

		group = random.choice(GROUPS)

		self.note_group_id = group.id
		self.name = self.gen_name()

		self.my_permissions = []

		group.add_team(self)

	def gen_name(self):
		n = parse("&ADVERB&&VERB&")
		return n

	def serialize(self):
		return "INSERT INTO team (note_group_id, name) VALUES (" + str(self.note_group_id) + ", \"" + self.name + "\");"

# SET THIS TO REGULATE HOW MANY ENTRIES WILL BE IN DATABASE.
user_am = 5

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
