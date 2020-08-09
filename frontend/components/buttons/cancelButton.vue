<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on }">
      <v-btn icon color="warning" v-on="on" @click="$emit('click')">
        <v-icon>mdi-cancel</v-icon>
      </v-btn>
    </template>
    <span>Cancelar</span>
  </v-tooltip>
</template>

<script>
export default {
  name: 'CancelButton',
}
</script>
