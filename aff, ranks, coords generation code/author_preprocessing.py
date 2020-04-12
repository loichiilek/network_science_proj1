import xml.sax
import csv
import pdb

author_list = []


class AuthorHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.new_author = False  # flag that indicates that new elements are to be saved
        self.working_tag = None
        self.working_pid = None
        # self.working_authors = []
        self.aff_content = ''
        self.working_affiliations = []
        self.count = 0

    def startElement(self, tag, attributes):
        if self.new_author:         
            if tag == 'note':
                if 'type' in attributes and 'affiliation' in attributes['type']:
                    self.working_tag = 'affiliation'
            return

        if tag == 'www':
            if 'key' in attributes and 'homepages' in attributes['key']:
                self.new_author = True
                # key is something like homepages/31/3692, pid is 31/3692
                self.working_pid = attributes['key'][10:]

    def endElement(self, tag):
        # if at the end of document, save all
        if tag == 'dblp':
            self.save_data()
            print(f'All authors saved.')

        # if not within a <www key='homepages/...'> tag, skip tag.
        if not self.new_author:
            return

        if tag == 'www' and self.new_author is True:
            self.new_author = False
            self.add_authors_to_list()
            self.working_pid = None
            self.working_affiliations = []
            self.count += 1
            if self.count >= 1000:
                print('Saving..')
                self.save_data()
                self.count = 0
                author_list.clear()

        elif self.working_tag == 'affiliation':
            self.working_affiliations.append(self.aff_content)
            self.aff_content = ''
            self.working_tag = None

    def characters(self, content):
        if self.working_tag == 'affiliation':
            # sometimes the parser returns the characters within one tag in chunks
            self.aff_content += content

    def add_authors_to_list(self):
        # those without affiliations
        if len(self.working_affiliations) == 0:
            self.working_affiliations.append('-')

        for aff in self.working_affiliations:
            author_list.append({
                'pid': self.working_pid,
                'affiliation': aff
            })

    def save_data(self):
        with open('author_pid_to_inst.csv', 'a', encoding='utf8', newline='') as output_file:
            fc = csv.DictWriter(output_file, fieldnames=author_list[0].keys())
            fc.writeheader()
            fc.writerows(author_list)


if __name__ == '__main__':
    parser = xml.sax.make_parser()
    # turn off namespaces, our XML does not use them
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override default handler
    handler = AuthorHandler()
    parser.setContentHandler(handler)

    # unzipped = gzip.open('dblp.xml.gz', 'r')
    # parser.parse(unzipped)
    parser.parse("dblp.xml")

    # pdb.set_trace()
