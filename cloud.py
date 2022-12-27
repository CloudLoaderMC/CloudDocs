import json
import sys
import urllib.request


def log(text):
    with open("cloud-preprocessor.log", "a+") as f:
        f.write(str(text))
        f.write("\n")

if __name__ == '__main__':
    if len(sys.argv) > 1: # We check if we received any argument
        if sys.argv[1] == "supports":
            # Then we are good to return an exit status code of 0, since the other argument will just be the renderer's name
            sys.exit(0)
          
    context, book = json.load(sys.stdin)
    
    # log(book)

    variables = {
        'docs_version': '0.0.1'
    }

    url = 'https://meta.cloudmc.ml/v1/versions/loader/'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as url:
            data = json.loads(url.read().decode())
            
            # TODO: Adjust to API
            variables['version'] = data[0]['game_version']
    
            if variables['version'] == variables['docs_version']:
                variables['version_text'] = 'The current version is ' + variables['version'] + '.'
            else:
                higher = False
                for i in range(len(variables['version'].split('.'))):
                    if int(variables['docs_version'].split('.')[i]) > int(variables['version'].split('.')[i]):
                        higher = True
                        break
                if higher:
                    variables['version_text'] = 'Warning: This documentation is for version ' + variables['docs_version'] + ' but the latest version is only ' + variables['version'] + '. Some things might have changed from the latest release.'
                else:
                    variables['version_text'] = 'Warning: This documentation is for version ' + variables['docs_version'] + ' but the latest version is ' + variables['version'] + '. Some things might have changed since the docs were last updated.'
    except:
        variables['version'] = ''
        variables['version_text'] = ''
    
    # log(variables)
    
    for i in range(len(book['sections'])):
        for key in variables:
            if 'Chapter' in book['sections'][i]:
                book['sections'][i]['Chapter']['content'] = book['sections'][i]['Chapter']['content'].replace('{{ ' + key + ' }}', variables[key])
            
    print(json.dumps(book))
