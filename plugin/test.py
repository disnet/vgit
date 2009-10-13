import gitutils, vim
import unittest

class GitUtilsTest(unittest.TestCase):

    def setUp(self):
        v = vim.Vim()
        self.git = gitutils.GitUtils(v)

    def testSimple(self):
        self.assert_(True)

    def testFoo(self):
        self.assert_(self.git.foo())




if __name__ == "__main__":
    unittest.main()
