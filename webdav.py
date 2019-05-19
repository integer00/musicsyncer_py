#
# uploading can be made by client.upload_sync("from","to")
# delete can be made by client.clean("what")
# syncing can be made by client.sync("from","to")
#

###options
##pull all shit from mobile to pc
##push all shit from pc to mobile
#

import hashlib
def file_as_bytes(file):
    with file:
        return file.read()

import webdav3.client as wc

options = {
 # 'webdav_hostname': "http://10.0.0.6:8080",
 'webdav_hostname': "http://127.0.0.1:8080",
 # 'webdav_login':    "asd",
 # 'webdav_password': "bkb",
 'verbose': True
}
# base = "/C7F1-1BF2"

client = wc.Client(options)

# client.mkdir("asd")

#
# client.mkdir("/testdav3")
# client.clean("/testdav3")
#ok


#client.upload_sync("/dav/test.mp3","/Users/kdm/testdav/test.mp3")

for each in client.list("/"):
 print(each)

##put to server (replace)
# client.upload_async("/testdav2","/Users/kdm/test/testdav")

##get from server
# client.download_sync("/testdav2","/Users/kdm/test/testdav")

##pull diff from server to local
# client.pull("/testdav2","/Users/kdm/test/testdav")

##push to server diffs (not working)

# client.pull("/testdav2","/Users/kdm/test/testdav")
#client.clean("/testdav2/sda 2.txt")

########download from server
# client.download_sync("/testdav2","/Users/kdm/test/sd")

########push to server
# client.push_force("/testdav2","/Users/kdm/test/sd")

# client.mkdir("sync")
#s

# client.upload("/sync/" ,"")
# print(client.list("/"))
# client.mkdir("sync")
# client.push_force("/sync","/Users/kdm/test/sync")
# client.push("/sync","/Users/kdm/test/sync")
# client.push_force("/Музыка","/garbage/Музыка")


# print(client.list("/C7F1-1BF2"))

# print(client.list("/testdav2/.DS_Store"))
# client.mkdir("/Музыка")


# print(client.info("/"));
# client.clean("/test")
# client.clean("/testdav")
# client.clean("/testdav2")
#print(client.list("/"))

#ok
# client.sync("/testdav2","/Users/kdm/test/testdav")
#ok


# client.push(remote_directory="this", local_directory="/Users/kdm/testdav")
# client.sync(remote_directory=".git", local_directory="/Users/kdm/testdav")
# client.clean(remote_path="testdav/sda.txt")