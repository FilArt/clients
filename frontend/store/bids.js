export const state = () => ({
  bids: [],
})

export const actions = {
  async fetchBids({ commit }, { params }) {
    const bids = await this.$axios.$get(`/bids/bids/?${params}`)
    commit('setBids', bids)
  },
}

export const mutations = {
  setBids(state, bids) {
    state.bids = bids
  },
}
