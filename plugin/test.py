import vim, unittest
from vgit import *
from mock import Mock

class GitUtilsTest(unittest.TestCase):
    def setUp(self):
        v = vim.Vim()
        self.git = GitUtils(v)


class GitWrapperTest(unittest.TestCase):
    def setUp(self):
        self.git = GitWrapper()

    def test_changes_for_non_file(self):
        """make sure fake files throw exceptions"""
        self.git._whatchanged = Mock(return_value="fatal: ambiguous argument...")
        self.assertRaises(GitUtilsInputError, self.git.changed_revisions, "FILE_NOT_REAL")
        self.git._whatchanged.assert_called_with("FILE_NOT_REAL")


    def test_changes_for_real_file(self):
        """find list of changes for "real" files"""
        mock_return = """513134261962e58f90a2a88cda2738d1da92cb6d making classes in prep for testing
:100644 100644 cbf55a2... 5dd6776... M  plugin/vim.py
48ecba5153ca0b4a44659435a61fa6810815e763 initial import
:000000 100644 0000000... cbf55a2... A  plugin/vim.py")"""

        self.git._whatchanged = Mock(return_value=mock_return)

        changed = self.git.changed_revisions("real_file.py")
        self.git._whatchanged.assert_called_with("real_file.py")
        self.assertEquals(len(changed),2)
        self.assertEquals(changed[0],"513134261962e58f90a2a88cda2738d1da92cb6d")

    def test_show_file_dne(self):
        """make sure fake files raise exceptions"""
        self.git._showfile = Mock(return_value="fatal: ambiguous argument...")
        self.assertRaises(GitUtilsError, self.git.show_file, "FILE_NOT_REAL", "123")
        self.git._showfile.assert_called_with("123:FILE_NOT_REAL")

    def test_show_file_real(self):
        """now display a real file at some given revisions"""
        mock_return = "here's some example text"
        self.git._showfile = Mock(return_value=mock_return)
        file = self.git.show_file("real.txt", "123")

        self.assertEquals(file, mock_return)
        self.git._showfile.assert_called_with("123:real.txt")


if __name__ == "__main__":
    unittest.main()
