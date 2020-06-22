<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on }">
      <v-btn v-on="on" icon color="error" @click="$emit('click')">
        <v-icon>mdi-trash-can-outline</v-icon>
      </v-btn>
    </template>
    <span>Eliminar</span>
  </v-tooltip>
</template>

<script>
export default {
  name: 'deleteButton',
}
</script>
