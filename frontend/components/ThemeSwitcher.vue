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
    console.log(this)
    const settings = this.$auth.user.settings
    let isDark = true
    if (settings && settings.hasOwnProperty('dark_theme')) {
      isDark = settings.dark_theme
    }
    this.$vuetify.theme.isDark = isDark
  },
  methods: {
    async switchTheme() {
      const isDark = this.$vuetify.theme.isDark
      const newTheme = !isDark
      this.$vuetify.theme.isDark = newTheme
      await this.$axios.$patch(`users/account/${this.$auth.user.id}/`, {
        settings: {
          dark_theme: newTheme,
        },
      })
    },
  },
}
</script>
