import vim, os

class GitUtilsError(Exception):
    pass

class GitUtilsInputError(GitUtilsError):
    def __init__(self, message, git_message):
        self.message = message
        self.git_message = git_message

class GitWrapper:
    """Wrapper around git calls"""

    def _whatchanged(self, object):
        """runs git whatchanged to get a list of revisions for given git object"""
        try:
            f = os.popen("git --no-pager whatchanged --pretty=oneline " + object)
            raw_changes = f.read()
        finally:
            f.close()

        return raw_changes

    def _showfile(self, object):
        """runs git show to retrieve contents of given git object"""
        try:
            f = os.popen("git --no-pager show %s" % object)
            raw_changes = f.read()
        finally:
            f.close()

        return raw_changes

    def _getprefix(self):
        """gets the path of the current directory relative to the top-level 
        dir (aka the one with .git). Needed because some commands (git show rev:file) 
        in git require full path from the project's root directory"""
        try:
            f = os.popen("git rev-parse --show-prefix")
            prefix = f.read().strip()
        finally:
            f.close()
        return prefix

    def changed_revisions(self, fname):
        """returns the revisions in which the given file was changed"""
        raw_revisions = self._whatchanged(fname)
        if(raw_revisions.startswith("fatal:")):
            raise GitUtilsInputError("File does not exist", raw_revisions)
        else:
            revisions = raw_revisions.strip().split("\n")
            return [revisions[i].split(" ")[0] for i in range(0,len(revisions)) \
                    if i%2 == 0]

    def show_file(self, fname, revision):
        """returns the contents of the given file at the given revision"""
        contents = self._showfile("%s:%s" % (revision, self._getprefix() + fname) )
        if(contents.startswith("fatal:")):
            raise GitUtilsInputError("File at revision does not exist", contents)
        else:
            return contents
