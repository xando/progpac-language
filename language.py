import sys

import parser
import ast


def entry_point(argv):
    if len(argv) > 1:
        filename = argv[1]
        f = open(filename, 'r')
        source = f.read()
        f.close()

        try:
            ast_tree = parser.parse(source)
            # print ast_tree
            code = ast.compile(ast_tree, source)
            print code
        except ValueError as e:
            print e.message

        sys.exit()

    return 1


def target(driver, args):
    driver.exe_name = 'language'
    return entry_point, None



if __name__ == "__main__":
    entry_point(sys.argv)
