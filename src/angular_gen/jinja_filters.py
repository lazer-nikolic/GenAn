def sub_routes_filter(routes):
    if routes is not None:
        all_sub_routes = routes['sub_routes']
        for sub_route in routes['sub_routes']:
            all_sub_routes += sub_routes_filter(sub_route)
    else:
        all_sub_routes = []
    return all_sub_routes


if __name__ == '__main__':
    sub_route = {'sub_routes': [
        {
            'sub_routes': [
            {
                'sub_routes': [

            ],
                'template': 'app/views/articles_list/articles_list.html',
                'path': '/articles_list',
                'name': 'articles_list',
                'controller': 'articles_list'
            },
            {
            'sub_routes': [
                {
                'sub_routes': [

                ],
                    'template': 'app/views/articles_list/articles_list.html',
                    'path': '/articles_list',
                    'name': 'articles_list',
                    'controller': 'articles_list'
                }
            ],
                'template': 'app/views/articles_list/articles_list.html',
                'path': '/articles_list',
                'name': 'articles_list',
                'controller': 'articles_list'
            }
            ],
            'template': 'app/views/articles_list/articles_list.html',
            'path': '/articles_list',
            'name': 'articles_list',
            'controller': 'articles_list'}
    ],
        'template': 'app/views/articles_for_user/articles_for_user.html', 'path': '/articles_for_user',
        'name': 'articles_for_user', 'controller': 'articles_for_user'}

    test = sub_routes_filter(sub_route)
    print(test)
