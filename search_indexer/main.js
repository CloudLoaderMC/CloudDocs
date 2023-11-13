// Currently needed packages:
// - elasticlunr

const fs = require('fs');
const elasticlunr = require('elasticlunr');

let sections_path = process.argv[2];

let sections = JSON.parse(fs.readFileSync(sections_path, 'utf8'));

var index = elasticlunr(function() {
  this.addField('title');
  this.addField('body');
  this.addField('breadcrumbs');
  this.setRef('id');
});

let doc_urls = [];

for (let i = 0; i < sections.length; i++) {
  let section = sections[i];

  let url = section['path'].replaceAll(/\s\s+/gm, ' ');
  if (section['id'] != null) {
    url += '#' + section['id'];
  }
  let doc_ref = doc_urls.length.toString();
  doc_urls.push(url);

  let body = section['content'];
  for (let j = 0; j < section['sub_items'].length; j++) {
    body = body.replace(section['sub_items'][j]['content'], '');
  }

  index.addDoc({
    title: section['name'],
    body: body,
    breadcrumbs: section['parent_names'].slice(1).join(' » '),
    id: doc_ref,
  });
}

let results_options = {
  'limit_results': 20,
  'teaser_word_count': 30,
};

let search_options = {
  'bool': 'AND',
  'expand': true,
  'fields': {
    'body': { 'boost': 1 },
    'breadcrumbs': { 'boost': 2 },
    'title': { 'boost': 2 },
  },
};

let result = {
  'results_options': results_options,
  'search_options': search_options,
  'doc_urls': doc_urls,
  'index': index.toJSON(),
};
result['index']['lang'] = 'English';
console.log(JSON.stringify(result));

