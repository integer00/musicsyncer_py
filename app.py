#!/usr/local/opt/python3/bin/python3

#### MUSIC SYNCER \ TRANSFER \ CODEC FFMPEG

#####################################
#                                   #
#  ~/.config/msyncer config file    #
#  make upload function             #
#  make sync function               #
#  make convert function            #
#  make edit function               #
#                                   #
#                                   #
#                                   #
#                                   #
#                                   #
#####################################

##USAGE
# app config [test,prod]
# app upload [song ...] - uploads list of songs to server
# app sync - sync folder with end server


##todo-USAGE
# app convert ./ --mp3 --high  - converts in ./ everything in mp3
# app edit song.mp3 - opens vim and show's song tags in JSON


##convert stuff##
# within folder find all mysic files and convert them as mp3
# then old old shit



##1show diff folder<->player

##2 sync files with player
# mtp is peace of shit, apple did it better - it find's iphone and just sync shit whenever phone is connected or not
# should have phone client for listening events to update library

# so, the syntax should be like:
#   app upload <file.mp3>|<file.mp3> ...|<folder>


##3decode files to mp3 with ffmpeg
# will be good to disperse cue file to flac files

##config file in ~/.syncer.conf
# compare to previous music


# folders as key(?)
# "eng":
#      "Rock":
#           "Eagles": [
#                       "name": "Eagles - hotel california",
#                       "path": "/garbage/music/eng/rock/eagles-hotel california.mp3",
#                       "etc": "etc",
#                      ]
#

from pathlib import Path
import configparser
import argparse
import os
import sys
import webdav3.client as wc

# todo do parallelism for fast converting
# todo map of music content?
# todo idv3 tags

class Syncer(object):
	def __init__(self, config):
		self.ip_address = config['config']['phone']['ip_address']
		self.port = config['config']['phone']['port']
		self.root_dir = config['config']['phone']['root_dir']
		self.path = config['path']

		# make parser
		parser = argparse.ArgumentParser()
		sub_parser = parser.add_subparsers(dest='choose')

		config_parser = sub_parser.add_parser('config')
		upload_parser = sub_parser.add_parser('upload')
		sync_parser = sub_parser.add_parser('sync')
		convert_parser = sub_parser.add_parser('convert')

		config_parser.add_argument('config', nargs='?', choices=['test', 'prod'], default='test')
		upload_parser.add_argument('data_upload', type=str, nargs='+')
		sync_parser.add_argument('data_sync', type=str, nargs=1)
		convert_parser.add_argument('data_convert', type=str, nargs='+')

		if len(sys.argv) == 1:
			parser.print_usage()
			exit(0)
		args = parser.parse_args()

		if args.choose == 'config':
			make_config(self.path, args.config)
		if args.choose == 'upload':
			self.upload(args.data_upload)
		if args.choose == 'sync':
			self.sync(args.data_sync)
		if args.choose == 'convert':
			self.convert(args.data_convert)

	def upload(self, data_upload):
		#upload file like app upload file santana.mp3 -> creates {ROOT_DIR}/santana.mp3
		#upload folder like app upload dir this    -> creates {ROOT_DIR}/this

		options = {'webdav_hostname': "http://" + self.ip_address + ":" + self.port}
		client = wc.Client(options)

		if not client.check(self.root_dir):
			client.mkdir(self.root_dir)

		if data_upload:
			for each in data_upload:
				ap = os.path.abspath(each)
				print("uploading " + ap)
				if os.path.isdir(ap):
					if each == '.':
						client.upload(self.root_dir + os.path.dirname(each), ap)
						break
					client.upload(self.root_dir + "/" + each, ap)
				else:
					client.upload(self.root_dir + "/" + each, ap)

	def sync(self, data_sync):

		#todo fix
		if data_sync is None:
			print('none')
			exit(0)

		options = {'webdav_hostname': "http://" + self.ip_address + ":" + self.port}
		client = wc.Client(options)

		if not client.check(self.root_dir):
			client.mkdir(self.root_dir)

		if not os.path.isdir(data_sync[0]):
			print("You should pass a folder")
			exit(1)

		client.push_force(self.root_dir, data_sync[0])

	def convert(self, data_convert):
		print("converting")


def make_config(config_path,config_type='default'):
	config_default = configparser.ConfigParser()

	def create(choice):

		if choice == 'prod':
			config_default['phone'] = {'ip_address': '10.0.0.6', 'port': '8080', 'root_dir': '/sync'}
			print("prod config was created")
		if choice == 'test' or choice == 'default':
			config_default['phone'] = {'ip_address': '127.0.0.1', 'port': '8080', 'root_dir': '/sync'}
			print("test config was created")
		with open(config_path, 'w+') as configFile:
			config_default.write(configFile)

	if config_type == 'prod':
		create('prod')
		exit(0)
	if config_type == 'test':
		create('test')
		exit(0)
	else:
		create('default')


def run(config):
	s = Syncer(config)


def main():
	settings = {}
	config_parser = configparser.ConfigParser()

	home_dir = str(Path.home())
	config_path = Path(home_dir + '/.config/msyncer')

	if Path.exists(config_path):
		pass
	else:
		print('config file not found, creating one...')
		make_config(config_path)

	config_parser.read(config_path)

	settings["path"] = config_path
	settings["config"] = config_parser

	run(settings)

#
# def convert(i):
# 	print("working on " + i)
# 	subprocess.call([
# 		"ffmpeg",
# 		"-y",
# 		"-i", i,
# 		"-acodec", "libmp3lame",
# 		"-ar", "44100",
# 		"-b:a", "320k",
# 		i + ".mp3"
# 	])


#
# for each in args['convert']:
#     print(each)
# print(args['convert'][0])

# commands = [
#     'ffmpeg -i ' + args['convert'][0] + ' -acodec libmp3lame -ar 44100 -b:a 320k out1.mp3',
#     'ffmpeg -i ' + args['convert'][1] + ' -acodec libmp3lame -ar 44100 -b:a 320k out2.mp3',
# ]
# processes = [Popen(cmd, shell=True) for cmd in commands]
# for p in processes: p.wait()

# for each in args['convert']:
#     threading.Thread(target=doWork(each)).start()
#
#
# print("done with " + str(args['convert']))


if __name__ == '__main__':
	main()
