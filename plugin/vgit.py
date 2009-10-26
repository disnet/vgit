from vim import eval, command
from gitwrapper import *

class GitUtils:
    """Vim utility methods related to git"""
    def working_file():
        return eval("@%")

    def test():
        name = self.working_file()

        command("silent keepjumps :open foo")
        command("setlocal bufhidden=delete")
        command("setlocal buftype=nofile")
        command("setlocal modifiable")
        command("setlocal noswapfile")
        command("setlocal nowrap")

        output = os.popen("git --no-pager show HEAD:" + name).read()
        cb = vim.current.buffer
        for gline in output.split("\n"):
            cb.append(gline)


def GitPreviousRevision():
    pass

