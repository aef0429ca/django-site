import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DOC_PATH = os.path.join(BASE_DIR, 'media/documents')
TMP_PATH = os.path.join(BASE_DIR, 'media/documents/tmp')
FINAL_PATH = os.path.join(BASE_DIR, 'media/documents/final')

def pretty_print(file):
	# os.system(" ".join(['xmllint', '--format', '--encode', 'utf-8', os.path.join(DOC_PATH, file), '>', os.path.join(TMP_PATH, file)]))
	os.system(" ".join(['xmllint', '--format', '--noblanks', '--nocdata' , '--encode', 'utf-8', os.path.join(DOC_PATH, file), '>', os.path.join(TMP_PATH, file)]))

	return True


def filter_tags(file, tags):
	tag_file = tags.lower() + 'tags.txt'
	os.system(" ".join(['grep', '-f', os.path.join(DOC_PATH, 'tags', tag_file), os.path.join(TMP_PATH, file), '>', os.path.join(FINAL_PATH, file)]))

	return True
