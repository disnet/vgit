import vim, os

class GitUtils:
    """Wrapper around git calls"""
    def __init__(self, vi):
        self.vi = vi

    def _changes(self, fname):
        try:
            f = os.popen("git --no-pager whatchanged --pretty=oneline " + fname)
            raw_changes = f.read()
        finally:
            f.close()

    def foo(self):
        return True

    def test():
        name = vim.eval("@%")

        changes = os.popen("git --no-pager whatchanged --pretty=oneline " + name).read()

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
