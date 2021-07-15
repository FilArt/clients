<template>
  <v-card>
    <v-toolbar>
      <v-toolbar-title>
        <v-btn icon color="error" @click="$router.back()">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        Ofertas
      </v-toolbar-title>
    </v-toolbar>

    <v-list>
      <v-list-item v-for="company in companies" :key="company.id">
        <v-list-item-title v-text="`(ID: ${company.id}) ` + company.name" />
        <v-list-item-action>
          <v-checkbox
            v-model="company.offer_status_used"
            label="Estado de oferta?"
            @change="modifyCompany(company.id, { offer_status_used: company.offer_status_used })"
          />
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      companies: [],
      errorMessages: {},
      loading: false,
    }
  },
  async mounted() {
    await this.refresh()
  },
  methods: {
    async refresh() {
      this.companies = await this.$axios.$get('calculator/companies/')
    },
    async modifyCompany(id, data) {
      this.loading = true
      try {
        await this.$axios.$patch(`calculator/companies/${id}/`, data)
        await this.refresh()
        this.$toast.global.done()
      } catch (e) {
        this.errorMessages = e.reponse.data
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
