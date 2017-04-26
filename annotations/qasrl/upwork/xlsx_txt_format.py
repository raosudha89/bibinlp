import sys, pdb
from openpyxl import load_workbook

class Unit:
    def __init__(self, unit_num, sent_num, trigger, question_answer):
        self.unit_num = unit_num
        self.sent_num = sent_num
        self.trigger = trigger
        self.question_answer = question_answer

def get_sentence_num_trigger_index_dict(original_file):
    sentence_num_trigger_index_dict = {}
    sent_num = 0
    for line in original_file.readlines():
        if line.strip('\n') == '':
            sent_num += 1
        else:
            index, word, is_predicate = line.strip('\n').split('\t')
            if is_predicate == 'Y':
                try:
                    sentence_num_trigger_index_dict[sent_num]
                except:
                    sentence_num_trigger_index_dict[sent_num] = []
                sentence_num_trigger_index_dict[sent_num].append(index)
    return sentence_num_trigger_index_dict 

def load_units(xlsx_file):
    sent_num = None
    wb = load_workbook(xlsx_file, read_only=True)
    units = {} # {sent_num: {trig_num: unit}}
    sentences_dict = {}
    for sheet_name in wb.get_sheet_names():
        ws = wb[sheet_name]
        for row in ws.rows:
            values = []
            for cell in row:
                values.append(cell.value)
                
            v = values[0]
            v = str(v)
            if 'UNIT' in v:
                unit_num = int(v.split('_')[1])
            elif 'SENT' in v:
                sent_num = int(v.split('_')[1])
                sentence = values[1]
                sentences_dict[sent_num] = sentence
            elif 'TRG' in v:
                trig_num = int(v.split('_')[1])
                trigger = values[1]
            elif 'QA' in v:
                num = v[2]
                if not values[1]: #empty qa
                    continue
                for i in range(1,10):
                    if not values[i]:
                        values[i] = "_"
                values[1] = values[1].encode('utf-8').lower() #lowercase wh words
                question_answer = '\t'.join(values[1:10])
                unit = Unit(unit_num, sent_num, trigger, question_answer)
                try:
                    units[sent_num]
                except:
                    units[sent_num] = {}
                try:
                    units[sent_num][trig_num]
                except:
                    units[sent_num][trig_num] = []
                units[sent_num][trig_num].append(unit)
    return units, sentences_dict

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: python xlsx_txt_format.py <output_file> <original_file xlxs_file>'
        sys.exit(0)
    output_file = open(sys.argv[1], 'w')
    index = 0
    print len(sys.argv)
    for i in range(2, len(sys.argv), 2):
        print sys.argv[i]
        print sys.argv[i+1]
        original_file = open(sys.argv[i], 'r')
        sentence_num_trigger_index_dict = get_sentence_num_trigger_index_dict(original_file)
        xlsx_file = sys.argv[i+1]
        units, sentences_dict = load_units(xlsx_file)

        for sent_num in units.keys():
            sentence = sentences_dict[sent_num]
            valid_trigger_units = []
            for trig_num, trigger_units in units[sent_num].iteritems():
                trigger = trigger_units[0].trigger
                possible_trigger_indices = [i for i, x in enumerate(sentence.split()) if x == trigger]
                trigger_index = None
                if len(possible_trigger_indices) != 1:
                    for possible_trigger_index in possible_trigger_indices:
                        if str(possible_trigger_index) in sentence_num_trigger_index_dict[sent_num]:
                            if trigger_index:
                                trigger_index = None
                                break
                            else:
                                trigger_index = possible_trigger_index
                else:
                    trigger_index = possible_trigger_indices[0]
                if not trigger_index:
                    continue
                valid_trigger_units.append([trigger_index, trigger, trigger_units])
                
            output_file.write(('WIKI2_%s\t%s\n') % (index, len(valid_trigger_units)))
            output_file.write(sentence.encode('utf-8').strip()+'\n')
            for trigger_index, trigger, trigger_units in valid_trigger_units:
                output_file.write(('%s\t%s\t%s\n') % (trigger_index, trigger, len(trigger_units)))
                for trigger_unit in trigger_units:
                    output_file.write(trigger_unit.question_answer.encode('utf-8').strip()+'\n')
            output_file.write('\n')
            index += 1
            
                
                    
                    
