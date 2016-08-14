# GenAn
[![MIT](https://camo.githubusercontent.com/52ec9e2dfec7264e254fb7af5ac87f301ced9180/68747470733a2f2f696d672e736869656c64732e696f2f707970692f6c2f417270656767696f2e737667)](https://raw.githubusercontent.com/hyperium/hyper/master/LICENSE)

DSL for definition of client-side application based on AngularJS.
#### Installation:

git clone https://github.com/theshammy/GenAn.git

Run genan.py in main package from command line: `genan -source_file -destination_folder`

#### Dependencies:
* Arpeggio
* textX
* Jinja2

##### Database
* mongoDB
* robomongo db client

##### Backend
* node.js and npm: https://nodejs.org/en/download/  or better:
* use nvm, follow installation manual from https://github.com/creationix/nvm and then install:
* node.js and npm v5.12:
`nvm install v5.12`
* express:
`npm install -g express`
* express generator:
`npm install -g express-generator`
* express cli:
`npm install -g express-cli`
* gulp:
`npm install -g gulp`

### Usage:

There are three concepts in GenAn:
* Object: Contains properties which are basic component or views. These properties describe how an entity should be visualized.
* View: Part of a page, containing other views or object references.
* Page: HTML page, containing views or object references.

Examples are located in test directory.

Once executed, GenAn will generate html pages described in a .gn file using the after mentioned concepts. GenAn also provides AngularJS application and node.js backend generation.

Documentation will be available soon.
