<template>
  <v-autocomplete
    v-model="tarif"
    :items="tarifs"
    :loading="loading"
    :error-messages="errorMessages"
    label="Tarif"
    dense
    chips
    deletable-chips
    @input="$emit('input', tarif)"
  />
</template>

<script>
export default {
  name: 'TarifSelect',
  props: {
    value: {
      type: String,
      default: null,
    },
    errorMessages: {
      type: Array,
      default: () => null,
    },
  },
  data() {
    return {
      loading: true,

      tarif: this.value,
      tarifs: [],
    }
  },
  watch: {
    value(val) {
      this.tarif = val
    },
  },
  mounted() {
    this.refresh()
  },
  methods: {
    refresh() {
      this.loading = true
      this.$axios
        .$get('/calculator/tarifs/')
        .then((tarifs) => {
          this.tarifs = tarifs
        })
        .finally(() => (this.loading = false))
    },
  },
}
</script>
