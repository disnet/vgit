import vim, os

class GitWrapper:
    """Wrapper around git calls"""

    def _whatchanged(self, fname):
        try:
            f = os.popen("git --no-pager whatchanged --pretty=oneline " + fname)
            raw_changes = f.read()
        finally:
            f.close()

    def changed_revisions(self, fname):
        """returns the revisions in which the given file was changed"""
        raw_revisions = self._whatchanged(fname)
        if(raw_revisions.startswith("fatal:")):
            return []
        else:
            revisions = raw_revisions.split("\n")
            return [revisions[i].split(" ")[0] for i in range(0,len(revisions)) \
                    if i%2 == 0]

    def show_file(self, fname, revision):
        return ""


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
