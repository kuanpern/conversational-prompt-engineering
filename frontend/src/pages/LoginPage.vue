<template>
  <div class="fit row wrap justify-center items-start content-start" style="padding: 20px;">

    <q-card class="text-center" style="max-width: 400px; min-width: 300px;" flat bordered>
      <q-card-section class="text-h6 text-weight-bold">
        <q-icon name="mdi-account-circle" />
        Sundial
      </q-card-section>

      <q-card-section class="text-weight-bold">
        AI Assistant
      </q-card-section>
      <q-card-section>
        <q-img src="~src/assets/images/sundial-logo.png" style="width: 200px" />
      </q-card-section>

      <q-card-section>
        <q-btn unelevated class="full-width" color="primary" label="Login with Google" icon="mdi-google"
          @click="oauth_login('google')" />
        <!-- Other sign-in method not supported yet
        <q-btn unelevated class="full-width q-mt-sm" color="secondary" label="Login with Github" icon="mdi-github"
          @click="oauth_login('github')" />
        <q-btn unelevated class="full-width q-mt-sm" color="secondary" label="Login with Okta" icon="task_alt"
          @click="oauth_login('okta')" />
        <q-btn unelevated class="full-width q-mt-sm" color="secondary" label="Login with Email" icon="mdi-email"
          @click="manual_login()" />
        -->
      </q-card-section>
      <q-card-actions>
        <q-btn flat color="primary" label="Can't login?" @click="email_maintainer" />
      </q-card-actions>
    </q-card>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from 'src/stores/user-store';
import { maintainer_email, login_url, manual_login_url } from './variables.js';

const router = useRouter();

const email_maintainer = () => {
  const subject = "Sundial: Can't login";
  const body = "Hi,\n\nI can't login to Sundial. Please help.\n\nThanks,\n\n";
  const mailto_link = "mailto:" + maintainer_email + "?subject=" + subject + "&body=" + body;
  window.open(mailto_link, "emailWindow");
};

const user = useUserStore();

// backend implementation dependent
const oauth_login = (provider) => {
  // redirect to backend oauth endpoint
  const redirect_uri = login_url + '/' + provider;
  // redirect to backend oauth endpoint
  window.location.replace(redirect_uri);
};

// login with username and password
// applies for local login
const manual_login = () => {
  window.location.replace(manual_login_url);
};


onMounted(() => {
  if (user.isLoggedIn) {
    router.push('/Home');
  }
});
</script>

<script>
export default {
  name: 'LoginPage',
}
</script>

<style scoped></style>

