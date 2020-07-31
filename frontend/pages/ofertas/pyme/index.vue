<template>
  <offers-view
    :default-filters="{
      client_type: 1,
      company: $route.query.company
        ? parseInt($route.query.company || '1')
        : '',
      tarif: $route.query.tarif,
      is_price_permanent: $route.query.is_price_permanent,
    }"
  />
</template>
<script>
export default {
  components: {
    OffersView: () => import('~/components/offers/OffersView'),
  },
}
</script>
