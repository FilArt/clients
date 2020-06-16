<template>
  <v-card>
    <v-dialog v-model="submitDialog">
      <template v-slot:activator="{ on }">
        <v-btn
          v-on="on"
          fab
          x-large
          icon
          large
          fixed
          bottom
          right
          color="success"
        >
          <v-icon>mdi-check</v-icon>
        </v-btn>
      </template>

      <v-card>
        <v-card-title
          ><p class="flex-grow-1">Submit</p>
          <close-button @click="submitDialog = false" />
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="submit" novalidate>
            <status-select
              v-model="data.status"
              :errors="errorMessages.status"
            />
            <v-textarea v-model="data.message" label="Message" />

            <v-card-actions>
              <v-btn
                block
                type="submit"
                color="success"
                :disabled="!data.status || !data.message"
                >Listo
                <v-icon right>mdi-check</v-icon>
              </v-btn>
            </v-card-actions>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-card-title>Offer</v-card-title>
    <v-card-text>
      <detail-offer :offer="bid.offer" />
    </v-card-text>

    <v-card-title>Card</v-card-title>
    <v-card-text>
      <card-detail :card="bid.card" />
    </v-card-text>

    <v-card-title>Attachments</v-card-title>
    <v-card-text>
      <v-chip
        v-for="attachment in bid.card.attachments"
        :key="attachment.id"
        link
        exact
        target="_blank"
        :href="attachment.attachment"
      >
        Attachment {{ attachment.id }}
      </v-chip>
    </v-card-text>
  </v-card>
</template>

<script>
import DetailOffer from '~/components/detailOffer'
import CardDetail from '~/components/CardDetail'
import StatusSelect from '~/components/selects/StatusSelect'
import CloseButton from '~/components/buttons/closeButton'
export default {
  components: { CloseButton, StatusSelect, CardDetail, DetailOffer },
  async asyncData({ $axios, params }) {
    const bid = await $axios.$get(`bids/${params.id}`)
    return {
      bid,
    }
  },
  data() {
    return {
      submitDialog: false,
      data: {
        status: null,
        message: null,
      },
      errorMessages: { status: null, message: null },
    }
  },
  methods: {
    submit() {
      this.$axios
        .$post(`bids/${this.bid.id}/validate/`, this.data)
        .then((data) => {
          this.bid = data
          this.$swal({
            title: 'Submitted',
            icon: 'success',
          }).then(() => {
            this.submitDialog = false
          })
        })
        .catch((e) => (this.errorMessages = e.response.data))
    },
  },
}
</script>
