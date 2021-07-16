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
          <decimal-field v-model="settings.tax" :error-messages="errors.tax" label="Imp. electricidad" />
          <decimal-field
            v-model="settings.carbon_tax"
            :error-messages="errors.carbon_tax"
            label="Imp. hidrocarburos"
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
