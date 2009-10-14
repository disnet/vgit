import vim, unittest
from gitutils import *
from mock import Mock

class GitUtilsTest(unittest.TestCase):
    def setUp(self):
        v = vim.Vim()
        self.git = GitUtils(v)

class GitWrapperTest(unittest.TestCase):
    def setUp(self):
        self.git = GitWrapper()

    def test_changes_for_non_file(self):
        self.git._whatchanged = Mock(return_value="fatal: ambiguous argument...")

        changed = self.git.changed_revisions("FILE_NOT_REAL")
        self.assertEquals(len(changed), 0)
        self.git._whatchanged.assert_called_with("FILE_NOT_REAL")


    def test_changes_for_real_file(self):
        self.git._whatchanged = Mock(return_value="513134261962e58f90a2a88cda2738d1da92cb6d making classes in prep for testing\n:100644 100644 cbf55a2... 5dd6776... M  plugin/vim.py\n48ecba5153ca0b4a44659435a61fa6810815e763 initial import\n:000000 100644 0000000... cbf55a2... A  plugin/vim.py")

        changed = self.git.changed_revisions("real_file.py")
        self.git._whatchanged.assert_called_with("real_file.py")
        self.assertEquals(len(changed),2)
        self.assertEquals(changed[0],"513134261962e58f90a2a88cda2738d1da92cb6d")

    def test_show_file_dne(self):
        self.git._showfile = Mock(return_value="fatal: ambiguous argument...")

        file = self.git.show_file("FILE_NOT_REAL", "123")

        self.assertEqual(len(file), 0)
        self.git._showfile.assert_called_with("123:FILE_NOT_REAL")




if __name__ == "__main__":
    unittest.main()
