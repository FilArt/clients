<template>
  <v-card>
    <v-card-title> Bid {{ $route.params.id }} </v-card-title>
    <v-card-text>
      <v-list>
        <v-list-item v-for="(value, name) in bid" :key="name">
          <v-list-item-group v-if="typeof value === 'object'">
            <v-list-item-title>{{ name }}</v-list-item-title>
            <v-list-item v-for="(v1, n1) in value" :key="n1" class="text-right">
              <v-list-item-title>{{ n1 }}: {{ v1 }}</v-list-item-title>
            </v-list-item>
          </v-list-item-group>

          <v-list-item-title v-else>{{ name }}: {{ value }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-card-text>
    <v-card-actions>
      <return-button to="/bids" />
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  components: {
    ReturnButton: () => import('~/components/buttons/returnButton'),
  },
  async asyncData({ $axios, params }) {
    const bid = await $axios.$get(`bids/${params.id}`)
    return { bid, id: params.id }
  },
}
</script>
