"""
This file contains unit tests for projfile.py
"""
import os
from unittest import TestCase
from bonsai_cli.projfile import ProjectFile, ProjectFileInvalidError

from click.testing import CliRunner


class TestProjectFile(TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_single_inkling(self):
        with self.runner.isolated_filesystem():
            open('one.ink', 'a').close()
            pf = ProjectFile()
            pf.files.add('./')

            self.assertEqual('one.ink', pf.inkling_file)
            self.assertTrue(os.path.isfile(pf.inkling_file))

    def test_inkling_specified(self):
        with self.runner.isolated_filesystem():
            open('one.ink', 'a').close()
            open('two.ink', 'a').close()
            pf = ProjectFile()
            pf.files.add('two.ink')
            self.assertEqual(pf.inkling_file, 'two.ink')

    def test_missing_inkling(self):
        with self.runner.isolated_filesystem():
            pf = ProjectFile()
            with self.assertRaises(ProjectFileInvalidError):
                pf.inkling_file

    def test_inkling_conflict(self):
        with self.runner.isolated_filesystem():
            open('one.ink', 'a').close()
            open('two.ink', 'a').close()
            pf = ProjectFile()
            pf.files.add('./')
            with self.assertRaises(ProjectFileInvalidError):
                pf.inkling_file

    def test_inkling_subdir(self):
        with self.runner.isolated_filesystem():
            os.mkdir('sub')
            os.mkdir('sub/sub2')
            open('sub/sub2/one.ink', 'a').close()
            pf = ProjectFile()
            pf.files.add('./')
            self.assertEqual(pf.inkling_file, 'sub/sub2/one.ink')
            self.assertTrue(os.path.isfile(pf.inkling_file))

    def test_outside_dir(self):
        with self.runner.isolated_filesystem():
            os.mkdir('sub')
            os.mkdir('sub/sub2')
            os.mkdir('sub/sub3')
            pf = ProjectFile('sub/sub3/test.bproj')
            pf.files.add('./')
            pf.files.add('something.ink')
            pf.files.add('../sub2/somethingelse.ink')
            pf.files.add('/tmp/athirdthing.ink')

            all_paths = list(pf._list_paths())
            self.assertEqual(1, len(all_paths))
            self.assertIn('something.ink', all_paths)

    def test_write_same_order_files(self):
        with self.runner.isolated_filesystem():
            pf1 = ProjectFile('test1.bproj')
            files1 = set([str(i) + '.py' for i in range(1, 100)])
            pf1.files.update(files1)
            pf1.save()
            with open(pf1.project_path, 'r') as f:
                s1 = f.read()

            pf2 = ProjectFile('test2.bproj')
            files2 = set([str(i) + '.py' for i in reversed(range(1, 100))])
            pf2.files.update(files2)
            pf2.save()
            with open(pf2.project_path, 'r') as f:
                s2 = f.read()

            self.assertEqual(s1, s2)

    def test_wildcard_does_not_include_git_files(self):
        with self.runner.isolated_filesystem():
            os.mkdir('.git')
            os.mkdir('subfolder')
            open('.gitignore', 'w').close()
            open('.git/one.txt', 'w').close()
            open('two.txt', 'w').close()
            open('subfolder/three.txt', 'w').close()

            pf = ProjectFile()
            pf.files.add('./')
            filenames = [os.path.basename(p) for p in pf._list_paths()]
            self.assertTrue('.gitignore' not in filenames)
            self.assertTrue('one.txt' not in filenames)
            self.assertTrue('two.txt' in filenames)
            self.assertTrue('three.txt' in filenames)
