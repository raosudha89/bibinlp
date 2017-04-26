import sys, pdb

if __name__ == '__main__':
    tsv_file = open(sys.argv[1], 'r')
    blind_tsv_file = open(sys.argv[2], 'w')
    i = 0
    blind_tsv_file.write("id\tprefix\tpredicate\tsuffix\n")
    seen_sent_predicate_ids = []
    for line in tsv_file.readlines():
        if i == 0:
            i += 1
            continue
        id, prefix, predicate, suffix, question, answer = line.split('\t')
        sent_predicate_id = '.'.join(id.split('.')[:2])
        if sent_predicate_id not in seen_sent_predicate_ids:
            blind_tsv_file.write("%s\t%s\t%s\t%s\n" % (sent_predicate_id, prefix, predicate, suffix))
            seen_sent_predicate_ids.append(sent_predicate_id)
    tsv_file.close()
    blind_tsv_file.close()
        