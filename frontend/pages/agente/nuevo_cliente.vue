<template>
  <v-card>
    <v-toolbar>
      <v-toolbar-title> Anadir nuevo cliente </v-toolbar-title>
    </v-toolbar>

    <v-card-text>
      <add-new-client @added="onAdded" />
    </v-card-text>

    <v-card-text>
      <borradores />
    </v-card-text>
  </v-card>
</template>

<script>
import AddNewClient from '@/components/forms/AddNewClient'
import Borradores from '@/components/tables/Borradores.vue'
export default {
  name: 'NuevoCliente',
  components: { AddNewClient, Borradores },
  methods: {
    onAdded(newClient) {
      this.$router.push(`/agente/tramitacion/${newClient.id}`)
    },
  },
}
</script>
