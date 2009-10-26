from gitwrapper import *
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


def GitPreviousRevision():
    v = vim.Vim()
    git = GitUtils(v)

v = vim.Vim()

v.current.buffer.append("foo")
