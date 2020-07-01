<template>
  <v-card>
    <v-card-title>
      {{ fullname }}
    </v-card-title>

    <v-card-text>
      {{ user }}
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  async asyncData({ params, $axios }) {
    const user = await $axios.$get(`/users/leeds/${params.id}/`)
    return {
      user,
    }
  },
  computed: {
    fullname() {
      const u = this.user
      let fullname = [u.first_name, u.last_name]
        .filter((name) => !!name)
        .join(' ')
        .trim()
      return fullname && fullname.length ? fullname : u.email
    },
  },
}
</script>
