<template>
  <v-autocomplete
    v-model="company"
    :items="companies"
    :loading="loading"
    :error-messages="errorMessages"
    label="Comercializadora"
    item-text="name"
    item-value="id"
    @input="$emit('input', company)"
  >
    <template v-slot:selection="{ item }">
      <v-avatar>
        <v-img v-if="item['logo']" :src="item['logo']" />
        <v-icon v-else>mdi-cancel</v-icon>
      </v-avatar>
      {{ item.name }}
    </template>
    <template v-slot:item="{ item }">
      <v-avatar>
        <v-img v-if="item['logo']" :src="item['logo']" />
        <v-icon v-else>mdi-cancel</v-icon>
      </v-avatar>
      {{ item.name }}
    </template>
  </v-autocomplete>
</template>

<script>
export default {
  name: 'CompanySelect',
  props: {
    errorMessages: {
      type: Array,
      default: () => null
    }
  },
  data() {
    return {
      loading: true,

      company: null,
      companies: []
    }
  },
  mounted() {
    this.refresh()
  },
  methods: {
    refresh() {
      this.loading = true
      this.$axios
        .$get('/calculator/companies/')
        .then(companies => {
          this.companies = companies
        })
        .finally(() => (this.loading = false))
    }
  }
}
</script>
