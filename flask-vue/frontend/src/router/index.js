import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";
import BabyShark from "../components/Shark.vue";
import Games from "../components/Games.vue";
import ProdHours from "../components/ProdHours.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  {
    path: "/prediction",
    name: "prediction",
    component: BabyShark,
  },
  {
    path: "/games",
    name: "GamesLib",
    component: Games,
  },
  {
    path: "/prod",
    name: "ProdHours",
    component: ProdHours,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
