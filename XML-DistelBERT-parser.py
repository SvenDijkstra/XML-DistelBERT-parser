import xml.etree.ElementTree as ET
import os
import psutil
from tqdm import tqdm

# set paths
xml_path = '/mnt/e/05-DATA/StackOverflowDatasets/Stackoverflow.com-Posts/Posts.xml'
output_dir = 'stackoverflow_data'

# create output directories
os.makedirs(os.path.join(output_dir, 'questions'), exist_ok=True)
os.makedirs(os.path.join(output_dir, 'answers'), exist_ok=True)

# process post element
def process_post(elem):
    post_type = elem.get('PostTypeId')
    post_id = elem.get('Id')
    post_body = elem.get('Body')
    
    # process question post
    if post_type == '1':
        with open(os.path.join(output_dir, 'questions', f'{post_id}.txt'), 'w') as f:
            f.write(post_body)
    
    # process answer post
    if post_type == '2':
        parent_id = elem.get('ParentId')
        with open(os.path.join(output_dir, 'answers', f'{post_id}.txt'), 'w') as f:
            f.write(post_body)
            f.write('\n' + parent_id + '\n')
    
    # clear memory when it reaches about 10GB
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    if mem_info.rss > 10 * 1024 * 1024 * 1024:
        del elem
        del post_body
        del parent_id
        del post_id
        del post_type

# iterate through xml file and process posts
context = ET.iterparse(xml_path, events=('start', 'end'))
_, root = next(context)
for event, elem in tqdm(context, desc="Processing Posts"):
    if event == 'end' and elem.tag == 'row':
        process_post(elem)
        root.clear()
