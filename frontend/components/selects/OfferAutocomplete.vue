<template>
  <v-autocomplete
    v-model="model"
    :items="entries"
    :loading="isLoading"
    :search-input.sync="search"
    hide-no-data
    hide-selected
    item-text="name"
    item-value="id"
    :label="label"
    placeholder="Start typing to Search"
    prepend-icon="mdi-database-search"
    :return-object="returnObject"
    :error-messages="errorMessages"
    @input="$emit('input', $event)"
  >
    <template v-slot:item="{ item }">
      <v-list-item-content @click="model = item">
        <v-list-item-subtitle> ID: {{ item.id }} </v-list-item-subtitle>
        <v-list-item-subtitle> {{ item.tarif }} - {{ item.company }} </v-list-item-subtitle>
        <v-list-item-title>
          {{ item.name }}
        </v-list-item-title>
      </v-list-item-content>
    </template>
  </v-autocomplete>
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
      isLoading: false,
      model: this.value,
      search: null,
    }
  },
  watch: {
    async search(val) {
      if (typeof val !== 'string' || this.isLoading) return
      this.isLoading = true
      try {
        const res = await this.$axios.$get(`calculator/offers/?search=${val}&fields=id,name,tarif,company`)
        this.entries = res
      } catch (err) {
        this.$toast.error(err.response && err.response.data ? JSON.stringify(err.response.data) : err)
      } finally {
        this.isLoading = false
      }
    },
  },
}
</script>
