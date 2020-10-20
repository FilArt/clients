<template>
  <v-dialog v-if="userId" v-model="dialog" max-width="750">
    <template v-slot:activator="{ on }">
      <v-btn icon v-on="on">
        <v-icon color="success">mdi-plus</v-icon>
      </v-btn>
    </template>

    <add-new-bid
      :user-id="userId"
      @close="dialog = false"
      @bid-added="
        $emit('bid-added')
        dialog = false
      "
    />
  </v-dialog>
</template>

<script>
import AddNewBid from '@/components/forms/AddNewBid'
export default {
  name: 'AddNewBidDialog',
  components: { AddNewBid },
  props: {
    userId: {
      type: Number,
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
