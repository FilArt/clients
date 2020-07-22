<template>
  <v-card>
    <v-card-text v-if="$auth.user.role === 'admin'">
      <admin-header />
    </v-card-text>

    <v-card-title>
      <p class="flex-grow-1">Contratar oferta {{ bid.id }}</p>
    </v-card-title>

    <v-card-text>
      <v-form @submit.prevent="submit" novalidate>
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

        <v-text-field v-model="form.dni" label="DNI Representante legal" />

        <phone-field
          v-model="phoneMobile"
          label="Teléfono mobil"
          :error-messages="phoneErrors['mobile']"
        />

        <phone-field
          v-if="['admin', 'support'].includes($auth.user.role)"
          v-model="phoneCity"
          label="Teléfono fijo"
          :error-messages="phoneErrors['city']"
        />

        <v-row align="center" class="text-center">
          Puntos suministros
          <v-col v-for="(punto, idx) in puntos" :key="idx">
            <add-punto
              :offer-client-type="bid.offer.client_type"
              color="green"
              :punto="punto"
              :label="`Punto suministro #${idx + 1}`"
              @punto-edited="fetchPuntos"
              @punto-deleted="fetchPuntos"
            />
          </v-col>
        </v-row>

        <v-divider />

        <v-row align="center" class="text-center">
          <v-col>
            <add-punto
              :offer-client-type="bid.offer.client_type"
              :bidId="bid.id"
              @punto-created="fetchPuntos"
            />
          </v-col>
        </v-row>

        <v-divider />

        <v-row>
          <v-col>
            <submit-button block label="Contratar" />
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
const phoneErrors = { city: [], mobile: [] }
export default {
  components: {
    AdminHeader: () => import('~/components/admin/AdminHeader'),
    AddPunto: () => import('~/components/puntos/AddPunto'),
    PhoneField: () => import('~/components/fields/phoneField'),
    CloseButton: () => import('~/components/buttons/closeButton'),
    SubmitButton: () => import('~/components/buttons/submitButton'),
  },
  data() {
    return {
      form: JSON.parse(JSON.stringify(this.$auth.user)),
      error: {},
      phoneErrors: phoneErrors,
    }
  },
  async asyncData({ $axios, params }) {
    const bid = await $axios.$get(`bids/bids/${params.id}/`)
    const puntos = await $axios.$get(`/users/puntos/?bid=${bid.id}`)
    const phones = await $axios.$get('/users/phones/')
    return {
      phones,
      phoneMobile: (
        phones.find((phoneObject) => phoneObject.phone_type == 'mobile') || {}
      ).number,
      phoneCity: (
        phones.find((phoneObject) => phoneObject.phone_type == 'city') || {}
      ).number,
      puntos,
      bid,
      isIndividual: bid.offer.client_type === 0,
    }
  },
  methods: {
    async fetchPuntos() {
      this.puntos = await this.$axios.$get(`/users/puntos/?bid=${this.bid.id}`)
    },
    loadPhones() {
      this.phoneErrors = phoneErrors
      const types = ['city', 'mobile']
      types.forEach((type) => {
        this.loadPhone(type)
      })
    },
    async loadPhone(type) {
      const value = type === 'city' ? this.phoneCity : this.phoneMobile
      const existedPhone = this.phones.find(
        (phoneObject) => phoneObject.phone_type === type
      )
      const axiosFunc = existedPhone ? this.$axios.$patch : this.$axios.$post
      const aep = existedPhone
        ? `/users/phones/${existedPhone.id}/`
        : '/users/phones/'
      const data = existedPhone
        ? {
            id: existedPhone.id,
            number: value,
            phone_type: type,
            bid: this.bid.id,
          }
        : { number: value, phone_type: type, bid: this.bid.id }
      try {
        await axiosFunc(aep, data)
      } catch (e) {
        this.phoneErrors[type] = e.response.data.number
      }
    },
    async submit() {
      if (!this.puntos || !this.puntos.length) {
        await this.$swal({
          title: 'No puntos!',
          icon: 'error',
        })
        return
      }
      this.loadPhones()
      try {
        await this.$axios.$patch(
          `users/account/${this.$auth.user.id}/`,
          this.form
        )
        await this.$auth.fetchUser()
        await this.$router.push(`/bids/${this.bid.id}`)
        await this.$swal({
          title: 'Contratado!',
          icon: 'success',
        })
      } catch (e) {
        this.error = e.response.data
      }
    },
  },
}
</script>
