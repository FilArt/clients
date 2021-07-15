<template>
  <v-card>
    <v-card-title>Update ofertas</v-card-title>
    <v-form @submit.prevent="submit">
      <v-card-text>
        <v-file-input v-model="file" label="Archivo" accept="text/csv" />
      </v-card-text>
      <v-card-actions>
        <submit-button block :loading="loading" label="Salvar" />
      </v-card-actions>
    </v-form>

    <v-card-text>
      <v-data-table
        :items="errors"
        :headers="errors && errors.length ? Object.keys(errors[0]).map((e) => ({ text: e, value: e })) : []"
      />
    </v-card-text>
  </v-card>
</template>

<script>
import submitButton from '../../../components/buttons/submitButton.vue'
export default {
  components: { submitButton },
  data() {
    return {
      loading: false,
      file: null,
      errors: [],
      errorMessages: {},
    }
  },
  methods: {
    async submit() {
      this.loading = true
      try {
        const formData = new FormData()
        formData.append('file', this.file)
        const errors = (await this.$axios.post('calculator/admin_offers/bulk_create/', formData)).data
        if (errors === 'OK') {
          this.$toast.global.done()
          await this.$router.back()
        } else {
          this.errors = errors
        }
      } catch (e) {
        if (e && e.response && e.response.data) {
          this.errorMessages = e.response.data
        } else {
          this.$toast.error({ title: 'Error', icon: 'error', text: e })
        }
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
