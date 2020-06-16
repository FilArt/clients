<template>
  <v-card v-if="card">
    <v-card-title>
      {{ card.name }}
    </v-card-title>
    <v-divider />
    <v-card-text>
      <v-data-table
        hide-default-footer
        :headers="headers"
        :items="[card.data]"
      />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'CardDetail',
  props: {
    card: {
      type: Object,
      default: () => null,
    },
  },
  computed: {
    headers() {
      return Object.keys(this.card.data).map((header) => {
        return {
          text: header,
          value: header,
        }
      })
    },
  },
}
</script>
