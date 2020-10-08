<template>
  <offers-view detail-url="/ofertas/search" />
</template>
<script>
export default {
  components: {
    OffersView: () => import('@/components/offers/OffersView'),
  },
}
</script>
