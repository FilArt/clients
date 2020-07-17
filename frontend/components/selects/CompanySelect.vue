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
    style="min-width: 150px;"
    @input="$emit('input', company)"
  >
    <template v-if="hint" v-slot:append-outer>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn v-on="on" icon color="info" v-bind="attrs">
            <v-icon>
              mdi-information
            </v-icon>
          </v-btn>
        </template>
        <span>
          Elija la empresa comercializadora con la que está actualmente.
        </span>
      </v-tooltip>
    </template>
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
      <v-row align="center">
        <v-col class="flex-grow-0">
          <v-avatar>
            <v-img v-if="item['logo']" :src="item['logo']" />
            <v-icon v-else>mdi-cancel</v-icon>
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
          this.companies = companies.concat({
            id: null,
            name: 'OTRA',
          })
        })
        .finally(() => (this.loading = false))
    },
  },
}
</script>
