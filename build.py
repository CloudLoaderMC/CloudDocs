import os
import shutil
import markdown
from bs4 import BeautifulSoup

SOURCE_PATH = 'src'
CSS_PATH = 'css'
JS_PATH = 'js'
IMAGES_PATH = 'img'
TARGET_PATH = 'html'
TEMPLATE_PATH = 'template.html'
SUMMARY_SOURCE_PATH = 'SUMMARY.md'

SEARCH_INDEXER_PATH = 'search_indexer/main.js'
SEARCH_INDEX_PATH = 'search_index.js'

VARIABLES = {}

template = ''
with open(TEMPLATE_PATH, 'r') as f:
    template = f.read()

summary = ''
index_path = ''

sections = []


def run_command(command):
    import subprocess

    return subprocess.run(command, stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')[:-1]


def list_files(path):
    result = {}
    for f in os.listdir(path):
        if os.path.isdir(os.path.join(path, f)):
            result[f] = list_files(os.path.join(path, f))
        elif os.path.join(path, f) != os.path.join(SOURCE_PATH, 'SUMMARY.md'):
            result[f] = None
    return result


def fetch_cloud_variables():
    import json
    import urllib.request

    global VARIABLES

    print('Fetching Cloud variables...')

    variables = {
        'docs_version': '0.0.1'
    }

    url = 'https://meta.cloudloader.org/v1/versions/loader/'
    try:
        req = urllib.request.Request(
            url, headers={'User-Agent': 'Mozilla/5.0'})

        with urllib.request.urlopen(req) as url:
            data = json.loads(url.read().decode())
            # TODO: Adjust to API
            variables['version'] = data[0]['game_version']

            if variables['version'] == variables['docs_version']:
                variables['version_text'] = 'The current version is ' + \
                    variables['version'] + '.'
            else:
                higher = False
                for i in range(len(variables['version'].split('.'))):
                    if int(variables['docs_version'].split('.')[i]) > int(variables['version'].split('.')[i]):
                        higher = True
                        break
                if higher:
                    variables['version_text'] = 'Warning: This documentation is for version ' + variables['docs_version'] + \
                        ' but the latest version is only ' + \
                        variables['version'] + \
                        '. Some things might have changed from the latest release.'
                else:
                    variables['version_text'] = 'Warning: This documentation is for version ' + variables['docs_version'] + \
                        ' but the latest version is ' + \
                        variables['version'] + \
                        '. Some things might have changed since the docs were last updated.'
    except:
        variables['version'] = ''
        variables['version_text'] = ''

    VARIABLES.update(variables)


def parse_variables(content):
    for key in VARIABLES:
        content = content.replace('{{ ' + key + ' }}', VARIABLES[key])
    return content


def get_admonition_title(ty):
    if ty in ['quote', 'cite']:
        return 'Quote'
    elif ty in ['example']:
        return 'Example'
    elif ty in ['bug']:
        return 'Bug'
    elif ty in ['danger', 'error']:
        return 'Danger'
    elif ty in ['failure', 'fail', 'missing']:
        return 'Failure'
    elif ty in ['warning', 'caution', 'attention']:
        return 'Warning'
    elif ty in ['question', 'help', 'faq']:
        return 'Question'
    elif ty in ['success', 'check', 'done']:
        return 'Success'
    elif ty in ['tip', 'hint', 'important']:
        return 'Tip'
    elif ty in ['info', 'todo']:
        return 'Info'
    elif ty in ['abstract', 'summary', 'tldr']:
        return 'Abstract'
    else:
        return 'Note'


def get_admonition_class(ty):
    if ty in ['quote', 'cite']:
        return 'quote'
    elif ty in ['example']:
        return 'example'
    elif ty in ['bug']:
        return 'bug'
    elif ty in ['danger', 'error']:
        return 'danger'
    elif ty in ['failure', 'fail', 'missing']:
        return 'failure'
    elif ty in ['warning', 'caution', 'attention']:
        return 'warning'
    elif ty in ['question', 'help', 'faq']:
        return 'question'
    elif ty in ['success', 'check', 'done']:
        return 'success'
    elif ty in ['tip', 'hint', 'important']:
        return 'tip'
    elif ty in ['info', 'todo']:
        return 'info'
    elif ty in ['abstract', 'summary', 'tldr']:
        return 'abstract'
    else:
        return 'note'


def add_element_classes(content, element, classes):
    import re

    pattern = r'<(?!\/)' + element

    result = content

    if element not in result:
        return result

    elements = re.split(pattern, result)
    for i in range(len(elements)):
        if i < len(elements) - 1:
            one_part = False
            split = elements[i + 1].split('>', 1)
            if split[0].endswith('/'):
                one_part = True
                if split[0].endswith(' /'):
                    split[0] = split[0][:-1]
                split[0] = split[0][:-1]
            if 'class' not in split[0]:
                split[0] = split[0] + ' class="' + \
                    classes + '"'
            if one_part:
                split[0] += ' /'
            elements[i + 1] = '>'.join(split)
    result = ('<' + element).join(elements)
    return result


def apply_styling(content):
    result = content

    result = add_element_classes(result, 'h1', 'fw-bold')
    result = add_element_classes(result, 'hr', 'border')

    return result


def convert_markdown(content, style=True, handle_toc=False):
    from markdown.extensions.toc import TocExtension
    from mdx_outline import OutlineExtension

    md = markdown.Markdown(
        extensions=['fenced_code', TocExtension(toc_depth=3, anchorlink=True, anchorlink_class="header"), OutlineExtension()])
    result = content
    result = parse_references(result)
    result = md.convert(result)
    if style:
        result = apply_styling(result)

    if handle_toc:
        return result, md.toc_tokens

    return result


def parse_references(content):
    result = content
    if ']: ' in result:
        reference_links = {}
        lines = result.splitlines(keepends=True)
        for i in range(len(lines)):
            if lines[i].startswith('[') and ']: ' in lines[i]:
                lines[i] = lines[i][1:-1]
                name = lines[i].split(']: ')[0]
                link = lines[i].split(']: ')[1]
                reference_links[name] = link
                lines[i] = ''
        for i in range(len(lines)):
            pretext = ''
            while '][' in lines[i]:
                split = lines[i].split('][', 1)
                name = split[1].split(']', 1)[0]
                if name not in reference_links:
                    pretext += split[0] + '][' + name + ']'
                    lines[i] = split[1].split(']', 1)[1]
                    continue
                lines[i] = split[0] + \
                    '](' + reference_links[name] + ')' + \
                    split[1].split(']', 1)[1]
            lines[i] = pretext + lines[i]
        result = ''.join(lines)
    return result


# def add_header_links(content):
#     result = content
#
#     h1_split = result.split('<h1')
#     for i in range(len(h1_split)):
#         if i == 0:
#             continue
#         split = h1_split[i].split('>', 1)
#         split[1] = '<a class="header" href="#' + split[1] + '">'
#
#
#     return result


def parse_summary():
    global summary, index_path

    content = ''
    print("Parsing: " + os.path.join(SOURCE_PATH, SUMMARY_SOURCE_PATH))
    with open(os.path.join(SOURCE_PATH, SUMMARY_SOURCE_PATH), 'r') as f:
        content = f.read()
    content = parse_references(content)

    lines = content.split('\n')
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith('# '):
            line = '''
<li class="nav-item sidebar-header">
    <b>''' + line[2:] + '''</b>
</li>'''
        elif line.startswith('- [') and '](' in line and line.endswith(')'):
            line = line[2:]
            line = line[1:]
            line = line[:-1]
            name = line.rsplit('](', 1)[0]
            link = line.rsplit('](', 1)[1].replace('.md', '.html')
            if index_path == '':
                index_path = TARGET_PATH + link
            line = '''
<li>
    <a href="''' + link + '''" class="nav-link link-body-emphasis">
        <div class="bi pe-none me-2"></div>
        ''' + name + '''
    </a>
</li>
'''
        lines[i] = line
    content = '\n'.join(lines)

    content = convert_markdown(content)
    summary = content


def parse_html(path):
    global sections

    content = ''
    page_title = ''
    print("Parsing: " + path)
    with open(path, 'r') as f:
        lines = f.read().split('\n')
        if lines[0] == '<!--':
            page_title = lines[1]
            lines = lines[3:]
        content = '\n'.join(lines)
    content = parse_references(content)
    html = template
    if page_title != '':
        html = html.replace('<title>', '<title>' + page_title + ' - ')
    content = parse_variables(content)
    content = content.replace('[X]', '<input disabled="" type="checkbox" checked="">').replace(
        '[ ]', '<input disabled="" type="checkbox">')
    admonition_counts = {}
    while '```admonish' in content:
        split = content.split('```admonish', 1)
        if ' ' in split[1].split('\n')[0]:
            admonition_type = split[1].split()[0]
        else:
            admonition_type = ''
        split[1] = split[1].split('\n', 1)[1]
        if get_admonition_class(admonition_type) not in admonition_counts:
            admonition_counts[get_admonition_class(admonition_type)] = 0
        admonition_counts[get_admonition_class(admonition_type)] += 1
        identifier = 'admonition-' + get_admonition_class(admonition_type) + '-' + str(
            admonition_counts[get_admonition_class(admonition_type)])
        classes = 'admonition ' + get_admonition_class(admonition_type)
        title = get_admonition_title(admonition_type)
        split[0] += f'''
<div id="{identifier}" class="{classes}">
    <div class="admonition-title">
        <p>{title}</p>
        <p><a class="admonition-anchor-link" href="#{identifier}"></a></p>
    </div>
    <div>
        <p>'''
        split[1] = convert_markdown(split[1].split('```', 1)[0]) + '''
        </p>
    </div>
</div>
''' + split[1].split('```', 1)[1]
        content = split[0] + split[1]
    while '~~~admonish' in content:
        split = content.split('~~~admonish', 1)
        if ' ' in split[1].split('\n')[0]:
            admonition_type = split[1].split()[0]
        else:
            admonition_type = ''
        split[1] = split[1].split('\n', 1)[1]
        if get_admonition_class(admonition_type) not in admonition_counts:
            admonition_counts[get_admonition_class(admonition_type)] = 0
        admonition_counts[get_admonition_class(admonition_type)] += 1
        identifier = 'admonition-' + get_admonition_class(
            admonition_type) + '-' + str(admonition_counts[get_admonition_class(admonition_type)])
        classes = 'admonition ' + get_admonition_class(admonition_type)
        title = get_admonition_title(admonition_type)
        split[0] += f'''
<div id="{identifier}" class="admonition {classes}">
    <div class="admonition-title">
        <p>{title}</p>
        <p><a class="admonition-anchor-link" href="#{identifier}"></a></p>
    </div>
    <div>
        <p>'''
        split[1] = convert_markdown(split[1].split('~~~', 1)[0]) + '''
        </p>
    </div>
</div>
''' + split[1].split('~~~', 1)[1]
        content = split[0] + split[1]
    while '```' in content:
        split = content.split('```', 2)
        line = split[1].split('\n', 1)[0]
        line = 'language-' + line
        if line == 'language-' or line.startswith('language- '):
            line = line.replace('language-', '', 1)
        if line.replace(' ', '') != '':
            line = ' class="' + line + '"'
        split[1] = split[1].split('\n', 1)[1]
        split[1] = '''
<pre>
<code''' + line + '>' + split[1].split('```', 1)[0] + '''</code>
</pre>'''
        content = split[0] + split[1] + split[2]
    while '~~~' in content:
        split = content.split('~~~', 2)
        line = split[1].split('\n', 1)[0]
        line = 'language-' + line
        if line == 'language-' or line.startswith('language- '):
            line = line.replace('language-', '', 1)
        split[1] = split[1].split('\n', 1)[1]
        split[1] = '''
<pre>
    <code class="''' + line + '''">
        ''' + split[1].split('~~~', 1)[0] + '''
    </code>
</pre>'''
        content = split[0] + split[1] + split[2]
    content, toc = convert_markdown(content, handle_toc=True)
    html = html.replace('{{ CONTENT }}', content)
    html = html.replace('{{ SUMMARY }}', summary.replace(path.replace(SOURCE_PATH, '').replace('.md', '.html') + '" class="nav-link link-body-emphasis"',
                        path.replace(SOURCE_PATH, '').replace('.md', '.html') + '" class="nav-link active" aria-current="page"'))
    if path.replace(SOURCE_PATH, '') != '/404.md':
        soup = BeautifulSoup(content, 'html.parser')
        sectionOnes = soup.select('.section1')

        for sectionOne in sectionOnes:
            headerOne = sectionOne.select('h1')[0]
            sectOne = {
                'name': headerOne.text,
                'content': sectionOne.text,
                'id': headerOne['id'],
                # number?
                'sub_items': [],
                'path': path.replace(SOURCE_PATH + '/', '').replace('.md', '.html'),
                'source_path': path.replace(SOURCE_PATH + '/', ''),
                'parent_names': [page_title],
            }
            sectionTwos = sectionOne.select('.section2')
            for sectionTwo in sectionTwos:
                headerTwo = sectionTwo.select('h2')[0]
                sectTwo = {
                    'name': headerTwo.text,
                    'content': sectionTwo.text,
                    'id': headerTwo['id'],
                    # number?
                    'sub_items': [],
                    'path': path.replace(SOURCE_PATH + '/', '').replace('.md', '.html'),
                    'source_path': path.replace(SOURCE_PATH + '/', ''),
                    'parent_names': [page_title, headerOne.text],
                }
                sectionThrees = sectionTwo.select('.section3')
                for sectionThree in sectionThrees:
                    headerThree = sectionThree.select('h3')[0]
                    sectThree = {
                        'name': headerThree.text,
                        'content': sectionThree.text,
                        'id': headerThree['id'],
                        # number?
                        'sub_items': [],
                        'path': path.replace(SOURCE_PATH + '/', '').replace('.md', '.html'),
                        'source_path': path.replace(SOURCE_PATH + '/', ''),
                        'parent_names': [page_title, headerOne.text, headerTwo.text],
                    }
                    sectTwo['sub_items'].append(sectThree)
                sectOne['sub_items'].append(sectTwo)
            sectionThrees = sectionOne.select(':not(.section2) > .section3')
            for sectionThree in sectionThrees:
                headerThree = sectionThree.select('h3')[0]
                sectThree = {
                    'name': headerThree.text,
                    'content': sectionThree.text,
                    'id': headerThree['id'],
                    # number?
                    'sub_items': [],
                    'path': path.replace(SOURCE_PATH + '/', '').replace('.md', '.html'),
                    'source_path': path.replace(SOURCE_PATH + '/', ''),
                    'parent_names': [page_title, headerOne.text],
                }
                sectOne['sub_items'].append(sectThree)
            sections.append(sectOne)
            for childOne in sectOne['sub_items']:
                sections.append(childOne)
                for childTwo in childOne['sub_items']:
                    sections.append(childTwo)
    return html


def write(tree, target_path):
    for key in tree.keys():
        value = tree[key]
        if value is not None:
            os.makedirs(os.path.join(target_path, key))
            write(value, os.path.join(target_path, key))
        else:
            with open(os.path.join(target_path, key.replace('.md', '.html')), 'w') as f:
                f.write(parse_html(os.path.join(
                    target_path.replace(TARGET_PATH, SOURCE_PATH), key)))


def write_search_index():
    import json

    print('Writing search index...')

    with open('search_indexer/sections.json', 'w') as f:
        json.dump(sections, f)

    search_index = run_command(
        'node ' + SEARCH_INDEXER_PATH + " " + 'search_indexer/sections.json')
    with open(os.path.join(TARGET_PATH, SEARCH_INDEX_PATH + 'on'), 'w') as f:
        f.write(search_index)
    with open(os.path.join(TARGET_PATH, SEARCH_INDEX_PATH), 'w') as f:
        f.write('Object.assign(window.search, ' + search_index + ');')


if __name__ == '__main__':
    if os.path.exists(TARGET_PATH):
        shutil.rmtree(TARGET_PATH)

    fetch_cloud_variables()

    tree = list_files(SOURCE_PATH)
    parse_summary()
    write(tree, TARGET_PATH)
    write_search_index()
    print("Copying index page...")
    shutil.copyfile(index_path, os.path.join(TARGET_PATH, 'index.html'))

    print("Copying assets...")
    shutil.copytree(CSS_PATH, os.path.join(TARGET_PATH, CSS_PATH))
    shutil.copytree(JS_PATH, os.path.join(TARGET_PATH, JS_PATH))
    shutil.copytree(IMAGES_PATH, os.path.join(TARGET_PATH, IMAGES_PATH))
