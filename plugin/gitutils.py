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


    def changed_revisions(self, fname):
        """returns the revisions in which the given file was changed"""
        raw_revisions = self._whatchanged(fname)
        if(raw_revisions.startswith("fatal:")):
            raise GitUtilsInputError("File does not exist", raw_revisions)
        else:
            revisions = raw_revisions.split("\n")
            return [revisions[i].split(" ")[0] for i in range(0,len(revisions)) \
                    if i%2 == 0]

    def show_file(self, fname, revision):
        """returns the contents of the given file at the given revision"""
        contents = self._showfile("%s:%s" % (revision, fname) )
        if(contents.startswith("fatal:")):
            raise GitUtilsInputError("File at revision does not exist", contents)
        else:
            return contents

class GitUtils:
    """Vim utility methods related to git"""
    def __init__(self, vi):
        self.vi = vi

    def test():
        name = vim.eval("@%")

        vim.command("silent keepjumps :open foo")
        vim.command("setlocal bufhidden=delete")
        vim.command("setlocal buftype=nofile")
        vim.command("setlocal modifiable")
        vim.command("setlocal noswapfile")
        vim.command("setlocal nowrap")

        output = os.popen("git --no-pager show HEAD:" + name).read()
        cb = vim.current.buffer
        for gline in output.split("\n"):
            cb.append(gline)


def Dtest():
    v = vim.Vim()
    git = GitUtils(v)

v = vim.Vim()

v.current.buffer.append("foo")
