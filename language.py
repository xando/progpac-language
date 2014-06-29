import sys

import parser
import ast


def entry_point(argv):
    if len(argv) > 1:
        filename = argv[1]
        f = open(filename, 'r')
        code = f.read()
        f.close()

        ast_tree = parser.parse(code)
        print ast.compile(ast_tree)

    return 1


def target(driver, args):
    driver.exe_name = 'language'
    return entry_point, None



if __name__ == "__main__":
    entry_point(sys.argv)
