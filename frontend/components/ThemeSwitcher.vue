<template>
  <v-btn icon @click="switchTheme">
    <v-icon>
      mdi-theme-light-dark
    </v-icon>
  </v-btn>
</template>

<script>
export default {
  name: 'ThemeSwitcher',
  async created() {
    this.$vuetify.theme.isDark =
      JSON.parse(localStorage.getItem('isDark')) || false
  },
  methods: {
    async switchTheme() {
      const isDark = this.$vuetify.theme.isDark
      this.$vuetify.theme.isDark = !isDark
      localStorage.setItem('isDark', JSON.stringify(!isDark))
    },
  },
}
</script>
