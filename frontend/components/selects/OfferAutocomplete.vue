<template>
  <v-container>
    <v-menu offset-y close-on-content-click>
      <template v-slot:activator="{ on }">
        <v-responsive min-width="300" width="500">
          <v-text-field
            v-model="search"
            :label="label"
            outlined
            clearable
            :error-messages="errorMessages"
            v-on="on"
            @click:clear="give(null)"
          />
        </v-responsive>
      </template>

      <v-card min-width="300">
        <v-card-text>
          <v-progress-linear v-if="loading" indeterminate />
          <v-virtual-scroll v-else-if="entries.length" :items="entries" height="300" item-height="64">
            <template v-slot:default="{ item }">
              <v-list-item v-if="item" :key="item.id" @click="give(item)">
                <v-list-item-title> {{ item.id }}. {{ item.name }} </v-list-item-title>
              </v-list-item>
              <v-divider></v-divider>
            </template>
          </v-virtual-scroll>
          <v-alert v-else-if="entries.length === 0" type="warning">No hay ofertas</v-alert>
        </v-card-text>
      </v-card>
    </v-menu>
  </v-container>
</template>

<script>
export default {
  props: {
    value: {
      type: Number,
      default: null,
    },
    label: {
      type: String,
      default: 'Oferta',
    },
    returnObject: {
      type: Boolean,
      default: false,
    },
    errorMessages: {
      type: Array,
      default: () => [],
    },
    defaultItems: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      entries: [...this.defaultItems],
      loading: false,
      model: this.value,
      search: (this.defaultItems.find((e) => e === this.value || (e && e.id === this.value)) || {}).name || '',
    }
  },
  watch: {
    async search(val) {
      if (!val || typeof val !== 'string' || this.loading) return
      this.loading = true
      try {
        const res = await this.$axios.$get(
          `calculator/offers/?search=${val}&fields=id,name,tarif,company&calculator=true`,
        )
        this.entries = res
      } catch (err) {
        this.$toast.error(err.response && err.response.data ? JSON.stringify(err.response.data) : err)
      } finally {
        this.loading = false
      }
    },
  },
  methods: {
    give(newOffer) {
      console.log(newOffer)
      this.model = newOffer
      this.search = newOffer ? newOffer.name : ''
      this.$emit('input', newOffer ? newOffer.id : null)
    },
  },
}
</script>
