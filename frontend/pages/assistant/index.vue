<template>
  <v-card>
    <v-card-text class="text-center">
      <div class="text-h4">Para nosotros es importante que nuestros clientes reciban atención personalizada</div>

      <div class="text-h6">
        En esta página encontrará los datos de contacto y el chat de su asistente personal, no dude en ponerse en
        contacto con él para cualquier pregunta
      </div>
    </v-card-text>

    <v-row align="center">
      <v-col class="text-center">
        <v-avatar height="300" width="300">
          <v-img src="/isai.jpg" />
        </v-avatar>
      </v-col>

      <v-col class="text-center">
        <v-row>
          <v-col class="subtitle-1"> Tu gestor energético personal </v-col>
        </v-row>
        <v-row>
          <v-col class="subtitle-1"> Isai Secaduras </v-col>
        </v-row>

        <v-row class="flex-wrap">
          <v-col>
            <div>
              <v-icon left> mdi-phone </v-icon>
              <a href="tel:900838839"> 900-838-839 </a>
            </div>

            <div>
              <v-icon left> mdi-email </v-icon>
              <a href="mailto:isai@gestiongroup.es"> isai@gestiongroup.es </a>
            </div>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <v-row v-if="isLeed" class="pa-3 text-center mx-auto" style="margin-top: 1em">
      <v-col>
        Sí tiene dudas para seleccionar una oferta de nuestro catálogo o prefiere que nuestros agentes le asesoren
        personalmente. Por favor rellene el siguiente formulario y nos pondremos en contacto con usted lo antes
        posible.
      </v-col>
    </v-row>

    <v-row v-if="isLeed" class="mx-auto" style="max-width: 1000px">
      <v-col>
        <v-form @submit.prevent="submit">
          <v-file-input v-model="factura" label="Foto factura actual (anverso)" :error-messages="errors.factura">
            <template v-if="loadedFactura" v-slot:append-outer>
              <v-chip link exact target="_blank" :href="loadedFactura.attachment">
                {{ loadedFactura.type_verbose_name }}
              </v-chip>
            </template>
          </v-file-input>

          <v-file-input
            v-model="facturaReverso"
            label="Foto factura actual (reverso)"
            :error-messages="errors.factura_1"
          >
            <template v-if="loadedFacturaReverso" v-slot:append-outer>
              <v-chip link exact target="_blank" :href="loadedFacturaReverso.attachment">
                {{ loadedFacturaReverso.type_verbose_name }}
              </v-chip>
            </template>
          </v-file-input>

          <submit-button label="Enviar" block />
        </v-form>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
export default {
  components: {
    SubmitButton: () => import('~/components/buttons/submitButton'),
  },
  async asyncData({ $auth, $axios }) {
    const isLeed = $auth.user.client_role === 'leed'
    if (isLeed) {
      const attachments = await $axios.$get('users/users/load_facturas/')
      const loadedFactura = attachments.find((a) => a.attachment_type === 'factura')
      const loadedFacturaReverso = attachments.find((a) => a.attachment_type === 'factura_1')
      return {
        isLeed,
        loadedFactura,
        loadedFacturaReverso,
      }
    }
    return {
      isLeed,
    }
  },
  data() {
    return {
      factura: null,
      facturaReverso: null,
      errors: {},
    }
  },
  methods: {
    async submit() {
      this.errors = {}
      const formData = new FormData()
      formData.append('factura', this.factura)
      formData.append('factura_1', this.facturaReverso)
      const func = this.loadedFactura ? this.$axios.$patch : this.$axios.$post
      try {
        const attachments = await func('users/users/load_facturas/', formData)
        this.loadedFactura = attachments.find((a) => a.attachment_type === 'factura')
        this.loadedFacturaReverso = attachments.find((a) => a.attachment_type === 'factura_1')
        await this.$swal({
          title: 'Salvado',
          icon: 'success',
        })
      } catch (e) {
        this.errors = e.response.data
        if (this.errors.profileNotFilled) {
          await this.$swal({
            title: 'Por favor, complete su perfil por completo.',
            text: 'Para comenzar el proceso de contratación, debe completar su perfil.',
            icon: 'warning',
          })
          await this.$router.push('/profile')
        }
      }
    },
  },
}
</script>
