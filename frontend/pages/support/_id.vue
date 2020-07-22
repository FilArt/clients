<template>
  <v-card>
    <v-card-text v-if="$auth.user.role === 'admin'">
      <admin-header />
    </v-card-text>

    <v-card-title>Oferta</v-card-title>
    <v-card-text>
      <detail-offer :offer="bid.offer" />
    </v-card-text>

    <v-divider />

    <v-card-title>Datos de clientes</v-card-title>
    <v-card-text>
      <v-row>
        <v-col :cols="cols">
          <v-text-field
            v-model="values.first_name"
            label="Nombre"
            append-icon="mdi-content-save"
            @click:append="update({ field: 'first_name' })"
            @keyup.enter="update({ field: 'first_name' })"
          />
        </v-col>

        <v-col :cols="cols">
          <v-text-field
            v-model="values.last_name"
            label="Apellido"
            append-icon="mdi-content-save"
            @click:append="update({ field: 'last_name' })"
            @keyup.enter="update({ field: 'last_name' })"
          />
        </v-col>

        <v-col :cols="cols">
          <phone-field
            v-model="values.phone"
            label="Telefono"
            append-icon="mdi-content-save"
            @click:append="update({ field: 'phone' })"
            @keyup.enter="update({ field: 'phone' })"
          />
        </v-col>

        <v-col :cols="cols">
          <email-field v-model="values.email" label="Email" readonly />
        </v-col>

        <v-col :cols="cols">
          <v-text-field
            v-model="values.dni"
            label="DNI"
            append-icon="mdi-content-save"
            @click:append="update({ field: 'dni' })"
            @keyup.enter="update({ field: 'dni' })"
          />
        </v-col>

        <v-col :cols="cols">
          <v-text-field
            v-model="values.cif_dni"
            label="CIF/DNI"
            append-icon="mdi-content-save"
            @click:append="update({ field: 'cif_dni' })"
            @keyup.enter="update({ field: 'cif_dni' })"
          />
        </v-col>

        <v-col :cols="cols">
          <v-text-field
            v-model="values.legal_representative"
            label="Legal representative"
            append-icon="mdi-content-save"
            @click:append="update({ field: 'legal_representative' })"
            @keyup.enter="update({ field: 'legal_representative' })"
          />
        </v-col>
      </v-row>
    </v-card-text>

    <v-divider />

    <v-card-title>Puntos suministros</v-card-title>
    <v-card-text>
      <puntos-list :puntos="puntos" editable @punto-updated="fetchPuntos" />
    </v-card-text>

    <v-card-actions>
      <v-dialog v-model="submitDialog">
        <template v-slot:activator="{ on }">
          <v-btn color="primary" v-on="on" block>
            Enviar
            <v-icon right>mdi-check</v-icon>
          </v-btn>
        </template>
        <v-card>
          <v-card-title>
            <p class="flex-grow-1">Enviar</p>
            <close-button @click="submitDialog = false" />
          </v-card-title>
          <v-card-text>
            <v-form @submit.prevent="submit" novalidate>
              <status-select
                v-model="data.status"
                :errors="errorMessages.status"
              />
              <v-textarea
                v-model="data.message"
                label="Mensaje"
                :placeholder="
                  data.status === 'success'
                    ? 'Contrato celebrado!'
                    : 'No puede hacer un contrato porque...'
                "
              />

              <v-card-actions>
                <v-btn
                  block
                  type="submit"
                  color="success"
                  :disabled="!data.status || !data.message"
                >
                  Listo
                  <v-icon right>mdi-check</v-icon>
                </v-btn>
              </v-card-actions>
            </v-form>
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  components: {
    AdminHeader: () => import('~/components/admin/AdminHeader'),
    SubmitButton: () => import('~/components/buttons/submitButton'),
    CloseButton: () => import('~/components/buttons/closeButton'),
    StatusSelect: () => import('~/components/selects/StatusSelect'),
    DetailOffer: () => import('~/components/detailOffer'),
    PuntosList: () => import('~/components/puntos/PuntosList'),
    PhoneField: () => import('~/components/fields/phoneField'),
    EmailField: () => import('~/components/fields/emailField'),
  },
  async asyncData({ $axios, params, store }) {
    const bid = await $axios.$get(`bids/bids/${params.id}?support=true`)
    const user = bid.user
    let puntoHeaders = store.state.puntoHeaders
    if (!puntoHeaders || !puntoHeaders.length) {
      puntoHeaders = await $axios.$get('/users/puntos/get_headers/')
      store.commit('setPuntoHeaders', puntoHeaders)
    }
    return {
      bid,
      puntos: bid.puntos.sort((a, b) => a.id > b.id),
      puntoHeaders,
      values: {
        first_name: user.first_name,
        last_name: user.last_name,
        phone: user.phone,
        email: user.email,
        dni: user.dni,
        iban: user.iban,
        cif_dni: user.cif_dni,
      },
    }
  },
  data() {
    return {
      cols: 3,
      submitDialog: false,
      data: {
        status: null,
        message: null,
      },
      errorMessages: { status: null, message: null },
    }
  },
  methods: {
    async fetchPuntos() {
      const bid = await this.$axios.$get(
        `bids/bids/${this.bid.id}?support=true`
      )
      this.puntos = bid.puntos.sort((a, b) => a.id > b.id)
    },
    submit() {
      this.$axios
        .$post(`bids/bids/${this.bid.id}/validate/`, this.data)
        .then((data) => {
          this.bid = data
          this.$swal({
            title: 'Listo',
            icon: 'success',
          }).then(() => this.$router.push('/support'))
        })
        .catch((e) => (this.errorMessages = e.response.data))
    },
    async update({ field }) {
      const data = {}
      let value = this.values[field]
      value = value === undefined ? null : value
      data[field] = value
      try {
        await this.$axios.$patch(`users/users/${this.bid.user.id}/`, data)
        this.bid = await this.$axios.$get(
          `bids/bids/${this.bid.id}?support=true`
        )
        await this.$swal({
          title: 'Salvado',
          text: `${field.toUpperCase()} esta cambiado ${data[field]}`,
          icon: 'success',
        })
      } catch (e) {
        await this.$swal({
          title: 'Error!',
          text: e.response.data[field]
            ? e.response.data[field].join(', ')
            : JSON.parse(e.response.data),
          icon: 'error',
        })
      }
    },
  },
}
</script>
