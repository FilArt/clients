<template>
  <v-container>
    <v-card>
      <v-card-title> Call-Visit Ficha </v-card-title>
      <v-card-text>
        <v-alert v-if="error" type="error">{{ error }}</v-alert>

        <template v-if="card">
          <template v-for="field in cardFields">
            <div :key="field.value">
              <v-select
                v-if="field.type === 'select'"
                v-model="card[field.value]"
                :label="field.label"
                :items="field.items"
              />
              <v-text-field v-else v-model="card[field.value]" :label="field.label" />
            </div>
          </template>
        </template>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import constants from '../lib/constants'

export default {
  name: 'Ficha',
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
      url: `${constants.CV_URL}/api/cards/${this.cardId}/`,
      cardFields: [
        {
          label: 'Nombre',
          value: 'name',
        },
        // {
        //     label: "Persona contacto",
        //     value: "persona_contacto",
        // },
        {
          label: 'Estado',
          value: 'status',
          type: 'select',
        },
        {
          label: 'Operador',
          value: 'operator',
          type: 'select',
        },
        {
          label: 'Agente',
          value: 'manager',
          type: 'select',
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
  },
}
</script>
