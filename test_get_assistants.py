#!/usr/bin/env python3

import pprint
from utils import get_assistants


def test_get_assistants():
    data = get_assistants('assistants.yml')
    pprint.pprint(data)


if __name__ == '__main__':
    test_get_assistants()
