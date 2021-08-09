<template>
  <v-dialog v-model="dialog" max-width="750">
    <template v-slot:activator="{ on }">
      <v-btn icon color="success" v-on="on">
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </template>

    <v-card>
      <v-card-title>
        Añadir nuevo cliente
        <v-spacer />
        <close-button @click="dialog = false" />
      </v-card-title>

      <v-card-text>
        <add-new-client />
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import AddNewClient from '@/components/forms/AddNewClient'
import CloseButton from '@/components/buttons/closeButton'

export default {
  name: 'AddNewClientDialog',
  components: { CloseButton, AddNewClient },
  data() {
    return {
      dialog: false,
    }
  },
}
</script>
