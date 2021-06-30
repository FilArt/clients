<template>
  <v-card>
    <v-toolbar>
      <v-btn icon color="error" @click="$router.back()">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <v-toolbar-title> Comparador configuraciones </v-toolbar-title>
    </v-toolbar>

    <v-card-text>
      <v-form @submit.prevent="submit">
        <v-text-field v-model="settings.iva" :error-messages="errors.iva" label="IVA" />
        <v-text-field v-model="settings.igic" :error-messages="errors.igic" label="IGIC" />
        <v-text-field v-model="settings.tax" :error-messages="errors.tax" label="Impuesto electrico" />
        <v-text-field
          v-model="settings.carbon_tax"
          :error-messages="errors.carbon_tax"
          label="impuesto sobre el carbono"
        />
        <v-text-field
          v-model="settings.equip_rent_t20td"
          :error-messages="errors.equip_rent_t20td"
          label="Alquiler de equipos (2.0TD)"
        />
        <v-text-field
          v-model="settings.equip_rent_t30td"
          :error-messages="errors.equip_rent_t30td"
          label="Alquiler de equipos (3.0TD)"
        />
        <v-text-field
          v-model="settings.equip_rent_t61td"
          :error-messages="errors.equip_rent_t61td"
          label="Alquiler de equipos (6.1TD)"
        />
        <v-text-field
          v-model="settings.equip_rent_g31"
          :error-messages="errors.equip_rent_g31"
          label="Alquiler de equipos (3.1)"
        />
        <v-text-field
          v-model="settings.equip_rent_g32"
          :error-messages="errors.equip_rent_g32"
          label="Alquiler de equipos (3.2)"
        />
        <v-text-field
          v-model="settings.equip_rent_g33"
          :error-messages="errors.equip_rent_g33"
          label="Alquiler de equipos (3.3)"
        />
        <v-text-field
          v-model="settings.equip_rent_g34"
          :error-messages="errors.equip_rent_g34"
          label="Alquiler de equipos (3.4)"
        />
        <v-btn :loading="loading" block type="submit" color="success">
          Salvar
          <v-icon>mdi-check</v-icon>
        </v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  async asyncData({ $axios }) {
    const settingsResponse = await $axios.get('/calculator/settings/')
    const settings = settingsResponse.data[0]
    return {
      settings,
    }
  },
  data() {
    return {
      loading: false,
      errors: {},
    }
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
