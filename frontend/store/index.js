export const state = () => ({
  calculatedOffers: [],
  calculatorForm: {},
  tarif: null,
  participant: null,
})

export const mutations = {
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
