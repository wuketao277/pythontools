import unittest
from LogUtils import LogUtils

if __name__ == "__main__":
    unittest.main()


class LogUtilsTest(unittest.TestCase):
    def test_info(self):
        LogUtils.info('this is a info log')
