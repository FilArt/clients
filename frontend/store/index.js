export const state = () => ({
  calculatedOffers: [],
  calculatorForm: {},
  tarif: null,
  puntoHeaders: [],
  puntoCategories: [],
  cities: [],
  privacyAccepted: false,
})

export const mutations = {
  privacyAccepted(state, boolVal) {
    state.privacyAccepted = boolVal
  },
  setCities(state, cities) {
    state.cities = cities
  },
  setPuntoHeaders(state, h) {
    state.puntoHeaders = h
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
