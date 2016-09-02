import subprocess
import zipfile

import os
import shutil
from angular_gen.jinja_filters import sub_routes_filter
from jinja2 import Environment, FileSystemLoader
from main.common import BColors, FrontendGenerator

_MSG_HEADER_INFO = BColors.OKBLUE + "ANGULAR GENERATOR:" + BColors.ENDC
_MSG_HEADER_FAIL = BColors.FAIL + "ANGULAR GENERATOR - ERROR:" + BColors.ENDC
_MSG_HEADER_SUCCESS = BColors.OKGREEN + "ANGULAR GENERATOR - SUCCESS:" + BColors.ENDC


class AngularGenerator(FrontendGenerator):
    def __init__(self, model, builtins, path):
        super(AngularGenerator, self).__init__(model, builtins, path)
        self.routes = {}
        self.customIndexRoute = None

    def generate(self):
        print(_MSG_HEADER_INFO + " Started.")
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        if not os.path.exists(os.path.join(self.path, "app", "src", "styles")):
            os.makedirs(os.path.join(self.path, "app", "src", "styles"))

        path = os.path.abspath(__file__)
        module_path = os.path.dirname(path)
        print(_MSG_HEADER_INFO + " Generating Angular framework...")
        shutil.copy(os.path.join(module_path, "templates", "views", "page.css"),
                    os.path.join(self.path, "app", "src", "styles", "page.css"))

        seed_file = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'app.zip')
        try:
            zip_ref = zipfile.ZipFile(seed_file, 'r')
            zip_ref.extractall(self.path)
            zip_ref.close()

            print(_MSG_HEADER_INFO + " Installing dependencies...")

            subprocess.check_call(["npm", "install"], cwd=os.path.join(self.path, "app"))
        except FileNotFoundError:
            print(_MSG_HEADER_FAIL + " Unable to generate framework. Continues...")

        try:
            print(_MSG_HEADER_INFO + " Generating Angular frontend...")
            for concept in self.model.concept:
                if hasattr(concept, 'accept'):
                    concept.accept(self)
            self.generate_route_file()

            api_service_rend = _get_template('api.service.js', backend_url=self.backend_base_url)
            api_service_path = os.path.join(self.path, "app", "src", "app", "shared", "api", "api.service.js")
            api_service_file = open(api_service_path, 'w+')
            print(api_service_rend, file=api_service_file)

            print(_MSG_HEADER_SUCCESS + " Finished the Angular frontend generation.")
        except Exception as e:
            print(_MSG_HEADER_FAIL + str(e))
            print(_MSG_HEADER_FAIL + " Unable to generate Angular frontend.")
            raise e

    def visit_selector_view(self, view):
        return "<div ui-view='{0}'></div>".format(view.name)

    def visit_selector_object(self, object, property):
        if property.type in self.builtins:
            return _generate_basic(object, property)
        else:
            return "<h4><b>{2}:</b></h4><div><h4>{{{{ ctrl_page.{0}.{1} }}}}</h4></div>"\
                .format(object.name, property.name, property.name.capitalize())

    def visit_selector_fk_object(self, object, property, fk_properties):

        metas = {}

        for m in object.meta:
            metas[m.label] = m

        # return foreign key property
        result = ""
        fk_item = "ctrl_page.{0}.{1}".format(object.name, property)
        meta = metas[property]
        type = meta.foreignKeyType
        if type == "single":
            result = form_fk_property(meta, fk_item, fk_properties, False)
        elif type == "list":
            row = form_fk_property(meta, fk_item, fk_properties, True)
            result = "<li ng-repeat=\"fk_item in {0}\">{1}</li>".format(fk_item, row)
            result = "<ul>{0}</ul>".format(result)

        result = "<h4><b>{1}:</b></h4><div>{0}</div>".format(result, property.capitalize())
        return result

    def visit_view(self, view):
        # Rows for this view
        rows = [(row.number, self.visit_row(row)) for row in view.rows]

        route = self._subroutes(view)

        print(_MSG_HEADER_INFO + " Generating controller for {0}".format(view.name))
        main_factory, factories = _get_factories(view)
        controller_rend = _get_template("view.js", view=view, main_factory=main_factory, factories=factories)
        controller_file = _get_ctrl(self.path, view.name)

        print(controller_rend, file=controller_file)

        print(_MSG_HEADER_INFO + " Generating view {0}".format(view.name))

        view_rend = _get_template("view.html", rows=rows)
        view_file = _get_file(self.path, view.name)
        print(view_rend, file=view_file)

        self.routes[view.name] = route

    def visit_page(self, page):
        # Contains contained views
        positions = {}

        route = self._subroutes(page)

        print(_MSG_HEADER_INFO + " Generating page {0}".format(page.name))
        main_factory, factories = _get_factories(page)
        controller_rend = _get_template("page.js", page=page, main_factory=main_factory, factories=factories)
        controller_file = _get_ctrl(self.path, page.name)

        print(controller_rend, file=controller_file)

        for view_on_page in page.views:
            selector = view_on_page.selector
            # Default value is 'center'
            position = view_on_page.position if view_on_page.position else 'center'
            if position not in positions:
                positions[position] = []
            positions[position].append(selector.accept(self))

        menu_exist = 'false'
        sidebar_exist = 'false'
        menu_render = ""
        if page.menubar:
            menu_right = []
            menu_left = []
            menu_exist = 'true'
            for x in page.menubar.menus:
                if len(x.side) == 0:
                    menu_left.append(x)
                else:
                    if x.side[0] == 'left':
                        menu_left.append(x)
                    else:
                        menu_right.append(x)
            menu_render = _get_template("header.html", header=page.menubar, menuRight=menu_right, menuLeft=menu_left)

        sidebar_rend = ""
        if page.sidebar:
            sidebar_rend = _get_template("sidebar.html", sidebar=page.sidebar, menu=menu_exist)
            sidebar_exist = 'true'

        footer_rend = ""
        if page.footer:
            footer_rend = _get_template("footer.html", footer=page.footer, sidebarExist=sidebar_exist)

        page_rend = _get_template("page.html", page=page, positions=positions, sidebar=sidebar_rend, footer=footer_rend,
                                  header=menu_render)
        page_file = _get_file(self.path, page.name)
        print(page_rend, file=page_file)

        self.routes[page.name] = route

        # check if page is marked as index
        if self.customIndexRoute is None and page.indexPage:
            self.customIndexRoute = route


    def visit_action_selector(self, object, actions):
        view_name = object.name + '_form'
        self.routes[view_name] = _get_route(view_name, True)
        _generate_form_ctrl(self.path, object, actions)
        return _generate_form(self.path, object, actions)

    def visit_other_selector(self, name, **kwargs):
        return _get_template("{0}.html".format(name), **kwargs)

    def visit_row(self, row):
        rendered_selector = {
            sub_view.selector: sub_view.selector.accept(self) for sub_view in row.selectors
            }
        return _get_template("row.html", sub_views=row.selectors, rendered_selector=rendered_selector)

    def visit_object(self, object):
        queries = {query.name: _stringify_query(query) for query in object.queries}

        render = _get_template("factory.js", object=object, queries=queries)

        path = os.path.join(self.path, "app", "src", "app", "factories", object.name)
        file_path = "{0}.factory.js".format(object.name)
        full_path = os.path.join(path, file_path)
        if not os.path.exists(path):
            os.makedirs(path)
        file = open(full_path, 'w+')
        print(render, file=file)
        print(_MSG_HEADER_INFO + " Generating factory for {0}".format(object.name))

    def generate_route_file(self):
        render_routes = _get_template("app.routes.js", routes=self.routes, customIndexRoute=self.customIndexRoute)
        render_modules = _get_template("app.modules.js", modules=self.routes)
        path = os.path.join(self.path, "app", "src", "app")
        file_path_routes = "app.routes.js"
        file_path_modules = "app.modules.js"
        full_path_routes = os.path.join(path, file_path_routes)
        full_path_modules = os.path.join(path, file_path_modules)
        if not os.path.exists(path):
            os.makedirs(path)
        file_routes = open(full_path_routes, 'w+')
        print(render_routes, file=file_routes)
        print(_MSG_HEADER_INFO + " Generating app.route.js")
        file_modules = open(full_path_modules, 'w+')
        print(render_modules, file=file_modules)
        print(_MSG_HEADER_INFO + " Generating app.modules.js")

    def _subroutes(self, view):
        route = _get_route(view.name, view)
        try:
            for subview in view.subviews:
                if hasattr(subview, "property") and not hasattr(subview.property, "name"):
                    continue
                # Don't add subview if its a basic component
                if hasattr(subview, "property") and hasattr(subview.property, "name")\
                        and subview.property.name not in self.builtins:
                    continue
                if hasattr(subview, "name"):
                    sub_route = _get_route(subview.name)
                    if sub_route not in route['sub_routes']:
                        route['sub_routes'].append(self._subroutes(subview))
            return route
        except:
            print(view)
            print(dir(view))


def _get_template(template_name, **kwargs):
    """
    _get_template(template_name, **kwargs)
    Gets template under generation/templates folder and its subfolders.
    Takes additional parameters required for the template to be rendered.
    """
    path = os.path.abspath(__file__)
    module_path = os.path.dirname(path)
    env = Environment(trim_blocks=True, lstrip_blocks=True,
                      loader=FileSystemLoader([os.path.join(module_path, "templates"),
                                               os.path.join(module_path, "templates", "views"),
                                               os.path.join(module_path, "templates", "views", "basic"),
                                               os.path.join(module_path, "templates", "views", "data_show"),
                                               os.path.join(module_path, "templates", "views", "frame"),
                                               os.path.join(module_path, "templates", "controllers"),
                                               os.path.join(module_path, "templates", "route")
                                               ]))

    env.filters['sub_routes'] = sub_routes_filter
    template = env.get_template("{0}".format(template_name))
    return template.render(kwargs)


def _generate_basic(o, prop):
    return _get_template("{0}.html".format(prop.type),
                         o=o, prop=prop, type=prop.type.name)


def _get_file(path, name):
    path = os.path.join(path, "app", "src", "app", "views", name)
    file_path = "{0}.html".format(name)
    full_path = os.path.join(path, file_path)

    if not os.path.exists(path):
        os.makedirs(path)

    file = open(full_path, 'w+')
    return file


def _get_route(name, page=None, id=False):
    relative_path = "app/views/" + name + "/" + name + ".html"
    path = "/{0}".format(name)
    if page and hasattr(page, "urlParams"):
        for prm in page.urlParams:
            path += "/{{{0}}}".format(prm.param)
    return {
        'name': name,
        'path': path,
        'template': relative_path,
        'controller': "{0}".format(name),
        'sub_routes': [],
        'id': id
    }


def _get_ctrl(path, name):
    path = os.path.join(path, "app", "src", "app", "controllers", name)
    file_path = "{0}.controller.js".format(name)
    full_path = os.path.join(path, file_path)
    if not os.path.exists(path):
        os.makedirs(path)
    file = open(full_path, 'w+')
    return file


def _get_factories(view):
    factories_queries = {}
    # query_params = {}
    query = 'getAll'
    query_by_id = 'getById'
    main_factory = None

    # page with params
    if hasattr(view, "urlParams"):
        for param in view.urlParams:
            if param.object.name not in factories_queries:
                main_factory = param.object.name
                # foreign key entities
                if hasattr(param.object, "meta"):
                    fk_entities = [meta.object.name for meta in param.object.meta]
                    for fk in fk_entities:
                        if fk not in factories_queries and fk != main_factory:
                            factories_queries[fk] = query_by_id

                # factories_queries[param.object.name] = [query_by_id]
            #     query_params[query_by_id] = []
            # if query_by_id in query_params:
            #     query_params[query_by_id].append(param.param)

    for view_on_page in view.views:

        if hasattr(view_on_page, 'object'):
            if view_on_page.object.name not in factories_queries:
                if view_on_page.object.name != main_factory:
                    factories_queries[view_on_page.object.name] = query

        if hasattr(view_on_page, 'selector'):
            selector = view_on_page.selector

            # single object property
            if hasattr(selector, 'object'):
                if selector.object.name not in factories_queries:
                    if selector.object.name != main_factory:
                        factories_queries[selector.object.name] = query

            # data_show
            if hasattr(selector, 'data'):
                for selector_obj in selector.data:
                    if selector_obj.object.name not in factories_queries:
                        if selector_obj.object.name != main_factory:
                                factories_queries[selector_obj.object.name] = query

            # foreign key entities
            if hasattr(selector, "object") and hasattr(selector.object, "meta"):
                fk_entities = [meta.object.name for meta in selector.object.meta]
                for fk in fk_entities:
                    if fk not in factories_queries and fk != main_factory:
                        factories_queries[fk] = query_by_id

            # if hasattr(selector, 'fkProperties'):
            #     for property in selector.fkProperties:
            #         property

    if hasattr(view, 'object') and view.query:
        if main_factory is not None and view.object.name != main_factory:
            factories_queries[view.object.name] = view.query.name

    return main_factory, factories_queries


def _generate_form_ctrl(path, obj, actions):
    form_inputs = []
    distinct_meta = _distinct_meta_objects(obj)

    for property in obj.properties:
        if property.type is 'checkbox':
            render = _get_template("checkbox.js", name=property.name)
            form_inputs.append(render)
        elif property.type is 'date':
            render = _get_template("date.js", name=property.name)
            form_inputs.append(render)

    controller_rend = _get_template("form.js", name=obj.name, meta=distinct_meta, formInputs=form_inputs, actions=actions)
    controller_file = _get_ctrl(path, obj.name + "_form")

    print(controller_rend, file=controller_file)


def _stringify_query(query):
    string = ""
    if hasattr(query, 'property') and query.property:
        string += query.property.name + '&'
    if hasattr(query, 'condition') and query.condition:
        string += query.condition.conditionName + "$" + str(query.condition.parameter) + '&'
    if hasattr(query, 'sortBy') and query.sortBy:
        string += 'sortBy=' + query.sortBy.name + '&'
    if hasattr(query, 'order') and query.order:
        string += 'order=' + query.order + '&'
    if hasattr(query, 'rangeFrom'):
        string += 'from=' + str(query.rangeFrom) + '&'
    if hasattr(query, 'rangeTo') and query.rangeTo != 0:
        string += 'to=' + str(query.rangeTo) + '&'
    if len(string) > 0:
        string = string[:-1]
    return string


def _generate_form(path, obj, actions):
    form_inputs = []

    for property in obj.properties:

        if property.type is 'image':  # Za sliku se unosi string, a ne prikazuje se!
            render = _get_template("text.html", o=obj, prop=property, type=property.type.name)
            form_inputs.append(render)
        else:
            render = _generate_basic(obj, property)
            form_inputs.append(render)
    form_name = obj.name + "_form"
    route = _get_route(form_name, True)
    file = _get_file(path, form_name)
    rendered = _get_template("form.html", formInputs=form_inputs, obj=obj, actions=actions)

    print(rendered, file=file)
    return '<div ui-view=\'' + form_name + '\'/>'

def _distinct_meta_objects(obj):
    distinct_meta = []
    if obj.meta:
        for m in obj.meta:
            if m.object not in distinct_meta:
                distinct_meta.append(m.object)
    return distinct_meta


def form_fk_property(meta, fk_item, fk_properties, multiple):
    if multiple:
        fk_item = "fk_item"
    result = ""
    for fkp in fk_properties:
        fk_property = "{{{{ ctrl_page.loadFK_{0}({1}).{2} }}}}" \
            .format(meta.object.name, fk_item, fkp.property.name)
        # wrap in <a>
        if fkp.page:
            anchor_name = fkp.linkText if fkp.linkText else fk_property
            fk_property = "<a href=\"#/{0}/{{{{{1}}}}}\">{2}</a>".format(fkp.page.name, fk_item, anchor_name)

        # save property in result
        result = fk_property if result == "" else "{0}, {1}".format(result, fk_property)

    result = "<h4>{0}</h4>".format(result)
    return result
