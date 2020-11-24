<template>
  <div>
    <v-row v-for="item in items" :key="item.id">
      <v-col>
        <v-switch
          persistent-hint
          :hint="item.hint"
          :label="item.name"
          :value="isActive(item)"
          @click="
            $emit(
              'input',
              isActive(item)
                ? value.filter((activeItem) => activeItem[itemValue] !== item[itemValue])
                : activeItems.concat(item),
            )
          "
        />
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: 'ItemGrouper',
  props: {
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
  },
  methods: {
    isActive(item) {
      return this.activeItems.some((activeItem) => activeItem.id === item.id)
    },
  },
}
</script>
