<template>
  <v-autocomplete
    v-model="company"
    :items="companies"
    :loading="loading"
    :error-messages="errorMessages"
    label="Comercializadora"
    item-text="name"
    item-value="id"
    dense
    @input="$emit('input', company)"
  >
    <template v-slot:selection="{ item }">
      <v-chip close @click:close="closeItem">
        <v-avatar>
          <v-img v-if="item['logo']" :src="item['logo']" />
          <v-icon v-else>mdi-cancel</v-icon>
        </v-avatar>
        {{ item.name }}
      </v-chip>
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
    value: {
      type: Number,
      default: 0,
    },
    errorMessages: {
      type: Array,
      default: () => null,
    },
  },
  data() {
    return {
      loading: true,

      company: this.value,
      companies: [],
    }
  },
  watch: {
    value: {
      handler: function (val) {
        this.company = this.companies.find((c) => c.id === val)
      },
      deep: false,
    },
  },
  mounted() {
    this.refresh()
  },
  methods: {
    closeItem() {
      this.company = null
      this.$emit('input', null)
    },
    refresh() {
      this.loading = true
      this.$axios
        .$get('/calculator/companies/')
        .then((companies) => {
          this.companies = companies
        })
        .finally(() => (this.loading = false))
    },
  },
}
</script>
