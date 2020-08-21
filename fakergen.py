#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import re
import argparse

_silent = False


def printError(message):
    if not _silent:
        print('\033[91m[ERROR]\033[0m ' + str(message))
        sys.exit(1)


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('template', nargs=1, help='Faker template file')
    parser.add_argument('-s', '--silent', action='store_true', help='Don\'t show error message')
    return parser.parse_args()


def fetchContent(templateFile):
    try:
        with open(templateFile) as f:
            return f.read().splitlines()
    except FileNotFoundError as err:
        printError(err)


def generateData(templateContent):
    from faker import Faker
    fake = Faker()

    try:
        from customprovider import CustomProvider
        fake.add_provider(CustomProvider)
    except (ModuleNotFoundError, ImportError):
        pass

    pattern = r'\{\{\w+\([\w=,\s?#\'\":-]*\)\}\}'

    for line in templateContent:
        num = len(re.findall(pattern, line))
        if num != 0:
            newline = line
            for i in range(1, num+1):
                item = re.findall(pattern, newline)
                try:
                    newline = newline.replace(item[0], str(eval('fake.' + re.sub(r'[\{\}]', '', item[0]))), 1)
                except AttributeError as err:
                    printError(err)
            print(newline)
        else:
            print(line)


def main():
    args = parseArgs()

    global _silent
    _silent = args.silent

    template = str(args.template[0])
    content = fetchContent(template)
    generateData(content)


if __name__ == '__main__':
    main()
