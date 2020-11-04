<template>
  <v-row align="center" class="text-center">
    <v-col>Fisico</v-col>

    <v-col class="flex-grow-0">
      <v-switch
        v-model="item"
        :error-messages="errorMessages"
        chips
        deletable-chips
        @change="$emit('input', $event ? 1 : 0)"
      >
        <template v-if="hint" v-slot:append-outer>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon color="#004680" v-bind="attrs" v-on="on">
                <v-icon>mdi-information</v-icon>
              </v-btn>
            </template>
            <span>Elija el perfil de cliente más adecuado para usted.</span>
          </v-tooltip>
        </template>
      </v-switch>
    </v-col>

    <v-col>Juridico</v-col>
  </v-row>
</template>

<script>
export default {
  name: 'ClientTypeSelect',
  props: {
    hint: {
      type: Boolean,
      default: false,
    },
    value: {
      type: Number,
      default: 0,
    },
    errorMessages: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      item: this.value ? 1 : 0,
    }
  },
  watch: {
    value(val) {
      this.item = val ? 1 : 0
    },
  },
}
</script>
