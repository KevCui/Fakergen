#!/usr/bin/python3
# ~$ ./jsonfaker.py <json_template>

import sys
import re
from faker import Faker
from faker.providers import BaseProvider


class customProvider(BaseProvider):
    sentences = (
        'Hello world',
        'Hi there',
        'Ciao Bello',
    )

    def greeting(self):
        return self.random_element(self.sentences)


fake = Faker()
fake.add_provider(customProvider)
jsontemplate = sys.argv[1]
pattern = r'\{\{\w+\([\w=,\s?#\'\":-]*\)\}\}'

with open(jsontemplate) as f:
    content = f.read().splitlines()

for line in content:
    num = len(re.findall(pattern, line))
    if num != 0:
        newline = line
        for i in range(1, num+1):
            item = re.findall(pattern, newline)
            newline = newline.replace(item[0], str(eval('fake.' + re.sub(r'[\{\}]', '', item[0]))), 1)
        print(newline)
    else:
        print(line)
