<template>
  <div>
    <div v-for="punto in puntos" :key="punto.id">
      <v-row>
        <v-col>
          <v-row>
            <v-col>
              <v-card-title> Punto: {{ punto.id }} </v-card-title>
              <v-card-text>
                <div
                  class="d-flex"
                  v-for="field in puntoHeaders"
                  :key="field.value"
                >
                  <v-row>
                    <v-col>
                      <span> {{ field.name }}: </span>
                    </v-col>
                    <v-spacer />

                    <v-col>
                      <company-select
                        v-if="editable && field.value === 'company_luz'"
                        :value="punto.company_luz"
                        @input="
                          save({
                            id: punto.id,
                            field: 'company_luz',
                            value: $event,
                          })
                        "
                      />
                      <v-text-field
                        v-if="editable"
                        :value="punto[field.value]"
                        append-icon="mdi-content-save"
                        @input="values[field.value] = $event"
                        @click:append="
                          save({ id: punto.id, field: field.value })
                        "
                      />
                      <code v-else>
                        {{ punto[field.value] || '-' }}
                      </code>
                    </v-col>
                  </v-row>
                </div>
              </v-card-text>
            </v-col>

            <v-col>
              <v-card-title>Archivos adjuntos</v-card-title>
              <v-card-text>
                <v-chip
                  v-for="attachment in punto.attachments"
                  :key="attachment.id"
                  link
                  exact
                  target="_blank"
                  :href="attachment.attachment"
                  >Attachment {{ attachment.id }}</v-chip
                >
              </v-card-text>
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <v-divider :key="punto.id" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'PuntosList',
  components: {
    CompanySelect: () => import('~/components/selects/CompanySelect'),
  },
  props: {
    editable: {
      type: Boolean,
      default: false,
    },
    puntos: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      values: {},
    }
  },
  computed: {
    puntoHeaders() {
      return this.$store.state.puntoHeaders
    },
  },
  async created() {
    if (!this.puntoHeaders || !this.puntoHeaders.length) {
      this.$store.commit(
        'setPuntoHeaders',
        await this.$axios.$get('/users/puntos/get_headers/')
      )
    }
  },
  methods: {
    async save({ id, field, value }) {
      console.log(value)
      const data = {}
      data[field] = value || this.values[field]
      try {
        await this.$axios.$patch(`users/puntos/${id}/`, data)
        await this.$swal({
          title: 'Saved!',
          text: `New value of ${field} = ${value || this.values[field]}`,
          icon: 'success',
        })
      } catch (e) {
        const errorMsg = e.response.data
        await this.$swal({
          title: 'Error!',
          text:
            errorMsg[field] instanceof Array
              ? errorMsg[field].join(',')
              : JSON.stringify(errorMsg),
          icon: 'error',
        })
      }
      this.$emit('puntoUpdated')
    },
  },
}
</script>
