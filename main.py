import hashlib
import imghdr
import os
import time
import datetime
from PIL import Image

__author__ = 'andercruzbr'

DESTINATION_DIRECTORY = '/Users/andercruzbr/Development/Personal/PhotoOrganizer/dest'
SOURCE_DIRECTORY = '/Users/andercruzbr/Development/Personal/PhotoOrganizer/source'

def create_year_folder_if_not_exists(year: str):
	"""
	create_year_folder_if_not_exists
	:param year:
	:return:
	"""
	path = os.path.join(DESTINATION_DIRECTORY, year)
	if not os.path.exists(path):
		os.mkdir(path)


def create_month_folder_if_not_exists(month: str, year: str):
	"""
	create_mounth_folder_if_not_exists
	:param month:
	:param year:
	:return:
	"""
	create_year_folder_if_not_exists(year)
	path = os.path.join(DESTINATION_DIRECTORY, year, month)
	if not os.path.exists(path):
		os.mkdir(path)

def create_day_folder_if_not_exists(day:str, month:str, year: str):
	"""
	create_day_folder_if_not_exists
	:param day:
	:param month:
	:param year:
	:return:
	"""
	create_month_folder_if_not_exists(month, year)
	path = os.path.join(DESTINATION_DIRECTORY, year, month, day)
	if not os.path.exists(path):
		os.mkdir(path)


def check_file_exists(source_path: str, destination_path: str) -> str:
	"""
	check_file_exists
	:param source_path:
	:param destination_path:
	:return:
	"""
	if os.path.exists(destination_path):

		source_hash = None
		destination_hash = None

		with open(source_path, 'br') as f:
			file_content = f.read()
			md5Hash = hashlib.md5(file_content)
			source_hash = md5Hash.hexdigest()

		with open(destination_path, 'br') as f:
			file_content = f.read()
			md5Hash = hashlib.md5(file_content)
			destination_hash = md5Hash.hexdigest()

		if source_hash != destination_hash:
			dirname = os.path.dirname(destination_path)
			basename = os.path.basename(destination_path)
			head, tail = os.path.splitext(basename)
			count = 0
			while os.path.exists(destination_path):
				count += 1
				destination_path = os.path.join(dirname, "%s (%s)%s" % (head, count, tail))

	return destination_path


def move_photo(path: str):
	"""
	move_photo
	:param path:
	:return:
	"""
	if not imghdr.what(path):
		return

	# print(path)
	img = Image.open(path)
	created_in = datetime.datetime.strptime(time.ctime(os.path.getctime(path)), "%a %b %d %H:%M:%S %Y").strftime("%Y:%m:%d")
	# created_in = '1900:01:01'
	if hasattr(img, '_getexif'):
		exif = img._getexif()
		created_in = exif[36867] if exif and 36867 in exif else created_in
	dt = created_in.split(' ')[0].split(':')
	year = dt[0]
	month = dt[1]
	day = dt[2]
	create_day_folder_if_not_exists(day, month, year)
	dest = os.path.join(DESTINATION_DIRECTORY, year, month, day, os.path.basename(path))
	dest = check_file_exists(path, dest)
	print("Moving {0} to {1}".format(path, dest))
	os.rename(path, dest)


def organize_photos(path: str):
	"""
	organize_photos
	:param path:
	:return:
	"""
	for file in os.listdir(path):
		if os.path.isfile(os.path.join(path, file)):
			move_photo(os.path.join(path, file))
		elif os.path.isdir(os.path.join(path, file)):
			organize_photos(os.path.join(path, file))
		else:
			print("**** " + os.path.join(path, file))


if __name__ == '__main__':
	organize_photos(SOURCE_DIRECTORY)
