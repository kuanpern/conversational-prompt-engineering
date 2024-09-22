import { defineStore } from "pinia";
import axios from "axios";
import { user_info_url } from "../pages/variables.js";

export const useUserStore = defineStore("user", {
  state: () => ({
    user: null,
  }),

  getters: {
    isLoggedIn: (state) => state.user != null,
    data:    (state) => state.user,
    name:    (state) => state.user.name,
    email:   (state) => state.user.email,
    picture: (state) => state.user.picture,
    // uncomment for dev/debug: isLoggedIn: (state) => true,
  },

  actions: {
    setUser(user) {
      this.user = user;
    },
    logout() {
      this.user = null;
    },
    async login(callback) {
      // fetch user info from backend using axios, using cookies
      let _this = this;
      const res = axios.get(user_info_url,
        { withCredentials: true }
      ).then(function(response) {
        _this.setUser(response.data);
        callback();
      }).catch(function(error) {
        console.log(error);
        callback();
      });
    }
  },
});

