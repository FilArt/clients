<template>
  <v-navigation-drawer permanent>
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title class="title">Solicitudes</v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-divider />

    <v-list dense nav>
      <v-list-item v-for="bid in bids" :key="bid.id" @click="$emit('chosen', bid.id)">
        <v-icon v-if="bid.offer_kind === 'luz'" color="warning">mdi-flash</v-icon>
        <v-icon v-else color="blue">mdi-fire</v-icon>
        <v-list-item-title>
          <small> ID: {{ bid.id }} </small>
          <v-divider vertical />
          <i> {{ bid.status }} </i>
        </v-list-item-title>
      </v-list-item>

      <v-dialog v-model="addNewBidDialog" max-width="750">
        <template v-slot:activator="{ on }">
          <v-list-item v-on="on">
            <v-list-item-avatar>
              <v-icon color="success">mdi-plus</v-icon>
            </v-list-item-avatar>
            <v-list-item-title>Añadir nuevo solicitud</v-list-item-title>
          </v-list-item>
        </template>

        <add-new-bid
          :user-id="userId"
          @close="addNewBidDialog = false"
          @bid-added="
            $emit('bid-added')
            addNewBidDialog = false
          "
        />
      </v-dialog>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import AddNewBid from '@/components/forms/AddNewBid'
export default {
  name: 'SolicitudesBar',
  components: { AddNewBid },
  props: {
    bids: {
      type: Array,
      default: () => [],
    },
    userId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      addNewBidDialog: false,
    }
  },
}
</script>
