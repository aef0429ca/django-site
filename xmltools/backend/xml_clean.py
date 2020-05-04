import os
import django_project.settings as settings
# import logging

# Reads file from documents and xmllints it into documents/tmp
def pretty_print(file):
	# os.system(" ".join(['xmllint', '--format', '--encode', 'utf-8', os.path.join(DOC_PATH, file), '>', os.path.join(TMP_PATH, file)]))
	os.system(" ".join(['xmllint', '--format', '--noblanks', '--nocdata' , '--encode', 'utf-8', os.path.join(settings.DOC_ROOT, file), '>', os.path.join(settings.TMP_PATH, file)]))
	# logging.warning("Running xmllint function")
	

	return True

# Reads file from documents/tmp and greps it to documents/final
def filter_tags(file, tags):
	tag_file = tags.lower() + 'tags.txt'
	os.system(" ".join(['grep', '-f', os.path.join(settings.TAGS_PATH, tag_file), os.path.join(settings.TMP_PATH, file), '>', os.path.join(settings.FINAL_PATH, file)]))
	# msg = " ".join(['grep', '-f', str(os.path.join(settings.TAGS_PATH, tag_file)), str(os.path.join(settings.TMP_PATH, file)), '>', str(os.path.join(settings.FINAL_PATH, file))])
	# logging.warning(" ".join(['grep syntax', msg]))

	return True
