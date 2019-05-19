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

##usage
# app edit song.mp3 - opens vim and show's song tags in JSON
# app upload song.mp3 - uploads song to player
# app sync - sync folder with end device
# app convert ./ --mp3 --high  - converts in ./ everything in mp3

##convert stuff##
# within folder find all mysic files and convert them as mp3
# then old old shit
#


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

# todo do parallelism for fast convertion
# todo map of music content?
# todo config file ~/.syncer
# todo idv3 tags

home_dir = str(Path.home())
config_path = Path(home_dir + '/.config/msyncer')


class Syncer(object):
	def __init__(self, config):
		arg_parser = argparse.ArgumentParser(
			description="It sync's files between two nodes and bunch of other stuff"
		)
		self.config = config
		self.ip_address = config['phone']['ip_address']
		self.port = config['phone']['port']
		self.root_dir = config['phone']['root_dir']

		arg_parser.add_argument('command', help="currently available: UPLOAD, SYNC")
		args = arg_parser.parse_args(sys.argv[1:2])

		if not hasattr(self, args.command):
			print('Unrecognized command')
			arg_parser.print_usage()
			exit(1)
		# use dispatch pattern to invoke method with same name
		getattr(self, args.command)()


	def makeconfig(self):
		config_default = configparser.ConfigParser()

		parser = argparse.ArgumentParser()
		parser.add_argument("-t","--test", action="store_true", help="set testing config")
		parser.add_argument("-p","--production", action="store_true", help="set prod config")
		args = parser.parse_args(sys.argv[2:])

		if args.test:
			config_default['phone'] = {'ip_address': '127.0.0.1', 'port': '8080', 'root_dir': '/sync'}
		elif args.production:
			config_default['phone'] = {'ip_address': '10.0.0.6', 'port': '8080', 'root_dir': '/sync'}

		with open(config_path, 'w+') as configFile:
			config_default.write(configFile)
		exit(0)

	def upload(self):
		#upload file like app upload file santana.mp3 -> creates {ROOT_DIR}/santana.mp3
		#upload folder like app upload dir this    -> creates {ROOT_DIR}/this

		parser = argparse.ArgumentParser(
			description="Upload file to server"
		)
		parser.add_argument("-f","--file", nargs="+", type=str, help="Files to upload")
		parser.add_argument("-v","--verbose", action="store_true",help="Show files to upload and quit")
		args = parser.parse_args(sys.argv[2:])
		if args.verbose:
			print("------------------------------------")
			print(self.config.sections())
			print(self.ip_address)
			print(self.port)
			print(self.root_dir)
			print(args)
			print("------------------------------------")
			exit(0)

		options = {'webdav_hostname': "http://" + self.ip_address + ":" + self.port}
		client = wc.Client(options)

		if not client.check(self.root_dir):
			client.mkdir(self.root_dir)

		if args.file:
			for each in args.file:
				ap = os.path.abspath(each)
				print("uploading " + ap)
				if os.path.isdir(ap):
					if each == '.':
						client.upload(self.root_dir + os.path.dirname(each), ap)
						break
					client.upload(self.root_dir + "/" + each, ap)
				else:
					client.upload(self.root_dir + "/" + each, ap)

	def sync(self):

		parser = argparse.ArgumentParser(
			description="Sync local dir with server"
		)
		parser.add_argument("-f", "--folder", nargs=1, type=str, help="folder to sync")
		parser.add_argument("-v", "--verbose", action="store_true", help="Show files to upload and quit")
		args = parser.parse_args(sys.argv[2:])
		if args.verbose:
			print(args)
			exit(0)

		#todo fix
		if args.folder is None:
			parser.print_help()
			exit(0)

		options = {'webdav_hostname': "http://" + self.ip_address + ":" + self.port}
		client = wc.Client(options)

		if not client.check(self.root_dir):
			client.mkdir(self.root_dir)

		if not os.path.isdir(args.folder[0]):
			parser.print_usage()
			print("You should pass a folder")
			exit(1)

		client.push_force(self.root_dir, args.folder[0])


	def convert(self):
		print("converting")
# import webdav3.client as wc
# options = {
# 	'webdav_hostname': "http://" + config['phone']['ip_address'] + config['phone']['port']
# }
# print("connecting")
#
# client = wc.Client(options)
#
# client.upload(remote, local)

def make_default_config():
	config_default = configparser.ConfigParser()
	# config_default['phone'] = {'ip_address': '10.0.0.6', 'port': '8080', 'root_dir': '/sync'}
	config_default['phone'] = {'ip_address': '127.0.0.1', 'port': '8080', 'root_dir': '/sync'}

	with open(config_path, 'w+') as configFile:
		config_default.write(configFile)

def main():

	if Path.exists(config_path):
		pass
	else:
		make_default_config()

	config_parser = configparser.ConfigParser()

	config_parser.read(config_path)




	# arg_parser = argparse.ArgumentParser(
	# 	description="It sync's files between two nodes and bunch of other stuff"
	# )
	#
	# arg_parser.add_argument("-u", "--upload", type=str, nargs="+", help="upload this file to player")
	# # arg_parser.add_argument("-s")
	# # arg_parser.add_argument("-c", "--convert", type=str, nargs="+", help="converting stuff")
	# # arg_parser.add_argument("-s", "--sync", type=str, nargs="+", help="sync stuff")
	# args = arg_parser.parse_args()

	s = Syncer(config_parser)

	# print(args.upload)

	# upload(config_parser,what,where)

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
