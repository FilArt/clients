<template>
  <v-autocomplete
    v-model="offer"
    :items="offers"
    :loading="loading"
    :label="label"
    :return-object="returnObject"
    item-value="id"
    style="min-width: 150px"
    @input="$emit('input', offer)"
  >
    <template v-slot:selection="{ item }">
      <v-row class="align-center">
        <v-col>
          <v-list-item-avatar>
            <v-img :src="item.company_logo"></v-img>
          </v-list-item-avatar>
          {{ item.name }}
        </v-col>
        <v-col>
          <v-chip x-small>Consumo: {{ item.consumption_min }} kW/año - {{ item.consumption_max }} kW/año </v-chip>
          <v-chip v-if="item.power_max" x-small> Potencia: {{ item.power_min }} kW - {{ item.power_max }} kW </v-chip>
          <v-chip x-small>Tarif: {{ item.tarif }}</v-chip>
          <v-chip x-small>Tipo de precio: {{ item.is_price_permanent }}</v-chip>
          <v-chip x-small>
            {{ item.client_type === 0 ? 'Fisico' : item.client_type === 1 ? 'Juridico' : 'Autónomo' }}
          </v-chip>
        </v-col>
      </v-row>
    </template>
    <template v-slot:item="{ item }">
      <v-row class="align-center">
        <v-col>
          <v-list-item-avatar>
            <v-img :src="item.company_logo"></v-img>
          </v-list-item-avatar>
          {{ item.name }}
        </v-col>
        <v-col>
          <v-chip x-small>Consumo: {{ item.consumption_min }} kW/año - {{ item.consumption_max }} kW/año </v-chip>
          <v-chip v-if="item.power_max" x-small> Potencia: {{ item.power_min }} kW - {{ item.power_max }} kW </v-chip>
          <v-chip x-small>Tarif: {{ item.tarif }}</v-chip>
          <v-chip x-small>Tipo de precio: {{ item.is_price_permanent }}</v-chip>
          <v-chip x-small>
            {{ item.client_type === 0 ? 'Fisico' : item.client_type === 1 ? 'Juridico' : 'Autónomo' }}
          </v-chip>
        </v-col>
      </v-row>
    </template>
  </v-autocomplete>
</template>

<script>
import qs from 'qs'
import constants from '@/lib/constants'
export default {
  name: 'OfferSelect',
  props: {
    returnObject: {
      type: Boolean,
      default: true,
    },
    label: {
      type: String,
      default: 'Ofertas',
    },
    company: {
      type: Number,
      default: null,
    },
    clientType: {
      type: [String, Number],
      default: null,
    },
    tarif: {
      type: String,
      default: null,
    },
    kind: {
      type: String,
      default: null,
    },
    consumo: {
      type: Number,
      default: null,
    },
    p1: {
      type: Number,
      default: null,
    },
    p2: {
      type: Number,
      default: null,
    },
    p3: {
      type: Number,
      default: null,
    },
    p4: {
      type: Number,
      default: null,
    },
    p5: {
      type: Number,
      default: null,
    },
    p6: {
      type: Number,
      default: null,
    },
    value: {
      type: [Number, Object],
      default: () => null,
    },
  },
  data() {
    return {
      loading: false,
      offer: this.value,
      offers: [],
    }
  },
  watch: {
    kind() {
      this.refresh()
    },
    company() {
      this.refresh()
    },
    clientType() {
      this.refresh()
    },
    tarif() {
      this.refresh()
    },
    consumo() {
      this.refresh()
    },
    p1() {
      this.refresh()
    },
    p2() {
      this.refresh()
    },
    p3() {
      this.refresh()
    },
    p4() {
      this.refresh()
    },
    p5() {
      this.refresh()
    },
    p6() {
      this.refresh()
    },
  },
  async mounted() {
    await this.refresh()
  },
  methods: {
    async refresh() {
      this.loading = true
      const obj = {
        company: this.company,
        client_type: this.clientType,
        tarif: this.tarif,
        kind: this.kind,
        p1: this.p1,
        p2: this.p2,
        p3: this.p3,
        p4: this.p4,
        p5: this.p5,
        p6: this.p6,
        active: true,
      }
      if (this.consumo) obj.consumption_min__lte = this.consumo
      if (this.consumo) obj.consumption_max__gte = this.consumo
      const cleanObj = constants.cleanEmpty(obj)
      const getParamsString = qs.stringify(cleanObj)
      this.offers = await this.$axios.$get(`calculator/offers/?${getParamsString}`)
      if (!this.offer && this.value) {
        this.offer = this.offers.find((o) => {
          console.log(o.id, this.value)
          if (this.value instanceof Number) {
            o.id === this.value
          } else {
            o.id === this.value.id
          }
        })
      }
      this.loading = false
    },
  },
}
</script>
