export const state = () => ({
  calculatedOffers: [],
  calculatorForm: {
    kind: 'luz',
    igic: false,
    client_type: 0,
  },
  puntoCategories: [],
  cities: [],
  privacyAccepted: false,
  companies: [],
  responsibles: [],
  names: [],
  bidToChange: null,
  cvusers: [],
})

export const actions = {
  async fetchCvUsers({ commit }) {
    commit('setCvUsers', await this.$axios.$post('cv_integration/x', { url: `https://app.call-visit.com/api/users/` }))
  },
  async fetchResponsibles({ commit }) {
    const users = (await this.$axios.$get('users/users/?role=agent&fields=id,fullname&itemsPerPage=100')).results
    commit('setResponsibles', users)
  },
  async fetchCompanies({ commit }) {
    const companies = await this.$axios.$get('/calculator/companies/')
    commit('setCompanies', companies)
  },
  async fetchNames({ commit }) {
    const names = (await this.$axios.$get('/calculator/offers/?fields=name')).map((item) => item.name)
    commit('setNames', names)
  },
}

export const mutations = {
  setCvUsers(state, cvusers) {
    state.cvusers = cvusers
  },
  resetCalculator(state) {
    state.calculatorForm = {
      kind: 'luz',
      igic: false,
      client_type: 0,
      reactive: 0,
    }
  },
  setNames(state, names) {
    state.names = names
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
  setCalculatedOffers(state, offers) {
    state.calculatedOffers = offers
  },
  updateCalculatorForm(state, { key, value }) {
    state.calculatorForm[key] = value
  },
}
