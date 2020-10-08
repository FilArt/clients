<template>
  <v-autocomplete
    v-model="offer"
    :items="offers"
    :loading="loading"
    label="Oferta"
    item-value="id"
    return-object
    chips
    deletable-chips
    style="min-width: 150px"
    @input="$emit('input', offer)"
  >
    <template v-slot:selection="{ item }">
      <v-chip close @click:close="closeItem">
        <v-avatar>
          <v-img v-if="item['company_logo']" :src="item['company_logo']" />
          <v-icon v-else> mdi-cancel </v-icon>
        </v-avatar>
        <v-col>
          <v-row>
            {{ item.name }}
          </v-row>
          <v-row>
            <i style="font-size: 10px">
              <span>Consumo: {{ item.consumption_min }} kW/año - {{ item.consumption_max }} kW/año.</span>
              <span>
                Tarif:
                {{ item.tarif }}
              </span>
            </i>
          </v-row>
        </v-col>
      </v-chip>
    </template>
    <template v-slot:item="{ item }">
      <v-row align="center">
        <v-col class="flex-grow-0">
          <v-avatar>
            <v-img v-if="item['company_logo']" :src="item['company_logo']" />
            <v-icon v-else> mdi-cancel </v-icon>
          </v-avatar>
        </v-col>

        <v-col>
          <v-row>
            {{ item.name }}
          </v-row>
          <v-row>
            <i style="font-size: 10px">
              <span>Consumo: {{ item.consumption_min }} kW/año - {{ item.consumption_max }} kW/año.</span>
              <span>
                Tarif:
                {{ item.tarif }}
              </span>
            </i>
          </v-row>
        </v-col>
      </v-row>
    </template>
  </v-autocomplete>
</template>

<script>
import constants from '@/lib/constants'
export default {
  name: 'OfferSelect',
  props: {
    company: {
      type: Number,
      default: null,
    },
    clientType: {
      type: String,
      default: null,
    },
    // consumo: {
    //   type: [String, Number],
    //   default: null,
    // },
    tarif: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      loading: true,
      offer: null,
      offers: [],
    }
  },
  watch: {
    company() {
      this.refresh()
    },
    clientType() {
      this.refresh()
    },
    tarif() {
      this.refresh()
    },
    // consumo() {
    //   this.refresh()
    // },
  },
  mounted() {
    this.refresh()
  },
  methods: {
    closeItem() {
      this.offer = null
      this.$emit('input', null)
    },
    refresh() {
      this.loading = true
      const params = Object.entries(
        constants.cleanEmpty({
          company: this.company,
          client_type: this.clientType,
          // consumption_min__lt: this.consumo,
          // consumption_max__gt: this.consumo,
          tarif: this.tarif,
        }),
      )
        .map((pair) => `${pair[0]}=${pair[1]}`)
        .join('&')

      this.$axios
        .$get(`calculator/offers/?name=&${params}`)
        .then((offers) => (this.offers = offers))
        .finally(() => (this.loading = false))
    },
  },
}
</script>
