<template>
  <v-container style="border: 1px #004680 solid" fluid>
    <v-toolbar v-if="label" elevation="0" tile outlined dense>
      <v-toolbar-title>{{ label }}</v-toolbar-title>
    </v-toolbar>

    <v-row>
      <v-col>
        <small>Activo</small>
        <br />

        <v-tooltip v-for="(item, idx) in activeItems" :key="idx" bottom>
          <template v-slot:activator="{ on }">
            <v-chip color="success" label ou outlined v-on="on">
              {{ item[itemText] }}
              <v-icon
                right
                small
                color="error"
                @click="
                  $emit(
                    'input',
                    value.filter((activeItem) => activeItem[itemValue] !== item[itemValue]),
                  )
                "
              >
                mdi-close
              </v-icon>
            </v-chip>
          </template>

          <span>{{ item.hint }}</span>
        </v-tooltip>
      </v-col>

      <v-divider vertical />

      <v-col>
        <small>No activo</small>
        <br />
        <v-tooltip v-for="(item, idx) in inactiveItems" :key="idx" bottom>
          <template v-slot:activator="{ on }">
            <v-chip color="error" outlined label v-on="on">
              {{ item[itemText] }}
              <v-icon right small color="success" @click="$emit('input', activeItems.concat(item))"> mdi-plus </v-icon>
            </v-chip>
          </template>
          <span>{{ item.hint }}</span>
        </v-tooltip>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'ItemGrouper',
  props: {
    label: {
      type: String,
      default: null,
    },
    items: {
      type: Array,
      default: () => [],
    },
    value: {
      type: Array,
      default: () => [],
    },
    itemText: {
      type: String,
      default: 'text',
    },
    itemValue: {
      type: String,
      default: 'value',
    },
  },
  computed: {
    activeItems() {
      return this.items.filter((i) => this.value.some((j) => j[this.itemValue] === i[this.itemValue]))
    },
    inactiveItems() {
      return this.items.filter((i) => !this.value.some((j) => j[this.itemValue] === i[this.itemValue]))
    },
  },
  methods: {},
}
</script>
