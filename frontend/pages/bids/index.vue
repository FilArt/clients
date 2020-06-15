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
        <v-list nav>
          <v-list-item>
            <v-list-item-subtitle>№</v-list-item-subtitle>

            <v-list-item-title>
              Created at
            </v-list-item-title>

            <v-list-item-title>
              Offer
            </v-list-item-title>

            <v-list-item-title>
              Status
            </v-list-item-title>
          </v-list-item>

          <v-list-item
            v-for="bid in (status ? bids.filter(b => b.status === status) : bids)"
            :key="bid.id"
            :to="`/bids/${bid.id}`"
            link
          >
            <v-list-item-subtitle>{{ bid.id }}</v-list-item-subtitle>

            <v-list-item-title>
              {{ bid.created_at }}
            </v-list-item-title>

            <v-list-item-title>
              {{ bid.offer_name }}
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
    const data = await $axios.$get('bids/')
    return { bids: data }
  },
}
</script>
