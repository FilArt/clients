export const state = () => ({
  calculatedOffers: [],
  calculatorForm: {},
  tarif: null,
  puntoCategories: [],
  cities: [],
  privacyAccepted: false,
  companies: [],
  tarifs: [],
  responsibles: [],
  names: [],
  bidToChange: null,
})

export const actions = {
  async fetchResponsibles({ commit }) {
    const users = (await this.$axios.$get('users/users/?role=agent&fields=id,fullname&itemsPerPage=100')).results
    commit('setResponsibles', users)
  },
  async fetchCompanies({ commit }) {
    const companies = await this.$axios.$get('/calculator/companies/')
    commit('setCompanies', companies)
  },
  async fetchTarifs({ commit }) {
    const tarifs = await this.$axios.$get('/calculator/tarifs/')
    commit('setTarifs', tarifs)
  },
  async fetchNames({ commit }) {
    const names = (await this.$axios.$get('/calculator/offers/?fields=name')).map((item) => item.name)
    commit('setNames', names)
    console.log(names)
  },
}

export const mutations = {
  setNames(state, names) {
    state.names = names
  },
  setTarifs(state, tarifs) {
    state.tarifs = tarifs
  },
  setBidToChange(state, bid) {
    state.bidToChange = bid
  },
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
