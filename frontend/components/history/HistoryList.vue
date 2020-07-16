<template>
  <v-timeline>
    <v-timeline-item
      v-for="story in history"
      :key="story.id"
      class="text-left"
      :left="story.user === 'me'"
      :right="story.user !== 'me'"
    >
      <span slot="icon">
        <v-icon>{{ !story.old_status ? 'mdi-plus' : '' }}</v-icon>
      </span>
      <span slot="opposite">
        {{ story.dt }}
        <br />
        {{ story.user.email || story.user }}
      </span>
      <v-card class="elevation-2">
        <v-card-title class="headline">
          <span>{{ story.new_status }}</span>
        </v-card-title>
        <v-card-text>{{ story.message }}</v-card-text>
      </v-card>
    </v-timeline-item>
  </v-timeline>
</template>
<script>
export default {
  name: 'HistoryList',
  props: {
    history: {
      type: Array,
      default: () => [],
    },
  },
}
</script>
