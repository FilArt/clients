<template>
  <v-dialog v-model="dialog" scrollable max-width="750">
    <template v-slot:activator="{ on }">
      <v-btn color="info" v-on="on">
        <v-icon>mdi-cog</v-icon>
      </v-btn>
    </template>

    <v-card>
      <v-card-title> Comparador configuraciones </v-card-title>

      <v-divider />

      <v-card-text>
        <v-form @submit.prevent="submit">
          <decimal-field v-model="settings.iva" :error-messages="errors.iva" label="IVA" @input="test" />
          <decimal-field v-model="settings.igic" :error-messages="errors.igic" label="IGIC" />
          <decimal-field v-model="settings.tax" :error-messages="errors.tax" label="Imp. electricidad" />
          <decimal-field
            v-model="settings.carbon_tax"
            :error-messages="errors.carbon_tax"
            label="Imp. hidrocarburos"
          />
          <decimal-field
            v-model="settings.equip_rent_t20td"
            :error-messages="errors.equip_rent_t20td"
            label="Alquiler de equipos (2.0TD)"
          />
          <decimal-field
            v-model="settings.equip_rent_t30td"
            :error-messages="errors.equip_rent_t30td"
            label="Alquiler de equipos (3.0TD)"
          />
          <decimal-field
            v-model="settings.equip_rent_t61td"
            :error-messages="errors.equip_rent_t61td"
            label="Alquiler de equipos (6.1TD)"
          />
          <decimal-field
            v-model="settings.equip_rent_g31"
            :error-messages="errors.equip_rent_g31"
            label="Alquiler de equipos (3.1)"
          />
          <decimal-field
            v-model="settings.equip_rent_g32"
            :error-messages="errors.equip_rent_g32"
            label="Alquiler de equipos (3.2)"
          />
          <decimal-field
            v-model="settings.equip_rent_g33"
            :error-messages="errors.equip_rent_g33"
            label="Alquiler de equipos (3.3)"
          />
          <decimal-field
            v-model="settings.equip_rent_g34"
            :error-messages="errors.equip_rent_g34"
            label="Alquiler de equipos (3.4)"
          />
        </v-form>
      </v-card-text>

      <v-divider />

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="warning" @click="dialog = false"> Cancelar </v-btn>
        <v-btn :loading="loading" color="success" @click="submit">
          Salvar
          <v-icon>mdi-check</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'CalculatorSettingsDialog',
  components: {
    DecimalField: () => import('@/components/fields/decimalField'),
  },
  data() {
    return {
      settings: {},
      dialog: false,
      loading: false,
      errors: {},
    }
  },
  async created() {
    const settingsResponse = await this.$axios.get('/calculator/settings/')
    this.settings = settingsResponse.data[0]
  },
  methods: {
    async submit() {
      this.loading = true
      this.errors = {}
      try {
        await this.$axios.patch(`/calculator/settings/${this.settings.id}/`, this.settings)
        this.$toast.global.done()
      } catch (e) {
        this.errors = e.response.data
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
