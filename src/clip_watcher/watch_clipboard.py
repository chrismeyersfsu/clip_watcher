#!/usr/bin/env python3

import json
import time
import re
import logging

import pyperclip


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


RE_JSON_STARTS_WITH = re.compile('^\s*{')
RE_JSON_ENDS_WITH = re.compile('}\s*$')


def is_json(clipboard_content):
    if not RE_JSON_STARTS_WITH.search(clipboard_content):
        return False, "does not start with }"
    if not RE_JSON_ENDS_WITH.search(clipboard_content):
        return False, "does not end with }"
    return True, "starts with { and ends with }"


def save_json_to_file(clipboard_content):
    # TODO: Try catch to see if actually json
    try:
        d = json.loads(clipboard_content)
    except json.decoder.JSONDecodeError:
        return False, "json.loads() failed"

    return True, json.dumps(d, indent=2)


class ClipboardWatcher():
    def __init__(self, handlers):
        self._handlers = handlers

    def run(self):
        while True:
            try:
                clipboard_content = pyperclip.waitForNewPaste()
                logger.debug(f"new clipboard content '{clipboard_content}'")
                for handler in self._handlers:
                    deciders = handler['deciders']
                    parser = handler['parser']
                    name = handler['name']

                    possible_match = False
                    l = len(deciders)
                    for i, d in enumerate(deciders):
                        possible_match, reason = d(clipboard_content)
                        if not possible_match:
                            logger.debug(f"DECIDER FAIL {name} STEP {d.__name__} '{reason}'")
                            break
                        logger.debug(f"DECIDER PASS {name} STEP {i+1} of {l} {d.__name__} '{reason}'")

                    if possible_match:
                        res, content = parser(clipboard_content)
                        if res:
                            if logging.DEBUG >= logger.level:
                                # TODO: Multi-line output isn't pretty in the log coming from content
                                logger.debug(f"PARSER PASS {name} {parser.__name__} '{content}'")
                            else:
                                logger.info(f"PARSER PASS {name} {parser.__name__}")

                            pyperclip.copy(content)
                            with open('/tmp/clip', 'w') as f:
                                f.write(content)
                        else:
                            logger.info(f"PARSER FAIL {name} {parser.__name__} '{clipboard_content}'")


            except KeyboardInterrupt:
                break

def main():
    watcher = ClipboardWatcher([{
            'name': 'json',
            'deciders': [is_json],
            'parser': save_json_to_file
        }])
    watcher.run()

if __name__ == "__main__":
    main()
