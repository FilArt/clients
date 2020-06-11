export const state = () => ({
  calculatedOffers: [],
  calculatorForm: {},
})

export const mutations = {
  setCalculatedOffers(state, offers) {
    state.calculatedOffers = offers
  },
  updateCalculatorForm(state, { key, value }) {
    const form = state.calculatorForm
    form[key] = value
    state.calculatorForm = form
  },
}
