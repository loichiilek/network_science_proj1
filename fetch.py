import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json
import csv
import time
import os

# To grab the xml for different convention and organize the information 

# q :       query string
# h :       max number of hits
# f :       first parameter
# c :       max completion terms
# format :  xml/ json

BASE_URL = "https://dblp.uni-trier.de/search/publ/api"

# Can be replaced with a config/text file or whatnot
CONF_LIST = [
    "sigmod",
    "vldb",
    "kdd",
    "edbt",
    "icde",
    "icdm",
    "sdm",
    "cikm",
    "dasfaa",
    "pakdd",
    "pkdd",
    "dexa"
]


def query_string_builder(conf_string):

    query_string = "stream:streams/conf/{}:".format(conf_string)

    return query_string

def send_request(q, h, f, format = "json"):
    http = urllib3.PoolManager()
    response = http.request('GET', BASE_URL, fields={
        'q' : q,
        'h' : h,
        'f' : f,
        'format' : format
    })
    
    return response.data

def num_hits_in_conf(conf):
    query_string = query_string_builder(conf)
    json_data = json.loads(send_request(query_string, 0, 0).decode('utf-8'))

    return int(json_data['result']['hits']['@total'])


# list of dict
def add_entry_to_list(authors_list, pid, name, year, conf):
    authors_list.append({
        'pid' : pid,
        'name' : name,
        'year' : year,
        'conf' : conf
    })

def add_conf_to_csv(conf):
    
    authors_list = []
    query_string = query_string_builder(conf)
    h = 1000
    f = 0
    # load 1000 each time
    for i in range(int(num_hits_in_conf(conf) / 1000) + 1):
        print(conf, f)
        # Send request
        json_data = json.loads(send_request(query_string, h, f).decode('utf-8'))

        # Iterate through each publication
        for publication in json_data['result']['hits']['hit']:
            # BASICALLY, some publications don't have a single fucking author.
            if not 'authors' in publication['info'].keys():
                continue

            authors = publication['info']['authors']['author']
            year = publication['info']['year']

            # Check if object is a list, they do not hold list of length 1 hence the extra check.
            if type(authors) is list:
                for author in authors:
                    add_entry_to_list(authors_list, author['@pid'], author['text'], year, conf)
            else:
                add_entry_to_list(authors_list, authors['@pid'], authors['text'], year, conf)



        # Increase f
        f += 1000

    # Check file exists
    file_exists = True
    if not os.path.isfile('authors.csv'):
        file_exists = False
    # Append CSV
    with open('authors.csv', 'a', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=authors_list[0].keys())

        if not file_exists:
            fc.writeheader()

        fc.writerows(authors_list)

def create_csv(conf_list):
    beginning = time.time()
    for conf in conf_list:
        start = time.time()
        print("===============================================")
        print("starting {}".format(conf))
        add_conf_to_csv(conf)
        print("completed {}".format(conf))
        print("time elapsed: {:.3f}s\n".format(time.time()-start))

    
    print("total time elapsed: {:.3f}s\n".format(time.time()-beginning))


# Calling main function
create_csv(CONF_LIST)