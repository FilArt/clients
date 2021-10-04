<template>
  <v-container>
    <v-card>
      <v-card-title>
        Call-Visit Ficha
        <v-spacer />
        <v-btn target="_blank" :href="feUrl">
          <v-icon left>mdi-eye</v-icon>
          Abrir en Call-Visit
        </v-btn>
        <v-spacer />
        <v-text-field
          v-model="callVisitId"
          label="Call-Visit ID"
          append-icon="mdi-content-save"
          @click:append="onSaveNewCallVisitID"
        />
        <v-btn icon color="success" @click="refresh">
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-alert v-if="error" type="error">{{ error }}</v-alert>

        <template v-if="card">
          <template v-for="field in cardFields">
            <div :key="field.value">
              <v-select
                v-if="field.type === 'user'"
                v-model="card[field.value]"
                :label="field.label"
                :items="users.filter((u) => u.position === field.value)"
                item-text="fullname"
                item-value="id"
                clearable
              />
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

              <date-time-filter
                v-else-if="field.type === 'datetime'"
                v-model="card[field.value]"
                :label="field.label"
                formatted="DD/MM/YYYY HH:mm"
                format="YYYY-MM-DD HH:mm"
              />

              <date-time-filter
                v-else-if="field.type === 'date'"
                v-model="card[field.value]"
                :label="field.label"
                formatted="DD/MM/YYYY"
                format="DD/MM/YYYY HH:mm"
              />

              <v-text-field v-else v-model="card[field.value]" :label="field.label" />
            </div>
          </template>
        </template>
      </v-card-text>
      <v-card-actions>
        <submit-button label="Guardar" :loading="loading" @click="submit" />
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import { format, parse } from 'date-fns'
import constants from '../lib/constants'
import SubmitButton from './buttons/submitButton.vue'
export default {
  name: 'Ficha',
  components: {
    SubmitButton,
    DateTimeFilter: () => import('~/components/DateTimeFilter'),
  },
  props: {
    cardId: {
      type: Number,
      default: null,
      validator: (x) => x === null || (typeof x === 'number' && x > 0),
    },
    userId: {
      type: Number,
      default: null,
      validator: (x) => typeof x === 'number' && x > 0,
    },
  },
  data() {
    return {
      constants,
      callVisitId: this.cardId,
      loading: false,
      card: null,
      error: '',
      api: null,
      users: [],
      statuses: Object.values(constants.cvStatuses),
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
        {
          label: 'Persona contacto',
          value: 'persona_contacto',
        },
        {
          label: 'Fecha vencimiento',
          value: 'next_action_date',
          type: 'datetime',
        },
        {
          label: 'Fecha firma',
          value: 'fecha_firma',
          type: 'date',
        },
      ],
    }
  },
  computed: {
    url() {
      return `${constants.CV_URL}/api/cards/${this.callVisitId}/`
    },
    feUrl() {
      return constants.CV_URL.replace('8000', '8080') + '/admin/ficha/' + this.callVisitId
    },
  },
  watch: {
    async cardId() {
      this.card = null
      await this.refresh()
    },
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

    this.fetchUsers()

    await this.refresh()
  },
  methods: {
    async onSaveNewCallVisitID() {
      await this.$axios.$patch(`/users/users/${this.userId}/`, { call_visit_id: parseInt(this.callVisitId) || null })
      await this.refresh()
    },
    async refresh() {
      this.card = this.error = null

      this.loading = true

      try {
        const data = await this.api.$get(this.url)

        if (data.next_action_date) {
          data.next_action_date = this.$dateFns.format(
            this.$dateFns.parse(data.next_action_date, 'dd/MM/yyyy HH:mm', new Date()),
            'yyyy-MM-dd HH:mm',
          )
        }
        this.card = data
      } catch (e) {
        console.log(e)
        if (e.response.status === 404) {
          this.error = '404. No encontrado'
        } else {
          const err = e.response && e.response.data ? e.response.data : e
          this.error = err
        }
      } finally {
        this.loading = false
      }
    },
    async fetchUsers() {
      this.users = await this.api.$get(constants.CV_URL + '/api/users/')
    },
    async submit() {
      this.loading = true
      const data = {}
      this.cardFields.forEach((f) => {
        const v = this.card[f.value]
        if (f.type === 'date') {
          data[f.value] = v ? format(parse(v.substring(0, 10), 'dd/MM/yyyy', new Date()), 'yyyy-MM-dd') : null
        } else {
          data[f.value] = v
        }
      })
      try {
        await this.api.$patch(this.url, data)
        this.$toast.global.done()
        await this.refresh()
      } catch (e) {
        alert(JSON.stringify(e.response.data))
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
