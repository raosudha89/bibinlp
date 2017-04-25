import sys, pdb
from openpyxl import load_workbook

class Unit:
    def __init__(self, unit_num, sent_num, trigger, question_answer):
        self.unit_num = unit_num
        self.sent_num = sent_num
        self.trigger = trigger
        self.question_answer = question_answer

if __name__ == '__main__':
    original_file = open(sys.argv[1], 'r')
    xlsx_file = sys.argv[2]
    output_file = open(sys.argv[3], 'w')
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
                question_answer = '\t'.join(values[1:10])
                unit = Unit(unit_num, sent_num, trigger, question_answer)
                try:
                    units[sent_num]
                except:
                    units[sent_num] = {}
                units[sent_num][trig_num] = unit
    index = 0
    for k,v in units.iteritems():
        sent_num = k
        num_qas = len(units[sent_num].values())
        output_file.write(('WIKI2_%s\t%s\n') % (index, num_qas))
        sentence = sentences_dict[sent_num]
        output_file.write(sentence.encode('utf-8').strip()+'\n')
        for k,v in units[sent_num].iteritems():
            trig_num = k
            unit = v
            possible_trigger_indices = [i for i, x in enumerate(sentence.split()) if x == unit.trigger]
            trigger_index = None
            if len(possible_trigger_indices) != 1:
                for possible_trigger_index in possible_trigger_indices:
                    if possible_trigger_index in sentence_num_trigger_index_dict[sent_num]:
                        if trigger_index:
                            pdb.set_trace()
                        else:
                            trigger_index = possible_trigger_index
            else:
                trigger_index = possible_trigger_indices[0]
            output_file.write(('%s\t%s\t%s\n') % (trigger_index, unit.trigger, trig_num))
            output_file.write(unit.question_answer.encode('utf-8').strip()+'\n')
        output_file.write('\n')
        index += 1
            
                
                    
                    