<template>
  <v-card>
    <v-card-text>
      <admin-header />
    </v-card-text>

    <v-card-title>
      {{ fullname }}
    </v-card-title>

    <v-card-text>
      {{ user }}
    </v-card-text>

    <chat v-if="participant" :participant="participant" />
  </v-card>
</template>

<script>
export default {
  components: {
    AdminHeader: () => import('~/components/admin/AdminHeader'),
    Chat: () => import('~/components/chat/Chat'),
  },
  async asyncData({ params, $axios }) {
    const user = await $axios.$get(`/users/leeds/${params.id}/`)
    const participant = {
      id: user.id,
      name: user.email,
      imageUrl: user.avatar || '',
    }
    return {
      user,
      participant,
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
