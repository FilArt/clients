<template>
  <v-card>
    <v-toolbar>
      <v-toolbar-title>
        <v-btn icon color="error" @click="$router.back()">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        Prioridad de ofertas
      </v-toolbar-title>
    </v-toolbar>

    <v-card-text>
      <v-data-table :items="items" :headers="headers" :loading="loading">
        <template v-slot:top>
          <v-toolbar>
            <v-toolbar-items>
              <edit-priority-offer @update="refresh" />
            </v-toolbar-items>
          </v-toolbar>
        </template>

        <template v-slot:item.actions="{ item }">
          <edit-priority-offer updating :offer="item" @update="refresh" />
          <delete-button @click="deleteOffer(item)" />
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>
<script>
import DeleteButton from '../../../components/buttons/deleteButton.vue'
import EditPriorityOffer from '../../../components/dialogs/EditPriorityOffer.vue'
export default {
  components: { EditPriorityOffer, DeleteButton },
  data() {
    return {
      items: [],
      headers: [
        {
          text: 'ID',
          value: 'id',
        },
        {
          text: 'Tipo',
          value: 'kind',
        },
        {
          text: 'Tarifa',
          value: 'tarif',
        },
        {
          text: 'Consumo min',
          value: 'consumption_min',
        },
        {
          text: 'Consumo max',
          value: 'consumption_max',
        },
        {
          text: 'Potencia min',
          value: 'power_min',
        },
        {
          text: 'Potencia max',
          value: 'power_max',
        },
        {
          text: 'Primero',
          value: 'first_name',
        },
        {
          text: 'Segunda',
          value: 'second_name',
        },
        {
          text: 'Tercera',
          value: 'third_name',
        },
        {
          text: '',
          value: 'actions',
        },
      ],
      // errorMessages: {},
      loading: false,
    }
  },
  async mounted() {
    await this.refresh()
  },
  methods: {
    async refresh() {
      this.loading = true
      this.items = await this.$axios.$get(`calculator/priority_offers/`)
      this.loading = false
    },
    async updateOffer() {},
    async deleteOffer(offer) {
      const isDelete = await this.$swal({
        title: `Eliminar prioridad de ofertas ${offer.id}?`,
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      })
      if (!isDelete) return
      await this.$axios.$delete(`calculator/priority_offers/${offer.id}/`)
      await this.refresh()
    },
  },
}
</script>
