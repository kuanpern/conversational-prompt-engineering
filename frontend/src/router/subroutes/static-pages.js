import HomePage from "src/pages/HomePage.vue";

export default [
  {
    path: "/index.html",
    name: "IndexPage",
    component: HomePage,
    meta: { title: "Index" },
  },
  {
    path: "/Home",
    name: "HomePage",
    component: HomePage,
    meta: { title: "Home" },
  },
];
