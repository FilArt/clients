<template>
  <v-autocomplete
    v-model="agents"
    :label="label"
    :error-messages="errorMessages"
    :items="$store.state.responsibles"
    :append-icon="appendIcon"
    :multiple="multiple"
    item-text="fullname"
    item-value="id"
    @input="$emit('input', $event)"
    @click:append="$emit('click:append', $event)"
  />
</template>

<script>
export default {
  name: 'AgentsList',
  props: {
    value: {
      type: [Object, Array],
      default: () => null,
    },
    errorMessages: {
      type: Array,
      default: () => [],
    },
    label: {
      type: String,
      default: 'Agentes',
    },
    appendIcon: {
      type: String,
      default: '',
    },
    multiple: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      agents: this.value,
    }
  },
  watch: {
    value: {
      handler: function (val) {
        this.agents = val
      },
      deep: true,
    },
  },
  async created() {
    if (!this.$store.state.responsibles.length) {
      await this.$store.dispatch('fetchResponsibles')
    }
  },
}
</script>
