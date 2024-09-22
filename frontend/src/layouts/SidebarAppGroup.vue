<template>
  <q-expansion-item
    expand-separator
    :label="label"
    :icon="icon"
    :caption="caption"
    class="text-weight-bold text-uppercase"
    style="color: grey"
  >
    <q-item v-for="link in links" :key="link.text" :to="link.link" v-ripple clickable>
      <q-item-section avatar>
        <q-icon color="grey" :name="link.icon" />
      </q-item-section>
      <q-item-section>
        <q-item-label>{{ link.text }}</q-item-label>
      </q-item-section>
    </q-item>
  </q-expansion-item>
</template>


<script setup>
defineProps({
  label: {
    type: String,
    default: 'Links',
  },
  icon: {
    type: String,
    default: 'star',
  },
  caption: {
    type: String,
    default: '',
  },
  links: {
    type: Array,
    default: () => [
      {
        text: 'SampleApp',
        icon: 'star',
        link: '/NotFound',
      }
    ],
  },
})

</script>

<script>
export default {
  name: 'SidebarAppGroup',
}
</script>


<style scoped>

</style>
