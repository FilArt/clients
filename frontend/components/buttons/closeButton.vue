<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on }">
      <v-btn icon color="error" v-on="on" @click="$emit('click')">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </template>
    <span>Close</span>
  </v-tooltip>
</template>

<script>
export default {
  name: 'CloseButton',
}
</script>
