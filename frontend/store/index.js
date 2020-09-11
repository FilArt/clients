export const state = () => ({
  calculatedOffers: [],
  calculatorForm: {},
  tarif: null,
  puntoCategories: [],
  cities: [],
  privacyAccepted: false,
  companies: [],
})

export const mutations = {
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
