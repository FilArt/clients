<template>
  <v-container>
    <v-card>
      <v-card-title> Call-Visit Ficha </v-card-title>
      <v-card-text>
        <v-alert v-if="error" type="error">{{ error }}</v-alert>

        <template v-if="card">
          <template v-for="field in cardFields">
            <div :key="field.value">
              <cv-user-select v-if="field.type === 'user'" v-model="card[field.value]" :type="field.value" />
              <v-select
                v-else-if="field.value === 'status'"
                v-model="card[field.value]"
                label="Estado"
                :items="statuses"
              />
              <v-select
                v-else-if="field.type === 'select'"
                v-model="card[field.value]"
                :label="field.label"
                :items="[
                  { text: 'Si', value: true },
                  { text: 'No', value: false },
                ]"
              />
              <v-text-field v-else v-model="card[field.value]" :label="field.label" />
            </div>
          </template>
        </template>
      </v-card-text>
      <v-card-actions>
        <submit-button label="Guardar" @click="submit" />
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import constants from '../lib/constants'
import SubmitButton from './buttons/submitButton.vue'

export default {
  name: 'Ficha',
  components: {
    CvUserSelect: () => import('@/components/cv_components/selects/cvUserSelect'),
    SubmitButton,
  },
  props: {
    cardId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      loading: false,
      card: null,
      error: '',
      api: null,
      statuses: Object.values(constants.cvStatuses),
      url: `${constants.CV_URL}/api/cards/${this.cardId}/`,
      cardFields: [
        {
          label: 'Nombre',
          value: 'name',
        },
        {
          label: 'Estado',
          value: 'status',
        },
        {
          label: 'Operador',
          value: 'operator',
          type: 'user',
        },
        {
          label: 'Agente',
          value: 'manager',
          type: 'user',
        },
        {
          label: 'Cliente',
          value: 'is_client',
          type: 'select',
        },
      ],
    }
  },
  async mounted() {
    await this.$store.dispatch('fetchCvUsers')
    const token = this.$auth.user.cv_token
    if (!token) {
      alert('NO HAY TOKEN DE CALL-VISIT.')
      return
    }

    const headers = { Authorization: 'Token ' + token }
    const axiosInstance = this.$axios.create({ headers })
    this.api = axiosInstance

    await this.refresh()
  },
  methods: {
    async refresh() {
      if (!this.cardId) {
        this.error = 'Cliente no tiene call-visit ficha ID'
        return
      }
      this.loading = true
      try {
        const data = await this.api.$get(this.url)
        this.card = data
      } catch (e) {
        const err = e.response && e.response.data ? e.response.data : e
        this.error = err
      } finally {
        this.loading = false
      }
    },
    async getUsers() {
      const data = await this.api.$get(constants.CV_URL + '/api/users/')
      console.log(data)
    },
    async submit() {
      const data = {}
      this.cardFields.forEach((f) => {
        data[f.value] = this.card[f.value]
      })
      try {
        await this.api.$patch(this.url, data)
        await this.refresh()
      } catch (e) {
        alert(JSON.stringify(e.response.data))
      }
    },
  },
}
</script>
