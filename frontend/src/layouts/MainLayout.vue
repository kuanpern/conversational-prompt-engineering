<template>
  <q-layout view="hHh lpR fFf">

    <!-- HEADER -->
    <q-header bordered class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          <!-- go to homepage -->
          <q-avatar
            size="md"
            square
            class="cursor-pointer"
            @click="$router.push('/Home')">
          </q-avatar>
        </q-toolbar-title>

        <span v-if="!user.isLoggedIn">
          <q-btn flat @click="sign_in">
            Sign In
            <q-avatar size="md">
              <q-icon name="login" />
            </q-avatar>
          </q-btn>
        </span>

        <q-btn dense flat round @click="toggleRightDrawer">
          <template v-if="user.isLoggedIn">
            <q-avatar size="md">
              <img :src="user.picture" />
            </q-avatar>
          </template>
          <template v-else>
            <q-avatar size="md">
              <q-icon name="account_circle" />
            </q-avatar>
          </template>
        </q-btn>
      </q-toolbar>
    </q-header>
    <!-- END HEADER -->


    <!-- LEFT DRAWER -->
    <q-drawer show-if-above v-model="leftDrawerOpen" side="left" overlay bordered>
      <q-scroll-area class="fit">
        <q-list padding>

          <!-- PAGES -->
          <q-item v-for="link in links_pages" :key="link.text" :to="link.link" v-ripple link clickable>
            <q-item-section avatar>
              <q-icon color="grey" :name="link.icon" />
            </q-item-section>
            <q-item-section
              class="text-weight-bold text-uppercase"
              style="color: grey"
            >
              <q-item-label>{{ link.text }}</q-item-label>
            </q-item-section>
          </q-item>

          <q-separator />

          <sidebar-app-group label="CPE" icon="maps_ugc"
           :links="links_cpe"/>


        </q-list>
      </q-scroll-area>
    </q-drawer>


    <!-- RIGHT DRAWER -->
    <q-drawer v-model="rightDrawerOpen" side="right" overlay elevated>
      <q-scroll-area class="fit">
        <q-list padding>

          <!-- User Account Information -->
          <q-item v-if="user.isLoggedIn">
            <q-item-section avatar>
              <q-avatar>
                <img :src="user.picture" />
              </q-avatar>
            </q-item-section>
            <q-item-section>
              {{ user.name }} <br> {{ user.email }}
            </q-item-section>
          </q-item>
          <q-separator class="q-my-md" />

          <q-item v-for="link in links_preferences" :key="link.text" :to="link.link" v-ripple clickable>
            <q-item-section avatar>
              <q-icon color="grey" :name="link.icon" />
            </q-item-section>
            <q-item-section>
              <q-item-label>{{ link.text }}</q-item-label>
            </q-item-section>
          </q-item>

          <!-- SIGN OUT -->
          <q-item v-ripple clickable @click="sign_out">
            <q-item-section avatar>
              <q-icon color="grey" name="mdi-logout" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Sign out</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-scroll-area>

    </q-drawer>

    <q-page-container>
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </q-page-container>

  </q-layout>
</template>


<script setup>
import { ref } from 'vue'
import { useUserStore } from "src/stores/user-store";
import { useRoute, useRouter } from 'vue-router';
import SidebarAppGroup from './SidebarAppGroup.vue';
import {
  links_pages, links_preferences, links_cpe,
} from './variables.js';
import { logout_url } from '../pages/variables.js';

import { useQuasar } from 'quasar';
const $q = useQuasar();
const isDialogOpen = ref(true);

const router = useRouter();
const route = useRoute();
const user = useUserStore();

// handle login callback
const sign_in = () => {
  router.push('/Login');
};

const sign_out = () => {
  user.logout();
  // go to the logout endpoint
  window.location.href = logout_url;
  // redirect to the homepage
  router.push('/Home');
  // close the right drawer
  rightDrawerOpen.value = false;
};


const leftDrawerOpen  = ref(false);
const toggleLeftDrawer = () => {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
const rightDrawerOpen = ref(false);
const toggleRightDrawer = () => {
  rightDrawerOpen.value = !rightDrawerOpen.value
}


</script>



<style scoped>
.q-header {
  background-color: ghostwhite !important;
}

.q-header .q-btn {
  color: black !important;
}


</style>
