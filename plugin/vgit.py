import os, vim

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

def _working_file():
    return vim.eval("@%")

def _fillGitRevisionBuffer(fname, rev):
    """Given a filename and a git revision fill a (possibly new) buffer
    with the contents of the file at that revision"""
    vim.command("silent keepjumps :open %s:%s" % (fname, rev))
    vim.command("setlocal buftype=nofile")
    vim.command("setlocal modifiable")

    contents = git.show_file(fname, rev)
    cb = vim.current.buffer
    for gline in contents.split("\n"):
        cb.append(gline)


def GitPreviousRevision():
    """Open a new readonly buffer with the current file's previous revision contents"""
    git = GitWrapper()
    fname = _working_file()

    if(fname.find(":") > 0): # we're already in one of the previous revision buffers
        (fname, current_rev) = fname.split(":")
        revisions = git.changed_revisions(fname)
        
        current_index = revisions.index(current_rev)
        if(current_index >= len(revisions) - 1):
            print "Earliest revision"
            return
        else:
            # so figure out what the current revision is and chose the next one
            rev = revisions[revisions.index(current_rev) + 1] 
    else:
        revisions = git.changed_revisions(fname)
        rev = revisions[1]

    _fillGitRevisionBuffer(fname, rev)


def GitNextRevision():
    """Fills the current git revision buffer with the next revion's content"""
    git = GitWrapper()
    fname = _working_file()

    if(fname.find(":") > 0):
        (fname, current_rev) = fname.split(":")
        revisions = git.changed_revisions(fname)
        
        current_index = revisions.index(current_rev)
        if(current_index == 0):
            print "Latest revision"
            return
        else:
            # so figure out what the current revision is and chose the next one
            rev = revisions[revisions.index(current_rev) - 1] 
    else:
        print "Not in git vevision buffer -- call GitPreviousRevision first"
        return

    _fillGitRevisionBuffer(fname, rev)
