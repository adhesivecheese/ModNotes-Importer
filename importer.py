import praw
import pmtw
from datetime import datetime

reddit = praw.Reddit(
	client_id="my client id",
	client_secret="my client secret",
	user_agent="my user agent",
)
sub = input("Subreddit to import usernotes for: ")
subreddit = reddit.subreddit(sub)
toolbox = pmtw.Toolbox(subreddit)

mapping = {}

mn = {
	  '0': None
	, '1': 'BOT_BAN'
	, '2': 'PERMA_BAN'
	, '3': 'BAN'
	, '4': 'ABUSE_WARNING'
	, '5': 'SPAM_WARNING'
	, '6': 'SPAM_WATCH'
	, '7': 'SOLID_CONTRIBUTOR'
	, '8': 'HELPFUL_USER'
	}

print("Mod Notes Mappings:")
print(mn)
for x in toolbox.settings.usernoteColors:
	map = input(f"{x.text}: ")
	mapping[x.key] = mn[map]

prependTime = False
x = input("Prepend the toolbox timestamp in UTC to the usernote? Y/N: ")
if x.lower() == "y" or x.lower() == "yes":
	prependTime = True

prependUrl = False
x = input("Prepend the url to the usernote text? Y/N: ")
if x.lower() == "y" or x.lower() == "yes":
	prependUrl = True

trimLongNotes = False
x = input("Mod Notes may only be 250 characters. Type Yes to trim, or No to discard and notify: ")
if x.lower() == "y" or x.lower() == "yes":
	trimLongNotes = True

deleteAfterImport = False
x = input("Delete usernotes from toolbox after importing? Y/N: ")
if x.lower() == "y" or x.lower() == "yes":
	deleteAfterImport = True

importCount = 0
for note in toolbox.usernotes.list_all_notes():
	preparedNote = note.note
	if prependUrl:
		preparedNote = f"[{note.url}] {preparedNote}"
	if prependTime:
		preparedNote = f"({datetime.utcfromtimestamp(note.time).strftime('%y-%m-%d %H:%M:%S')} UTC) {preparedNote}"
	if trimLongNotes:
		if len(preparedNote) > 250:
			preparedNote = preparedNote[0:249] + "…"

	if len(preparedNote) <= 250:
		subreddit.mod.notes.create(
			  label = mapping[note.warning]
			, note = preparedNote
			, redditor = note.user
		)
		if deleteAfterImport:
			toolbox.usernotes.remove(note.user,note.time, lazy=True)
			importCount += 1
	else:
		print(f"note {note} too long to import")
	
if importCount > 0:
	toolbox.usernotes.save(f"Deleted {importCount} Toolbox usernotes imported into native Mod Notes")
