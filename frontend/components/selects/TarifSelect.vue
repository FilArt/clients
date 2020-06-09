<template>
  <v-autocomplete
    v-model="tarif"
    :items="tarifs"
    :loading="loading"
    :error-messages="errorMessages"
    label="Tarif"
    @input="$emit('input', tarif)"
  />
</template>

<script>
export default {
  name: 'TarifSelect',
  props: {
    errorMessages: {
      type: Array,
      default: () => null
    }
  },
  data() {
    return {
      loading: true,

      tarif: null,
      tarifs: []
    }
  },
  mounted() {
    this.refresh()
  },
  methods: {
    refresh() {
      this.loading = true
      this.$axios
        .$get('/calculator/tarifs/')
        .then(tarifs => {
          this.tarifs = tarifs
        })
        .finally(() => (this.loading = false))
    }
  }
}
</script>
