# GenAn
[![MIT](https://camo.githubusercontent.com/52ec9e2dfec7264e254fb7af5ac87f301ced9180/68747470733a2f2f696d672e736869656c64732e696f2f707970692f6c2f417270656767696f2e737667)](https://raw.githubusercontent.com/hyperium/hyper/master/LICENSE)

DSL for definition of client-side application based on AngularJS.
#### Instalation:

git clone https://github.com/theshammy/GenAn.git

Run genan.py in main package.

#### Dependencies:
* Arpeggio
* textX
* Jinja2

##### Backend
* node.js and npm: https://nodejs.org/en/download/
* express:
`npm install -g express`
* express generator:
`npm install -g express-generator`

### Usage:

There are three concepts in GenAn:
* Object: Contains properties which are basic component or views. These properties describe how an entity should be visualized.
* View: Part of a page, containing other views or object references.
* Page: HTML page, containing views or object references.

Examples are located in test directory.

Once executed, GenAn will generate html pages described in a .gn file using the after mentioned concepts. GenAn also provides AngularJS application and node.js backend generation.

To run GenAn, execute genan.py inside src/main and follow the instructons. Documentation will be available soon.
