<template>
  <v-dialog v-if="userId" v-model="dialog" max-width="750">
    <template v-slot:activator="{ on }">
      <v-btn outlined :icon="!label" v-on="on">
        {{ label }}
        <v-icon :right="!!label" color="success">mdi-plus</v-icon>
      </v-btn>
    </template>

    <create-bid
      v-if="userId"
      :for-client="userId"
      @close="dialog = false"
      @bid-added="
        dialog = false
        $emit('bid-added')
      "
    />
  </v-dialog>
</template>

<script>
export default {
  name: 'AddNewBidDialog',
  components: {
    CreateBid: () => import('@/components/forms/CreateBid'),
  },
  props: {
    label: {
      type: String,
      default: null,
    },
    userId: {
      type: [Number, String],
      default: null,
    },
  },
  data() {
    return {
      dialog: false,
    }
  },
}
</script>
