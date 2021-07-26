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
  },
  async mounted() {
    await this.refresh()
  },
  methods: {
    closeItem() {
      this.offer = null
      this.$emit('input', null)
    },
    async refresh() {
      this.loading = true
      const obj = {
        company: this.company,
        client_type: this.clientType,
        tarif: this.tarif,
        kind: this.kind,
        calculator: true,
        active: true,
        // consumption_min__lt: this.consumo,
        // consumption_max__gt: this.consumo,
      }
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
