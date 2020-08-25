<template>
  <v-list>
    <v-list-group v-for="punto in puntos" :key="punto.id">
      <template v-slot:activator>
        <v-list-item-title>Punto suministro {{ punto.name || `(id: ${punto.id})` }}</v-list-item-title>
      </template>

      <div class="d-flex flex-wrap">
        <v-card v-for="group in groups" :key="group.text" class="pa-3 mx-auto">
          <v-card-title>{{ group.text }}</v-card-title>

          <div v-for="header in group.headers" :key="header.value">
            <company-select
              v-if="editable && header.value === 'company_luz'"
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
              v-else-if="editable"
              :label="header.text"
              :value="punto[header.value]"
              append-icon="mdi-content-save"
              @input="values[header.value] = $event"
              @click:append="save({ id: punto.id, field: header.value })"
            />

            <code v-else>
              {{ punto[header.value] || '-' }}
            </code>
          </div>

          <v-flex v-if="group.text === 'Documentacion' && punto.attachments.length">
            <v-chip
              v-for="attachment in punto.attachments"
              :key="attachment.id"
              link
              exact
              target="_blank"
              :href="attachment.attachment"
            >
              {{ attachment.type_verbose_name }}
            </v-chip>
          </v-flex>
        </v-card>
      </div>
    </v-list-group>
  </v-list>
</template>

<script>
import constants from '@/lib/constants'

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
    const puntoValues = Object.values(constants.puntoFields)

    return {
      values: {},
      groups: puntoValues
        .map((field) => field.group.text)
        .filter(constants.onlyUnique)
        .map((groupText) => {
          return {
            text: groupText,
            headers: puntoValues
              .filter((field) => field.group.text === groupText)
              .map((field) => {
                return {
                  text: field.text,
                  value: field.value,
                }
              }),
          }
        }),
    }
  },
  methods: {
    async save({ id, field, value }) {
      const data = {}
      value = value === undefined ? null : value
      data[field] = value || this.values[field]
      try {
        await this.$axios.$patch(`users/puntos/${id}/`, data)
        await this.$swal({
          title: 'Salvado',
          text: `${field.toUpperCase()} esta cambiado ${value || this.values[field] || 'null'}`,
          icon: 'success',
        })
        this.$emit('punto-updated')
      } catch (e) {
        const errorMsg = e.response.data
        await this.$swal({
          title: 'Error!',
          text: errorMsg[field] instanceof Array ? errorMsg[field].join(',') : JSON.stringify(errorMsg),
          icon: 'error',
        })
      }
    },
  },
}
</script>
