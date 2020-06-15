<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on }">
      <v-btn v-on="on" icon color="error" @click="$emit('click')">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </template>
    <span>Close</span>
  </v-tooltip>
</template>

<script>
export default {
  name: 'closeButton',
}
</script>
