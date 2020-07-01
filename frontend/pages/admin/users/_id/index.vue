<template>
  <v-card>
    <v-card-title>
      {{ fullname }}
    </v-card-title>

    <v-card-text>
      <v-row>
        <v-col>
          <v-list three-line subheader nav shaped>
            <v-subheader inset>Bids</v-subheader>

            <v-list-item
              v-for="bid in user.bids"
              :key="bid.id"
              nuxt
              :to="`/bids/${bid.id}`"
            >
              <v-list-item-content>
                <v-list-item-title v-text="bid.offer_name" />
                <v-list-item-subtitle v-text="'id: ' + bid.id" />
                <v-list-item-subtitle v-text="bid.created_at" />
              </v-list-item-content>

              <v-list-item-content>
                {{ bid.status }}
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  async asyncData({ params, $axios }) {
    const user = await $axios.$get(`/users/users/${params.id}/`)
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
