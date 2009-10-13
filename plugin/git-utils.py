import vim, os

def git_changes(fname):
    try:
        f = os.popen("git --no-pager whatchanged --pretty=oneline " + fname)
        raw_changes = f.read()
    finally:
        f.close()

def Dtest():
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

print vim.command("foo")
