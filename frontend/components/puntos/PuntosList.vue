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
                  <span> {{ field.name }}: </span>
                  <v-spacer />
                  <code>
                    {{ punto[field.value] || '-' }}
                  </code>
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
  props: {
    puntos: {
      type: Array,
      default: () => [],
    },
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
}
</script>
