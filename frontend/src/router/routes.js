// import from subroute files
import static_page_routes from './subroutes/static-pages.js';
import cpe_routes from './subroutes/cpe.js';

// combine routes
const paths = [
  ...static_page_routes,
  ...cpe_routes,
];

// Default routes
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      ... paths,
    ]
  },
  {
    path: '/Login',
    name: 'Login',
    component: () => import('pages/LoginPage.vue'),
    meta: {title: 'Login'},
  },
  {
    path: '/Redirect',
    name: 'Redirect',
    component: () => import('pages/RedirectPage.vue'),
    meta: {title: 'Redirect'},
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  }
]

export default routes
