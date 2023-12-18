import unittest
import os
import re
from shell import eval_expression
from shell import convert


class TestShell(unittest.TestCase):
    def setUp(self):
        # Save the current working directory before each test
        self.original_cwd = os.getcwd()

    def tearDown(self):
        # Reset the working directory after each test
        os.chdir(self.original_cwd)

    # Test cases
    # note: unsafe applications are not tested
    def test_echo(self):
        stdout = eval_expression(convert("echo foo"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"foo"})

    def test_echo_with_glob(self):
        stdout = eval_expression(convert("echo *"))
        long_string = stdout.strip()
        result = set(long_string.split(" "))
        self.assertEqual(result, {'README.md', 'system_test', 'requirements.txt',
                                  'src', 'apps.svg', 'test_folder',
                                  'test', 'Dockerfile', 'tools',
                                  'sh', 'newfile.txt',
                                  '.devcontainer', '.vscode',
                                  '.gitignore', '.dockerignore', '.env', 'history.txt',
                                  '.flake8', '.github'})

    def test_echo_with_substitution(self):
        stdout = eval_expression(convert("echo foo bar"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"foo bar"})

    def test_echo_with_quotes(self):
        stdout = eval_expression(convert("echo 'foo bar'"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"foo bar"})

    def test_echo_with_backquotes(self):
        stdout = eval_expression(convert("echo `echo foo`"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"foo"})

    def test_echo_with_backquotes_and_quotes(self):
        stdout = eval_expression(convert("echo `echo 'foo bar'`"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"foo bar"})

    def test_echo_globbing(self):
        stdout = eval_expression(convert("echo *.txt"))
        long_string = stdout.strip()
        result = set(long_string.split(" "))
        self.assertEqual(result, {"history.txt", "newfile.txt", "requirements.txt"})

    def test_echo_globbing_dir(self):
        stdout = eval_expression(convert("echo test_folder/*.txt"))
        long_string = stdout.strip()
        result = set(long_string.split(" "))
        self.assertEqual(result, {"test_folder/longfile.txt",
                                  "test_folder/abc.txt",
                                  "test_folder/test1.txt",
                                  "test_folder/test2.txt"})

    def test_ls(self):
        stdout = eval_expression(convert("ls"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {'README.md',
                                  'system_test',
                                  'requirements.txt',
                                  'src',
                                  'apps.svg',
                                  'test_folder',
                                  'test',
                                  'Dockerfile',
                                  'tools',
                                  'sh',
                                  'newfile.txt',
                                  'history.txt'})

    def test_ls_dir(self):
        stdout = eval_expression(convert("ls test_folder"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"longfile.txt", "test.py",
                                  "test1.txt", "test2.txt", "abc.txt"})

    def test_ls_with_substitution(self):
        stdout = eval_expression(convert("ls `echo test_folder`"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"longfile.txt", "test.py",
                                  "test1.txt", "test2.txt", "abc.txt"})

    def test_ls_pipe(self):
        stdout = eval_expression(convert("echo 'test_folder' | ls"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"abc.txt", "longfile.txt",
                                  "test.py", "test1.txt", "test2.txt"})

    def test_cd_pwd(self):
        stdout = eval_expression(convert("cd src; pwd"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {os.path.join(self.original_cwd, "src")})

    def test_cd_pwd_with_substitution(self):
        stdout = eval_expression(convert("cd `echo src`; pwd"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {os.path.join(self.original_cwd, "src")})

    def test_cd_pwd_with_quotes(self):
        stdout = eval_expression(convert("cd 'src'; pwd"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {os.path.join(self.original_cwd, "src")})

    def test_cd_pwd_with_backquotes(self):
        stdout = eval_expression(convert("cd `echo src`; pwd"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {os.path.join(self.original_cwd, "src")})

    def test_cat_one_file(self):
        stdout = eval_expression(convert("cat test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "aaaa", "bbbb", "bbbb", "BBBB"})

    def test_cat_two_files(self):
        stdin = "cat test_folder/test1.txt test_folder/test2.txt"
        stdout = eval_expression(convert(stdin))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "aaaa", "bbbb", "bbbb", "BBBB", "aaaa",
                                  "bbbb", "aaaa", "bbbb", "aaaa", "asdf",
                                  "asdfasdf", "asdfasdf", "asdf", "asdf",
                                  "asdf", "fdfds"})

    def test_cat_two_files_with_substitution(self):
        stdin = "cat `echo test_folder/test1.txt` `echo test_folder/test2.txt`"
        stdout = eval_expression(convert(stdin))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "aaaa", "bbbb", "bbbb", "BBBB", "aaaa",
                                  "bbbb", "aaaa", "bbbb", "aaaa", "asdf",
                                  "asdfasdf", "asdfasdf", "asdf", "asdf",
                                  "asdf", "fdfds"})

    def test_cat_stdin(self):
        stdout = eval_expression(convert("cat < test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "aaaa", "bbbb", "bbbb", "BBBB"})

    def test_cat_stdin_with_substitution(self):
        stdout = eval_expression(convert("cat < `echo test_folder/test1.txt`"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "aaaa", "bbbb", "bbbb", "BBBB"})

    def test_cat_stdin_with_quotes(self):
        stdout = eval_expression(convert("cat < 'test_folder/test1.txt'"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "aaaa", "bbbb", "bbbb", "BBBB"})

    def test_cat_pipe(self):
        stdout = eval_expression(convert("echo 'test_folder/test1.txt' | cat"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"test_folder/test1.txt"})

    def test_head(self):
        stdout = eval_expression(convert("head test_folder/longfile.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {str(i) for i in range(1, 11)})

    def test_head_stdin(self):
        stdout = eval_expression(convert("head < test_folder/longfile.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {str(i) for i in range(1, 11)})

    def test_head_n3(self):
        stdout = eval_expression(convert("head -n 3 test_folder/longfile.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {str(i) for i in range(1, 4)})

    def test_head_n30_stdin(self):
        stdout = eval_expression(convert("head -n 30 < test_folder/longfile.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {str(i) for i in range(1, 31)})

    def test_head_with_substitution(self):
        stdout = eval_expression(convert("head `echo test_folder/longfile.txt`"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {str(i) for i in range(1, 11)})

    def test_head_with_quotes(self):
        stdout = eval_expression(convert("head 'test_folder/longfile.txt'"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {str(i) for i in range(1, 11)})

    def test_head_with_backquotes(self):
        stdout = eval_expression(convert("head `echo test_folder/longfile.txt`"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {str(i) for i in range(1, 11)})

    def test_head_pipe(self):
        stdin = "head `echo test_folder/longfile.txt` | head -n 3"
        stdout = eval_expression(convert(stdin))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {str(i) for i in range(1, 4)})

    def test_tail(self):
        stdout = eval_expression(convert("tail test_folder/longfile.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {str(i) for i in range(35, 45)})

    def test_tail_stdin(self):
        stdout = eval_expression(convert("tail < test_folder/longfile.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {str(i) for i in range(35, 45)})

    def test_tail_n3(self):
        stdout = eval_expression(convert("tail -n 3 test_folder/longfile.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {str(i) for i in range(42, 45)})

    def test_tail_n30_stdin(self):
        stdout = eval_expression(convert("tail -n 30 < test_folder/longfile.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {str(i) for i in range(15, 45)})

    def test_tail_pipe(self):
        stdin = "tail `echo test_folder/longfile.txt` | tail -n 3"
        stdout = eval_expression(convert(stdin))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {str(i) for i in range(42, 45)})

    def test_grep(self):
        stdout = eval_expression(convert("grep a test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"aaaa", "aaaa"})

    def test_grep_stdin(self):
        stdout = eval_expression(convert("grep a < test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"aaaa", "aaaa"})

    def test_grep_ignore_case(self):
        stdout = eval_expression(convert("grep -i a test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "aaaa", "aaaa"})

    def test_grep_no_matches(self):
        stdout = eval_expression(convert("grep c test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {''})

    def test_grep_regex(self):
        stdout = eval_expression(convert("grep 'a..a' test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"aaaa", "aaaa"})

    def test_grep_all(self):
        stdout = eval_expression(convert("grep '...' test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "aaaa", "bbbb", "bbbb", "BBBB"})

    def test_grep_all_stdin(self):
        stdout = eval_expression(convert("grep '...' < test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "aaaa", "bbbb", "bbbb", "BBBB"})

    def test_grep_all_with_substitution(self):
        stdout = eval_expression(convert("grep '...' `echo test_folder/test1.txt`"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "aaaa", "bbbb", "bbbb", "BBBB"})

    def test_grep_with_quotes(self):
        stdout = eval_expression(convert("grep 'a..a' 'test_folder/test1.txt'"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"aaaa", "aaaa"})

    def test_grep_with_backquotes(self):
        stdout = eval_expression(convert("grep 'a..a' `echo test_folder/test1.txt`"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"aaaa", "aaaa"})

    def test_find(self):
        stdout = eval_expression(convert("find -name test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"./test_folder/test1.txt"})

    def test_find_dir(self):
        stdout = eval_expression(convert("find test_folder -name test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"test_folder/test1.txt"})

    def test_find_dir_pattern(self):
        stdout = eval_expression(convert("find test_folder -name '*.txt'"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"test_folder/test1.txt", "test_folder/test2.txt",
                                  "test_folder/longfile.txt", "test_folder/abc.txt"})

    def test_find_dir_pattern_with_substitution(self):
        stdout = eval_expression(convert("find `echo test_folder` -name '*.txt'"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"test_folder/test1.txt", "test_folder/test2.txt",
                                  "test_folder/longfile.txt", "test_folder/abc.txt"})

    def test_sort(self):
        stdout = eval_expression(convert("sort test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "BBBB", "aaaa", "bbbb", "bbbb"})

    def test_sort_reverse(self):
        stdout = eval_expression(convert("sort -r test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"bbbb", "bbbb", "aaaa", "BBBB", "AAAA"})

    def test_sort_stdin(self):
        stdout = eval_expression(convert("sort < test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "BBBB", "aaaa", "bbbb", "bbbb"})

    def test_sort_stdin_reverse(self):
        stdout = eval_expression(convert("sort -r < test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"bbbb", "bbbb", "aaaa", "BBBB", "AAAA"})

    def test_uniq(self):
        stdout = eval_expression(convert("uniq test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "aaaa", "bbbb", "BBBB"})

    def test_uniq_ignore_case(self):
        stdout = eval_expression(convert("uniq -i test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "bbbb"})

    def test_uniq_stdin(self):
        stdout = eval_expression(convert("uniq < test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "aaaa", "bbbb", "BBBB"})

    def test_uniq_stdin_ignore_case(self):
        stdout = eval_expression(convert("uniq -i < test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "bbbb"})

    def test_cut(self):
        stdout = eval_expression(convert("cut -b 1 test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"A", "a", "b", "b", "B"})

    def test_cut_interval(self):
        stdout = eval_expression(convert("cut -b 1-2 test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AA", "aa", "bb", "bb", "BB"})

    def test_cut_open_interval(self):
        stdout = eval_expression(convert("cut -b 1- test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "aaaa", "bbbb", "bbbb", "BBBB"})

    def test_cut_overlapping(self):
        stdout = eval_expression(convert("cut -b 1-2,2-3 test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA", "aaa", "bbb", "bbb", "BBB"})

    def test_cut_union(self):
        stdout = eval_expression(convert("cut -b 1-2,3-4 test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "aaaa", "bbbb", "bbbb", "BBBB"})

    def test_cut_no_interval(self):
        stdout = eval_expression(convert("cut -b -1,3- test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA", "aaa", "bbb", "bbb", "BBB"})

    def test_cut_stdin(self):
        stdout = eval_expression(convert("cut -b 1-2 < test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AA", "aa", "bb", "bb", "BB"})

    def test_cut_substitution(self):
        stdout = eval_expression(convert("cut -b 1-2 `echo test_folder/test1.txt`"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AA", "aa", "bb", "bb", "BB"})

    def test_cut_quotes(self):
        stdout = eval_expression(convert("cut -b 1-2 'test_folder/test1.txt'"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AA", "aa", "bb", "bb", "BB"})

    def test_pipe_ls_grep(self):
        stdout = eval_expression(convert("ls | grep test"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"test_folder", "test", "system_test"})

    def test_pipe_ls_grep_with_substitution(self):
        stdout = eval_expression(convert("ls | grep `echo test`"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"test_folder", "test", "system_test"})

    def test_pipe_sort_uniq(self):
        stdout = eval_expression(convert("sort test_folder/test1.txt | uniq"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "BBBB", "aaaa", "bbbb"})

    def test_pipe_chain_ls_grep_sort_uniq(self):
        stdout = eval_expression(convert("ls | grep test | sort | uniq"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"test", "test_folder", "system_test"})

    def test_wc(self):
        stdout = eval_expression(convert("wc test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"5 5 25"})

    def test_wc_stdin(self):
        stdout = eval_expression(convert("wc < test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"5 5 25"})

    def test_wc_m(self):
        stdout = eval_expression(convert("wc -m test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"25"})

    def test_wc_l(self):
        stdout = eval_expression(convert("wc -l test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"5"})

    def test_wc_w(self):
        stdout = eval_expression(convert("wc -w test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"5"})

    def test_sed(self):
        stdout = eval_expression(convert("sed 's/a/b/' test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "baaa", "bbbb", "bbbb", "BBBB"})

    def test_sed_stdin(self):
        stdout = eval_expression(convert("sed 's/a/b/' < test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "baaa", "bbbb", "bbbb", "BBBB"})

    def test_sed_separator(self):
        stdout = eval_expression(convert("sed 's|a|b|' test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "baaa", "bbbb", "bbbb", "BBBB"})

    def test_sed_g(self):
        stdout = eval_expression(convert("sed 's/a/b/g' test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "bbbb", "bbbb", "bbbb", "BBBB"})

    def test_sed_re(self):
        stdout = eval_expression(convert("sed 's/a../b/' test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "ba", "bbbb", "bbbb", "BBBB"})

    def test_sed_pipe(self):
        stdout = eval_expression(convert("echo 'AAAA' | sed 's/A/B/'"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"BAAA"})

    # test cases below are to catch errors
    def test_error_cat(self):
        with self.assertRaises(FileNotFoundError):
            eval_expression(convert("cat test_folder/unknown.txt"))

    def test_error_cd_no_args(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("cd"))

    def test_error_cd_too_many_args(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("cd src src"))

    def test_error_cd_no_dir(self):
        with self.assertRaises(OSError):
            eval_expression(convert("cd unknown"))

    def test_error_cut_no_args(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("cut"))

    def test_error_cut_too_few_args_with_pipe(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("echo aaa | cut"))

    def test_error_cut_wrong_option(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("cut -a 1 test_folder/test1.txt"))

    def test_error_cut_no_file(self):
        with self.assertRaises(FileNotFoundError):
            eval_expression(convert("cut -b 1 test_folder/unknown.txt"))

    def test_error_find_no_args(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("find"))

    def test_error_find_no_path(self):
        with self.assertRaises(FileNotFoundError):
            eval_expression(convert("find unknown -name unknown.txt"))

    def test_error_no_name(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("find test_folder"))

    def test_error_grep_no_args(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("grep"))

    def test_error_grep_no_file(self):
        with self.assertRaises(FileNotFoundError):
            eval_expression(convert("grep a test_folder/unknown.txt"))

    def test_error_head_wrong_args(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("head 6 test_folder/test1.txt"))

    def test_error_head_wrong_option(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("head -a 10 test_folder/test1.txt"))

    def test_error_head_args_2_not_int(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("head -n a test_folder/test1.txt"))

    def test_error_head_args_2_not_int_with_pipe(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("echo aaa | head -n a"))

    def test_error_head_no_file(self):
        with self.assertRaises(FileNotFoundError):
            eval_expression(convert("head test_folder/unknown.txt"))

    def test_error_ls_wrong_args(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("ls wow test_folder"))

    def test_error_ls_no_dir(self):
        with self.assertRaises(FileNotFoundError):
            eval_expression(convert("ls unknown"))

    def test_error_pwd_too_many_args(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("pwd src"))

    def test_error_sed_wrong_args(self):
        with self.assertRaises(ValueError):
            inp = "sed 's/a/b/' test_folder/test1.txt test_folder/test2.txt"
            eval_expression(convert(inp))

    def test_error_sed_wrong_separator(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("sed 's_a_b_' test_folder/test1.txt"))

    def test_error_sed_not_s(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("sed 'a/b/' test_folder/test1.txt"))

    def test_error_sed_g(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("sed 's/g/' test_folder/test1.txt"))

    def test_error_sort_wrong_args(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("sort wow wow wow"))

    def test_error_sort_no_file(self):
        with self.assertRaises(FileNotFoundError):
            eval_expression(convert("sort test_folder/unknown.txt"))

    def test_error_tail_wrong_args(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("tail 6 test_folder/test1.txt"))

    def test_error_tail_wrong_option(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("tail -a 10 test_folder/test1.txt"))

    def test_error_tail_args_2_not_int(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("tail -n a test_folder/test1.txt"))

    def test_error_tail_args_2_not_int_with_pipe(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("echo aaa | tail -n a"))

    def test_error_tail_no_file(self):
        with self.assertRaises(FileNotFoundError):
            eval_expression(convert("tail test_folder/unknown.txt"))

    def test_error_uniq_wrong_args(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("uniq wow wow 4 test_folder/test1.txt"))

    def test_error_uniq_no_file(self):
        with self.assertRaises(FileNotFoundError):
            eval_expression(convert("uniq test_folder/unknown.txt"))

    def test_error_wc_wrong_args(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("wc"))

    def test_error_wc_no_file(self):
        with self.assertRaises(FileNotFoundError):
            eval_expression(convert("wc test_folder/unknown.txt"))

    # test cases below are for unsafe applications
    # Not sure what this is supposed to do
    def test_unsafe_ls(self):
        stdout = eval_expression(convert("_ls; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {'README.md',
                                  'system_test',
                                  'requirements.txt',
                                  'src',
                                  'apps.svg',
                                  'test_folder',
                                  'test',
                                  'Dockerfile',
                                  'tools',
                                  'sh',
                                  'newfile.txt',
                                  'history.txt',
                                  'AAA'})

    def test_unsafe_ls_dir(self):
        stdout = eval_expression(convert("_ls test_folder unknown; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_unsafe_ls_pipe(self):
        stdout = eval_expression(convert("echo 'unknown' | _ls; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_unsafe_cat(self):
        stdin = "_cat test_folder/unknown.txt test_folder/yo.txt; echo AAA"
        stdout = eval_expression(convert(stdin))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_unsafe_cat_two_files(self):
        stdin = "_cat test_folder/test1.txt test_folder/test2.txt"
        stdout = eval_expression(convert(stdin))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "aaaa", "bbbb", "bbbb", "BBBB", "aaaa",
                                  "bbbb", "aaaa", "bbbb", "aaaa", "asdf", "asdfasdf",
                                  "asdfasdf", "asdf", "asdf", "asdf", "fdfds"})

    def test_unsafe_cat_stdin(self):
        stdout = eval_expression(convert("_cat < test_folder/unknown.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_unsafe_cat_pipe(self):
        stdin = "echo 'test_folder/unknown.txt' | _cat; echo AAA"
        stdout = eval_expression(convert(stdin))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"test_folder/unknown.txt", "AAA"})

    def test_unsafe_cd(self):
        stdout = eval_expression(convert("_cd unknown; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_unsafe_cd_pwd(self):
        stdout = eval_expression(convert("cd src; _pwd"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {os.path.join(self.original_cwd, "src")})

    def test_unsafe_cut(self):
        stdout = eval_expression(convert("_cut -b 1 test_folder/unknown.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_unsafe_cut_interval(self):
        stdout = eval_expression(convert("_cut -b 1-2 test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AA", "aa", "bb", "bb", "BB"})

    def test_unsafe_cut_open_interval(self):
        stdout = eval_expression(convert("_cut -b 1- test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "aaaa", "bbbb", "bbbb", "BBBB"})

    def test_unsafe_cut_overlapping(self):
        stdout = eval_expression(convert("_cut -b 1-2,2-3 test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA", "aaa", "bbb", "bbb", "BBB"})

    def test_unsafe_cut_union(self):
        stdout = eval_expression(convert("_cut -b 1-2,3-4 test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "aaaa", "bbbb", "bbbb", "BBBB"})

    def test_unsafe_cut_no_interval(self):
        stdout = eval_expression(convert("_cut -b -1,3- test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA", "aaa", "bbb", "bbb", "BBB"})

    def test_unsafe_echo(self):
        stdout = eval_expression(convert("_echo AAA; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA", "AAA"})

    def test_unsafe_echo_with_glob(self):
        stdout = eval_expression(convert("_echo *; echo AAA"))
        long_string = stdout.strip()
        first_res = re.split("\n| ", long_string)
        result = set(first_res)
        self.assertEqual(result, {"README.md", "system_test", "requirements.txt",
                                  "apps.svg", "test_folder", "test",
                                  "Dockerfile", "tools", "sh",
                                  "newfile.txt",  ".devcontainer",
                                  ".vscode", ".gitignore", ".dockerignore",
                                  ".env", "history.txt", ".flake8", "src",
                                  ".github", "AAA"})

    def test_unsafe_find(self):
        stdout = eval_expression(convert("_find unknown; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_unsafe_find_dir(self):
        stdout = eval_expression(convert("_find test_folder unknown; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_unsafe_find_dir_pattern(self):
        stdout = eval_expression(convert("_find test_folder -name unknown.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_unsafe_grep(self):
        stdout = eval_expression(convert("_grep a test_folder/unknown.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_unsafe_grep_ignore_case(self):
        stdout = eval_expression(convert("_grep -i a test_folder/unknown.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_unsafe_grep_no_matches(self):
        stdout = eval_expression(convert("_grep c test_folder/test1.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_unsafe_grep_regex(self):
        stdout = eval_expression(convert("_grep 'a..a' test_folder/test1.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"aaaa", "AAA"})

    def test_unsafe_grep_all(self):
        stdout = eval_expression(convert("_grep '...' test_folder/test1.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "aaaa", "bbbb", "bbbb", "BBBB", "AAA"})

    def test_unsafe_grep_pipe(self):
        stdin = "echo 'test_folder/test1.txt' | _grep a; echo AAA"
        stdout = eval_expression(convert(stdin))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_unsafe_head(self):
        stdout = eval_expression(convert("_head test_folder/unknown.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_unsafe_head_n3(self):
        stdout = eval_expression(convert("_head -n 3 test_folder/longfile.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {str(i) for i in range(1, 4)})

    def test_unsafe_head_n30_stdin(self):
        stdout = eval_expression(convert("_head -n 30 < test_folder/longfile.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {str(i) for i in range(1, 31)})

    def test_unsafe_head_pipe(self):
        stdout = eval_expression(convert("echo 'test_folder/longfile.txt' | _head"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"test_folder/longfile.txt"})

    def test_unsafe_tail(self):
        stdout = eval_expression(convert("_tail test_folder/unknown.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_unsafe_tail_n3(self):
        stdout = eval_expression(convert("_tail -n 3 test_folder/longfile.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {str(i) for i in range(42, 45)})

    def test_unsafe_tail_n30_stdin(self):
        stdout = eval_expression(convert("_tail -n 30 < test_folder/longfile.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {str(i) for i in range(15, 45)})

    def test_unsafe_tail_pipe(self):
        stdout = eval_expression(convert("echo 'test_folder/longfile.txt' | _tail"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"test_folder/longfile.txt"})

    def test_unsafe_sort(self):
        stdout = eval_expression(convert("_sort test_folder/unknown.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_unsafe_sort_reverse(self):
        stdout = eval_expression(convert("_sort -r test_folder/test1.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"bbbb", "bbbb", "aaaa", "BBBB", "AAAA", "AAA"})

    def test_unsafe_uniq(self):
        stdout = eval_expression(convert("_uniq test_folder/unknown.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_unsafe_uniq_ignore_case(self):
        stdout = eval_expression(convert("_uniq -i test_folder/test1.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "bbbb", "AAA"})

    def test_unsafe_wc(self):
        stdout = eval_expression(convert("_wc test_folder/unknown.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_unsafe_wc_stdin(self):
        stdout = eval_expression(convert("_wc < test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"5 5 25"})

    def test_unsafe_wc_m(self):
        stdout = eval_expression(convert("_wc -m test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"25"})

    def test_unsafe_wc_l(self):
        stdout = eval_expression(convert("_wc -l test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"5"})

    def test_unsafe_wc_w(self):
        stdout = eval_expression(convert("_wc -w test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"5"})

    def test_unsafe_sed(self):
        stdin = "_sed 's/a/b/' test_folder/unknown.txt; echo AAA"
        stdout = eval_expression(convert(stdin))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_unsafe_sed_stdin(self):
        stdout = eval_expression(convert("_sed 's/a/b/' < test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "baaa", "bbbb", "bbbb", "BBBB"})

    def test_unsafe_sed_separator(self):
        stdout = eval_expression(convert("_sed 's|a|b|' test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "baaa", "bbbb", "bbbb", "BBBB"})

    def test_unsafe_sed_g(self):
        stdout = eval_expression(convert("_sed 's/a/b/g' test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "bbbb", "bbbb", "bbbb", "BBBB"})

    def test_unsafe_sed_re(self):
        stdout = eval_expression(convert("_sed 's/a../b/' test_folder/test1.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAAA", "ba", "bbbb", "bbbb", "BBBB"})

    def test_unsafe_sed_pipe(self):
        stdout = eval_expression(convert("echo 'AAAA' | _sed 's/A/B/'"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"BAAA"})

    ''' test cases below are for unsafe applications errors '''
    def test_error_unsafe_cat(self):
        stdout = eval_expression(convert("_cat test_folder/unknown.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_cd(self):
        stdout = eval_expression(convert("_cd unknown wow; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_cut_no_args(self):
        stdout = eval_expression(convert("_cut; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_cut_wrong_option(self):
        stdout = eval_expression(convert("_cut -a 1 test_folder/test1.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_find_no_path(self):
        stdout = eval_expression(convert("_find unknown -name unknown.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_find_no_name(self):
        stdout = eval_expression(convert("_find test_folder; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_grep_no_args(self):
        stdout = eval_expression(convert("_grep; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_grep_no_file(self):
        stdout = eval_expression(convert("_grep a test_folder/unknown.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_head_wrong_args(self):
        stdout = eval_expression(convert("_head 6 test_folder/test1.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_head_wrong_option(self):
        stdout = eval_expression(convert("_head -a 10 test_folder/test1.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_head_args_2_not_int(self):
        stdout = eval_expression(convert("_head -n a test_folder/test1.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_head_no_file(self):
        stdout = eval_expression(convert("_head test_folder/unknown.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_ls_wrong_args(self):
        stdout = eval_expression(convert("_ls wow test_folder; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_ls_no_dir(self):
        stdout = eval_expression(convert("_ls unknown; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_pwd_too_many_args(self):
        stdout = eval_expression(convert("_pwd src; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_sed_wrong_args(self):
        stdin = "_sed 's/a/b/' test_folder/test1.txt test_folder/test2.txt; echo AAA"
        stdout = eval_expression(convert(stdin))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_sed_wrong_separator(self):
        stdout = eval_expression(convert("_sed 's_a_b_' test_folder/test1.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_sed_not_s(self):
        stdout = eval_expression(convert("_sed 'a/b/' test_folder/test1.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_sed_g(self):
        stdout = eval_expression(convert("_sed 's/g/' test_folder/test1.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_sort_wrong_args(self):
        stdout = eval_expression(convert("_sort wow wow wow; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_sort_no_file(self):
        stdout = eval_expression(convert("_sort test_folder/unknown.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_tail_wrong_args(self):
        stdout = eval_expression(convert("_tail 6 test_folder/test1.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_tail_wrong_option(self):
        stdout = eval_expression(convert("_tail -a 10 test_folder/test1.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_tail_args_2_not_int(self):
        stdout = eval_expression(convert("_tail -n a test_folder/test1.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_tail_no_file(self):
        stdout = eval_expression(convert("_tail test_folder/unknown.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_uniq_wrong_args(self):
        stdin = "_uniq wow wow 4 test_folder/test1.txt; echo AAA"
        stdout = eval_expression(convert(stdin))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_uniq_no_file(self):
        stdout = eval_expression(convert("_uniq test_folder/unknown.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_wc_wrong_args(self):
        stdout = eval_expression(convert("_wc; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_error_unsafe_wc_no_file(self):
        stdout = eval_expression(convert("_wc test_folder/unknown.txt; echo AAA"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"AAA"})

    def test_parser_syntax_error(self):
        with self.assertRaises(SyntaxError):
            eval_expression(convert(";;"))

    def test_unknown_command_error(self):
        with self.assertRaises(SyntaxError):
            eval_expression(convert("dwdwadawd"))

    def test_cat_long(self):
        stdout = eval_expression(convert("cat test_folder/longfile.txt"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {str(i) for i in range(1, 45)})

    def test_splitting(self):
        stdout = eval_expression(convert('echo a"b"c'))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"abc"})

    def test_output_redirection(self):
        eval_expression(convert('echo aaa > test_folder/abc.txt'))
        long_string = eval_expression(convert('cat test_folder/abc.txt')).strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"aaa"})

    def test_single_cat_substitution(self):
        stdout = eval_expression(convert("cat `find test_folder -name 'longfile.txt'`"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {str(i) for i in range(1, 45)})

    def test_cat_multiple_files_substitution(self):
        stdout = eval_expression(convert("cat `find test_folder -name 'test*.txt'`"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {'AAAA',
                                  'aaaa',
                                  'bbbb',
                                  'BBBB',
                                  'asdfasdf',
                                  'asdf',
                                  'fdfds'})

    def test_find_pattern_error(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("find src -name"))

    def test_sed_invalid(self):
        with self.assertRaises(ValueError):
            eval_expression(convert("sed 'sbg' test_folder/test1.txt"))

    def test_multiple_pipes(self):
        stdout = eval_expression(convert("echo AAA | sed 's/A/C/' | sed 's/A/B/'"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"CBA"})

    def test_redirection_infront(self):
        stdout = eval_expression(convert("< test_folder/abc.txt cat"))
        long_string = stdout.strip()
        result = set(long_string.split("\n"))
        self.assertEqual(result, {"aaa"})


if __name__ == "__main__":
    unittest.main()
