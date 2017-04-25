import sys, pdb, os
from bs4 import BeautifulSoup
import nltk

if __name__ == '__main__':
    html_dir = sys.argv[1]
    output_file = open(sys.argv[2], 'w')
    output_file.write("id\tsentence\n")
    id = 1
    for file in os.listdir(html_dir):
        html = open(os.path.join(html_dir, file), 'r')
        parsed_html = BeautifulSoup(html, 'html.parser')
        section = parsed_html.find('section', attrs={'id':'contentReviews'})
        if section:
            for div in section.find_all('div', attrs={'class':'media-body'}):
                if div.p:
                    review = div.p.text.strip('\n').strip()
                    sents = nltk.sent_tokenize(review)
                    if len(sents) > 1:
                        continue
                    output_file.write("%s\t%s\n" % (id, review.encode('utf-8')))
                    id += 1
    output_file.close()