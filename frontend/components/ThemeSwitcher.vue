<template>
  <v-btn color="primary" icon @click="switchTheme">
    <v-icon> mdi-theme-light-dark </v-icon>
  </v-btn>
</template>

<script>
export default {
  name: 'ThemeSwitcher',
  async created() {
    const { settings } = this.$auth.user
    let isDark = true
    if (settings && settings.dark_theme !== undefined) {
      isDark = settings.dark_theme
    }
    this.$vuetify.theme.isDark = isDark
  },
  methods: {
    async switchTheme() {
      const newTheme = !this.$vuetify.theme.isDark
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
