export const state = () => ({
  calculatedOffers: [],
  calculatorForm: {
    kind: 'luz',
    igic: false,
    client_type: 1,
  },
  puntoCategories: [],
  cities: [],
  privacyAccepted: false,
  companies: [],
  responsibles: [],
  bidToChange: null,
  cvusers: [],
})

export const actions = {
  async fetchCvUsers({ commit }) {
    const url =
      (process.env.NODE_ENV === 'development' ? 'http://localhost:8000' : 'https://call-visit.gestiongroup.es') +
      '/api/users/'
    commit('setCvUsers', await this.$axios.$post('cv_integration/x', { url }))
  },
  async fetchResponsibles({ commit }, isAgent) {
    const users = (
      await this.$axios.$get(
        `users/${isAgent ? 'canal_agents' : 'users'}/?role=agent&fields=id,fullname&itemsPerPage=100`,
      )
    ).results
    commit('setResponsibles', users)
  },
  async fetchCompanies({ commit }) {
    const companies = await this.$axios.$get('/calculator/companies/')
    commit('setCompanies', companies)
  },
  async fetchProvinces({ commit }) {
    const provinces = await this.$axios.$get('/users/puntos/get_cities/')
    commit('setCities', provinces)
  },
  setCalculatorForm({ commit }, form) {
    commit('setCalculatorForm', form)
  },
}

export const mutations = {
  setCvUsers(state, cvusers) {
    state.cvusers = cvusers
  },
  resetCalculator(state) {
    state.calculatorForm = { client_type: 1, kind: 'luz', igic: false }
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
  setCalculatorForm(state, form) {
    state.calculatorForm = form
  },
}
