from re import sub
from webdav3.urn import Urn
from webdav3.exceptions import *
import os

def listdir(directory):
    """Returns list of nested files and directories for local directory by path

    :param directory: absolute or relative path to local directory
    :return: list nested of file or directory names
    """
    file_names = list()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isdir(file_path):
            filename = "{filename}{separate}".format(filename=filename, separate=os.path.sep)
        file_names.append(filename)
    return file_names


def push(self, remote_directory, local_directory):

    #cut unused stuff
    def prune(src, exp):
        return [sub(exp, "", item) for item in src]
    #get a unified resource name
    urn = Urn(remote_directory, directory=True)

    if not self.is_dir(urn.path()):
        raise OptionNotValid(name="remote_path", value=remote_directory)

    if not os.path.isdir(local_directory):
        raise OptionNotValid(name="local_path", value=local_directory)

    if not os.path.exists(local_directory):
        raise LocalResourceNotFound(local_directory)

    #return paths without %20 escape characters
    paths = self.list(urn.path())

    expression = "{begin}{end}".format(begin="^", end=urn.path())
    remote_resource_names = prune(paths, expression)

    local_resources = listdir(local_directory);

    for local_resource_name in listdir(local_directory):

        local_path = os.path.join(local_directory, local_resource_name)
        remote_path = "{remote_directory}{resource_name}".format(remote_directory=urn.path(),
                                                                 resource_name=local_resource_name)

        # if os.path.isdir(local_path):
        #     if not self.check(remote_path=remote_path):
        #         self.mkdir(remote_path=remote_path)
        #     self.push(remote_directory=remote_path, local_directory=local_path)
        # else:
        #     if local_resource_name in remote_resource_names:
        #         continue
        #     self.upload_file(remote_path=remote_path, local_path=local_path)


print(listdir("/Users/kdm/test"))