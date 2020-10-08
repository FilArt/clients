<template>
  <v-autocomplete
    v-model="company"
    :items="companies"
    :loading="loading"
    :error-messages="errorMessages"
    :label="label"
    item-text="name"
    item-value="id"
    chips
    deletable-chips
    dense
    style="min-width: 150px"
    @input="$emit('input', company)"
  >
    <template v-if="hint" v-slot:append-outer>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon color="#004680" v-bind="attrs" v-on="on">
            <v-icon> mdi-information </v-icon>
          </v-btn>
        </template>
        <span> Elija la empresa comercializadora con la que está actualmente. </span>
      </v-tooltip>
    </template>
    <template v-slot:selection="{ item }">
      <v-chip close @click:close="closeItem">
        <v-avatar>
          <v-img v-if="item['logo']" :src="item['logo']" />
          <v-icon v-else> mdi-cancel </v-icon>
        </v-avatar>
        {{ item.name }}
      </v-chip>
    </template>
    <template v-slot:item="{ item }">
      <v-row align="center">
        <v-col class="flex-grow-0">
          <v-avatar>
            <v-img v-if="item['logo']" :src="item['logo']" />
            <v-icon v-else> mdi-cancel </v-icon>
          </v-avatar>
        </v-col>

        <v-col>{{ item.name }}</v-col>
      </v-row>
    </template>
  </v-autocomplete>
</template>

<script>
export default {
  name: 'CompanySelect',
  props: {
    withoutOther: {
      type: Boolean,
      default: false,
    },
    hint: {
      type: Boolean,
      default: false,
    },
    label: {
      type: String,
      default: 'Comercializadora',
    },
    value: {
      type: [Number, String],
      default: 0,
    },
    errorMessages: {
      type: Array,
      default: () => null,
    },
  },
  data() {
    return {
      loading: false,
      company: this.value,
    }
  },
  computed: {
    companies() {
      const comps = this.$store.state.companies
      return this.withoutOther ? comps.filter((c) => c.name !== 'OTRA') : comps
    },
  },
  watch: {
    value: {
      handler(val) {
        this.company = !val ? null : this.companies.find((c) => c.id.toString() === val.toString())
      },
      deep: false,
    },
  },
  async mounted() {
    if (!this.companies.length) await this.$store.dispatch('fetchCompanies')
  },
  methods: {
    closeItem() {
      this.company = null
      this.$emit('input', null)
    },
  },
}
</script>
