# -*- coding: utf-8 -*-
from faker.providers import BaseProvider


class CustomProvider(BaseProvider):
    sentences = (
        'Hello world',
        'Hi there',
        'Ciao Bello',
    )

    def greeting(self):
        return self.random_element(self.sentences)
