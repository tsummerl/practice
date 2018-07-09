
#
# Every week he searches through the Sunday newspaper to find a string of digits that might be potential lottery picks.
# But this week the newspaper has moved to a new electronic format, and instead of a comfortable pile of papers,
# Uncle Morty receives a text file with the stories.
#
# Help your Uncle find his lotto picks. Given a large series of number strings, return each that might be suitable
# for a lottery ticket pick. Note that a valid lottery ticket must have 7 unique numbers between 1 and 59, digits must
# be used in order, and every digit must be used exactly once.
#
# For example, given the following strings:
#
#
# Your function should return:
#
# 4938532894754 -> 49 38 53 28 9 47 54
# 1234567 -> 1 2 3 4 5 6 7
# README instructions:
#
#
# To Run: use the command python lottery.py [string values]
# example: python lottery.py "1234567" "12345678"
# The program will print out 1234567 and 12345678 since they are both valid strings
#
# Thought process: I looked at the problem as a sliding window permutation problem. Depending on the length
# of the string I would know how many numbers were single digit numbers and how many numbers were double digit
# numbers. For example: 1234567 has seven single digit numbers and no double digit numbers while 12345678 has six
# single digit numbers and 1 double digit number.
#
# Knowing how many single and double digit numbers a string has I created a recursive solution where we iterate through
# the possible solutions by choosing to make a number from a single digit or a double digit and then continue to
# recurse. To optimize my solution I do a check to make sure that the number is valid before recursing again.
# If it isn't valid we eliminate all possible values resulting from the number. Also if we find a solution we return
# right away.  To keep track of numbers used, I'm using a set, for fast lookup and insertion O(1).  The worst case times
# are times where the the test fails nearing the end of the solution. Since the algorithm is depth first and was unable
# to cut out paths
# or prune the tree with invalid digits it will attempt to continue finding values. The algorithm is also worse when
# the number of single digit and double digits are closer in value, this results in the most possible combinations.



import sys
import ast
import unittest

# CONSTANTS

MAX_NUM = 59
MIN_NUM = 1
MAX_DIGITS = 7


class TestLottery(unittest.TestCase):

    def test_empty(self):
        self.assertFalse(Lottery.is_lottery(''))
        self.assertFalse(Lottery.is_lottery(None))

    def test_invalid(self):
        self.assertFalse(Lottery.is_lottery('123.4567'))
        self.assertFalse(Lottery.is_lottery('-12434567'))
        self.assertFalse(Lottery.is_lottery('abcbebdhighehg'))

    def test_short(self):
        self.assertFalse(Lottery.is_lottery('12345'))
        self.assertFalse(Lottery.is_lottery('1'))

    def test_long(self):
        self.assertFalse(Lottery.is_lottery('1234567891235465488457584594594'))
        self.assertFalse(Lottery.is_lottery('128394845060348128394845060348'))

    def test_leading_zero(self):
        self.assertFalse(Lottery.is_lottery('0123456789'))

    def test_repeat(self):
        self.assertFalse(Lottery.is_lottery('123459999'))
        self.assertFalse(Lottery.is_lottery('911989323'))

    def test_valid(self):
        self.assertTrue(Lottery.is_lottery('1234567'))
        self.assertTrue(Lottery.is_lottery('12345678'))
        self.assertTrue(Lottery.is_lottery('123456789'))
        self.assertTrue(Lottery.is_lottery('12345678911'))
        self.assertTrue(Lottery.is_lottery('938592884754'))
        self.assertTrue(Lottery.is_lottery('4938532894754'))


class Lottery:
    @staticmethod
    def is_lottery(str_nums):
        if str_nums is None:
            return False
        length = len(str_nums)
        if length < 7 or length > 14:
            return False
        if not str_nums.isdigit():
            return False
        double_digit = length - MAX_DIGITS
        single_digit = MAX_DIGITS - double_digit

        is_lottery = Lottery.create_digit(single_digit, double_digit, set(), str_nums)
        if is_lottery is True:
            return True
        else:
            return False

    @staticmethod
    def create_digit(single, double, num_set, str):

        print "single: {} double: {} arr: {} str: {}".format(single, double, num_set, str)
        is_lottery = False
        if len(str) == 0 and single == 0 and double == 0:
            print num_set
            is_lottery = True
        else:
            if double > 0:
                new_set = num_set.copy()
                if str[0] != '0':
                    temp_num = int(str[0:2])
                    if temp_num > 0 and temp_num <= MAX_NUM and temp_num not in new_set:
                        new_set.add(temp_num)
                        is_lottery = is_lottery or Lottery.create_digit(single, double-1, new_set, str[2:])
            if single > 0 and is_lottery is False:
                new_set = num_set.copy()
                temp_num = int(str[0])
                if temp_num > 0 and temp_num <= MAX_NUM and temp_num not in new_set:
                    new_set.add(temp_num)
                    is_lottery = is_lottery or Lottery.create_digit(single-1, double, new_set, str[1:])
        return is_lottery


def main(argv):
    arr = ast.literal_eval(str(argv[1:]))
    # print arr
    for val in arr:
        if Lottery.is_lottery(val):
            print val


if __name__ == "__main__":
    unittest.main()
    main(sys.argv)
