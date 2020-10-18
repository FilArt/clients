<template>
  <v-card>
    <v-toolbar>
      <v-toolbar-title class="flex-grow-1">Añadir nuevo solicitud</v-toolbar-title>

      <v-toolbar-items>
        <v-btn color="error" icon @click="$emit('close')">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>

    <v-form @submit.prevent="submit">
      <v-card-text>
        <select-offer v-model="offer" label="Elejir oferta" />
      </v-card-text>

      <v-card-actions>
        <submit-button :disabled="!offer || !offer.id" label="Enviar" block />
      </v-card-actions>
    </v-form>
  </v-card>
</template>

<script>
import SubmitButton from '@/components/buttons/submitButton'
import SelectOffer from '@/components/selects/SelectOffer'
export default {
  name: 'AddNewBid',
  components: { SelectOffer, SubmitButton },
  props: {
    userId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      offer: null,
    }
  },
  methods: {
    async submit() {
      try {
        await this.$axios.$post('bids/bids/', { user: this.userId, offer: this.offer.id })
        this.$emit('bid-added')
      } catch (e) {
        console.error(e)
        await this.$swal({ title: 'Error', text: e.response.data, icon: 'error' })
      }
    },
  },
}
</script>
