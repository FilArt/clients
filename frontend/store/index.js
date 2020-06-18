export const state = () => ({
  calculatedOffers: [],
  calculatorForm: {},
  tarif: null,
})

export const mutations = {
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
