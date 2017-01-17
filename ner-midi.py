#!/usr/bin/env python

import sys
import os
import pprint
import operator
import copy

class NERMidi(object):
    def __init__(self, __path):
        self.path = __path
        self.records = []
        self.sep = [' ', '.', '_', '-']

    def process(self):
        for root, dirs, files in os.walk(path):
            for f in files:
                if '.mid' in f:
                    record = {}
                    # Full path of the MIDI file
                    record['midi_path'] = os.path.join(root, f)
                    # MIDI file name
                    record['midi_filename'] = f
                    # Without the extension
                    record['midi_name'] = f[:f.rfind('.')]

                    record['separators'] = {}
                    for s in self.sep:
                        record['separators'][s] = record['midi_name'].count(s)

                    # Use the max of the previous count as tokenizer
                    record['sep_max'] = max(record['separators'].iteritems(), key=operator.itemgetter(1))[0]
                    temp = copy.copy(record['separators'])
                    # We'll also store the 2nd max
                    del temp[record['sep_max']]
                    record['sep_2nd_max'] = max(temp.iteritems(), key=operator.itemgetter(1))[0]
                    del temp

                    # A draw between '-' and '_' should put priority in the latter
                    if record['sep_max'] == '-' and record['sep_2nd_max'] == '_' and  record['separators'][record['sep_max']] == record['separators'][record['sep_2nd_max']]:
                        record['sep_max'] = '_'
                        record['sep_2nd_max'] = '-'

                    record['tokens'] = [token.strip() for token in record['midi_name'].split(record['sep_max'])]
                    record['normal_blanks'] = ' '.join(record['tokens'])

                    # Use the 2nd_max to separate entities
                    # The latter is only useful if it's > 0
                    record['entities'] = [entity.strip() for entity in record['normal_blanks'].split(record['sep_2nd_max'])] if record['separators'][record['sep_2nd_max']] > 0 else [record['normal_blanks']]

                    self.records.append(record)

        return None

    def print_records(self):
        pp = pprint.PrettyPrinter(indent=4)
        for r in self.records:
            pp.pprint(r)
            print

        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: ner-midi.py PATH-TO-MIDIS"
        exit(1)

    path = sys.argv[1]
    ner_midi = NERMidi(path)
    ner_midi.process()
    ner_midi.print_records()

    exit(0)
