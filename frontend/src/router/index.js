import { route } from 'quasar/wrappers'
import { createRouter, createMemoryHistory, createWebHistory, createWebHashHistory } from 'vue-router'
import { useUserStore } from 'src/stores/user-store.js'
import { Cookies } from 'quasar'
import routes from './routes'

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory)

  // check if to.name is included in candidates (for auth guard exclusions)
  const is_included = (to, candidates) => {
    let det = false;
    candidates.forEach((c) => {
      if (to.name === c) {
        det = true;
        return det;
      }
    });
    return det;
  } // end is_included

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.VUE_ROUTER_BASE)
  });

  // auth guard (implement for all routes for now)
  const exclude_route_names = ['Login', 'Redirect'];
  Router.beforeEach(async (to, from) => {

    // disable authentication
    if (process.env.DISABLE_AUTH === 'true'){
      return true;
    } // end if
    

    // get user store
    const store = useUserStore();

    // if user is not logged in and is requesting a protected routes
    if ((!store.isLoggedIn) && (!is_included(to, exclude_route_names))) {
      // redirect the user to the login page
      return { name: 'Login', query: { redirect: to.fullPath }};
    } // end if

    // set lastpath cookie (for redirect after login)
    if (!is_included(to, exclude_route_names)) {
      Cookies.set('lastpath', to.fullPath);
    }
  })
  return Router
})
