<template>
  <v-card>
    <v-card-title>
      <p class="flex-grow-1">Contratar oferta {{ bid.id }}</p>
    </v-card-title>

    <v-card-text>
      <v-form @submit.prevent="submit" novalidate>
        <v-checkbox
          v-model="form.change_of_name"
          label="Cambio de nombre"
          hint="Hint"
          persistent-hint
          :items="[
            {
              text: 'Si',
              value: true,
            },
            {
              text: 'No',
              value: false,
            },
          ]"
        />
        <v-text-field
          v-model="form.name"
          :label="isIndividual ? 'Nombre/razon social' : 'Nombre y apellido'"
          hint=""
        />

        <v-text-field
          v-if="!isIndividual"
          v-model="form.cif_dni"
          label="CIF/DNI"
        />

        <v-text-field
          v-if="!isIndividual"
          v-model="form.legal_representative"
          label="Representante legal"
        />

        <v-text-field v-model="form.dni" label="DNI" />

        <phone-field v-model="form.phoneMobile" label="Telefono mobil" />

        <phone-field v-model="form.phoneCity" label="Telefono pijo" />

        <email-field v-model="form.email" />

        <v-text-field v-model="form.iban" label="IBAN" />

        <v-text-field v-model="form.cups" label="CUPS LUZ" />

        <v-text-field
          v-model="form.power"
          label="Potencia contractada"
          type="number"
        />

        <v-text-field v-model="form.province" label="Provincia" />
        <v-text-field v-model="form.region" label="Poblacion" />
        <v-text-field
          v-model="form.postalcode"
          label="Codigo postal"
          type="number"
        />
        <v-text-field v-model="form.address" label="Direccion" />

        <v-row
          v-for="fileField in fileFields"
          :key="fileField.name"
          v-if="!(isIndividual && fileField.onlyBusiness)"
          align="center"
        >
          <v-col>
            <v-file-input
              v-model="files[fileField.name]"
              :label="fileField.label"
              :error-messages="fileErrors[fileField.name]"
            />
          </v-col>
          <v-col
            v-for="attachment in attachments.filter(
              (a) => a.attachment_type === fileField.name
            )"
            :key="attachment.id"
          >
            <v-chip
              close
              link
              exact
              target="_blank"
              :href="attachment.attachment"
              @click:close="deleteAttachment(attachment.id)"
            >
              Attachment {{ attachment.id }}
            </v-chip>
          </v-col>
        </v-row>

        <submit-button block label="Contratar" />
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
const defaultForm = {
  power: null,
  email: null,
  phoneMobile: null,
  phoneCity: null,
  name: null,
  cups: null,
  change_of_name: false,
  cif_dni: null,
  legal_representative: null,
  dni: null,
  iban: null,
  province: null,
  region: null,
  postalcode: null,
  address: null,
}
export default {
  components: {
    EmailField: () => import('~/components/fields/emailField'),
    PhoneField: () => import('~/components/fields/phoneField'),
    CloseButton: () => import('~/components/buttons/closeButton'),
    SubmitButton: () => import('~/components/buttons/submitButton'),
  },
  data() {
    return {
      error: {},

      fileFields: [
        {
          name: 'factura',
          label: 'Foto factura',
        },
        {
          name: 'dni1',
          label: 'Foto DNI anverso',
        },
        {
          name: 'dni2',
          label: 'Foto DNI reverso',
        },
        {
          name: 'cif1',
          label: 'Foto CIF anverso',
          onlyBusiness: true,
        },
        {
          name: 'cif2',
          label: 'Foto CIF reverso',
          onlyBusiness: true,
        },
      ],

      files: {
        photo_factura: null,
        photo_dni1: null,
        photo_dni2: null,
        photo_cif1: null,
        photo_cif2: null,
      },
      fileErrors: {},
    }
  },
  async asyncData({ route, $axios }) {
    let attachments = []
    let form = defaultForm
    let cardId = route.query.card
    if (cardId && /^\d+$/.test(cardId)) {
      const data = await $axios.$get(`cards/cards/${cardId}/`)
      form = data.data
      attachments = data.attachments
    } else {
      cardId = null
    }
    return {
      attachments: attachments,
      cardId: cardId,
      form: form,
      bid: { id: route.query.bid },
      isIndividual: route.query.isIndividual === 'true',
    }
  },
  methods: {
    async submit() {
      const axiosFunc = this.cardId ? this.$axios.$patch : this.$axios.$post
      const aep = this.cardId ? `cards/cards/${this.cardId}/` : 'cards/cards/'

      try {
        const card = await axiosFunc(aep, {
          bid: this.bid.id,
          ...{ data: this.form },
        })

        await this.loadFiles(card.id)
        if (Object.keys(this.fileErrors).length !== 0) return

        this.$swal({
          title: this.cardId ? 'Actualizado' : 'Creado',
          icon: 'success',
        })
        await this.$router.push(`/bids/${this.bid.id}`)
      } catch (e) {
        this.error = e.response.data
      }
    },
    async loadFiles(cardId) {
      for await (let fileKey of Object.keys(this.files)) {
        const file = this.files[fileKey]
        if (!file) continue
        const form = new FormData()
        form.append('attachment_type', fileKey)
        form.append('attachment', file)
        form.append('card', cardId)
        try {
          await this.$axios.$post('/cards/attachments/', form)
        } catch (e) {
          this.fileErrors = e.response.data
        }
      }
    },
    deleteAttachment(attachmentId) {
      this.$swal({
        title: `Borrar el archivo adjunto ${attachmentId}?`,
        text: '¡Una vez borrado, no podrás recuperar esto!',
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      }).then((willDelete) => {
        if (willDelete) {
          this.$axios.$delete(`cards/attachments/${attachmentId}/`).then(() => {
            this.$swal({ title: 'Solicitud eliminada!', icon: 'success' })
            this.attachments = this.attachments.filter(
              (a) => a.id !== attachmentId
            )
          })
        }
      })
    },
  },
}
</script>
