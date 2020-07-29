export const state = () => ({
  calculatedOffers: [],
  calculatorForm: {},
  tarif: null,
  participant: null,
  puntoHeaders: [],
  puntoCategories: [],
  cities: [],
})

export const mutations = {
  setCities(state, cities) {
    state.cities = cities
  },
  setPuntoHeaders(state, h) {
    state.puntoHeaders = h
  },
  setPuntoCategories(state, c) {
    state.puntoCategories = c
  },
  setParticipant(state, p) {
    state.participant = p
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
