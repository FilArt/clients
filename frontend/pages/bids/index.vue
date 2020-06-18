<template>
  <v-card>
    <v-alert v-if="bids.length === 0">
      No bids so far.
    </v-alert>

    <div v-else>
      <v-card-title>
        <p class="flex-grow-1">Bids</p>
        <status-select v-model="status" multiple />
      </v-card-title>

      <v-card-text>
        <v-list nav shaped subheader>
          <v-list-item>
            <v-col>
              <small>
                №
              </small>
            </v-col>

            <v-list-item v-for="header in headers" :key="header.value">
              {{ header.text }}
            </v-list-item>
          </v-list-item>

          <v-list-item
            v-for="bid in (status ? bids.filter(b => b.status === status) : bids)"
            :key="bid.id"
            :to="`/bids/${bid.id}`"
            link
          >
            <v-col>
              <small> {{ bid.id }} </small>
            </v-col>

            <v-list-item-title>
              {{ bid.offer_name }}
            </v-list-item-title>

            <v-list-item-title>
              {{ bid.created_at }}
            </v-list-item-title>

            <v-list-item-title>
              {{ bid.status }}
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-card-text>

      <go-up-button />
    </div>
  </v-card>
</template>

<script>
import ClientTypeSelect from '~/components/selects/ClientTypeSelect'
import StatusSelect from '~/components/selects/StatusSelect'
import GoUpButton from '~/components/buttons/goUpButton'
export default {
  components: { GoUpButton, StatusSelect, ClientTypeSelect },
  data() {
    return {
      status: null,
    }
  },
  async asyncData({ $axios }) {
    const bids = await $axios.$get('bids/')
    const headers = await $axios.$get('bids/headers/')
    return { bids, headers }
  },
}
</script>
