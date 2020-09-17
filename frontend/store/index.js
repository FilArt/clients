export const state = () => ({
  calculatedOffers: [],
  calculatorForm: {},
  tarif: null,
  puntoCategories: [],
  cities: [],
  privacyAccepted: false,
  companies: [],
  responsibles: [],
})

export const actions = {
  async fetchResponsibles({ commit }) {
    const users = (await this.$axios.$get('users/users/?role=agent&fields=id,fullname&itemsPerPage=100')).results
    commit('setResponsibles', users)
  },
}

export const mutations = {
  setResponsibles(state, users) {
    state.responsibles = users
  },
  setCompanies(state, companies) {
    state.companies = companies
  },
  privacyAccepted(state, boolVal) {
    state.privacyAccepted = boolVal
  },
  setCities(state, cities) {
    state.cities = cities
  },
  setPuntoCategories(state, c) {
    state.puntoCategories = c
  },
  setTarif(state, tarif) {
    state.tarif = tarif
  },
  setCalculatedOffers(state, offers) {
    state.calculatedOffers = offers
  },
  updateCalculatorForm(state, { key, value }) {
    state.calculatorForm[key] = value
  },
}
