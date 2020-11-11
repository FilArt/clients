<template>
  <v-dialog v-if="userId" v-model="dialog" max-width="750">
    <template v-slot:activator="{ on }">
      <v-btn outlined :icon="!label" v-on="on">
        {{ label }}
        <v-icon :right="!!label" color="success">mdi-plus</v-icon>
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
