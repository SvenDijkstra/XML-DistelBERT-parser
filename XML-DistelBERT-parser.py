import xml.etree.ElementTree as ET
import os
from tqdm import tqdm

# set the path of the xml file
xml_path = '/Path/to/Posts.xml'

# create a dictionary to group posts by their post type id
post_type_dict = {}

# create a generator to iterate over the xml file
def post_generator():
    context = ET.iterparse(xml_path, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag == 'row':
            yield elem.attrib
            root.clear()

# iterate over the generator and group posts by their post type id
for post in tqdm(post_generator(), desc='Processing Posts'):
    post_type_id = post['PostTypeId']
    if post_type_id not in post_type_dict:
        post_type_dict[post_type_id] = []
    post_type_dict[post_type_id].append(post)

# create folders for each post type id and save the corresponding posts
for post_type_id, posts in tqdm(post_type_dict.items(), desc='Saving Posts'):
    folder_path = f'post_type_{post_type_id}'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(f'{folder_path}/posts.txt', 'w') as f:
        for post in tqdm(posts, desc=f'Saving Posts of type {post_type_id}'):
            f.write(f'{post}\n')

