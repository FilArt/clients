<template>
  <v-card>
    <v-card-text v-if="$auth.user.role === 'admin'">
      <admin-header />
    </v-card-text>

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

    <v-card-title>Bids</v-card-title>
    <v-card-text>
      <v-list>
        <v-list-group
          v-for="bid in user.bids"
          :key="bid.id"
          v-model="bid.active"
          no-action
        >
          <template v-slot:activator>
            <v-list-item-content>
              ID: {{ bid.id }}

              <v-chip
                :color="
                  bid.status === 'OK'
                    ? 'success'
                    : bid.status === 'Pendiente tramitacion'
                    ? 'warning'
                    : 'error'
                "
                >{{ bid.status }}</v-chip
              >
            </v-list-item-content>
          </template>

          <v-list-item>
            <v-list-item-content>
              <tramitacion :bid-id="bid.id" @tramitate="bid.status = $event" />
            </v-list-item-content>
          </v-list-item>
        </v-list-group>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    AdminHeader: () => import('~/components/admin/AdminHeader'),
    SubmitButton: () => import('~/components/buttons/submitButton'),
    StatusSelect: () => import('~/components/selects/StatusSelect'),
    PhoneField: () => import('~/components/fields/phoneField'),
    EmailField: () => import('~/components/fields/emailField'),
    Tramitacion: () => import('~/components/support/Tramitacion'),
  },
  data() {
    return {
      cols: 3,
      errorMessages: { status: null, message: null },
    }
  },
  async asyncData({ $axios, params, store }) {
    const user = await $axios.$get(`users/users/${params.id}/`)

    return {
      user,
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
  methods: {
    async refresh() {
      this.user = await this.$axios.$get(`users/users/${this.user.id}/`)
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
