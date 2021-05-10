#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import argparse


def printError(message):
    if not _quiet:
        print('\033[91m[ERROR]\033[0m ' + str(message))
        exit(1)


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('template', help='template file')
    parser.add_argument('-q', '--quiet', action='store_true', help='be quiet, no error message')
    parser.add_argument('-s', '--seed', type=int, help='set seed value')
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
    if _seed:
        fake.seed_instance(_seed)

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

    global _quiet
    global _seed
    _seed = args.seed or 0
    _quiet = args.quiet or False

    template = str(args.template)
    content = fetchContent(template)
    generateData(content)


if __name__ == '__main__':
    main()
