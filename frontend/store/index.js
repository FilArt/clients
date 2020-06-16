export const state = () => ({
  calculatedOffers: [],
  calculatorForm: {},
  refreshTokenIds: [],
})

export const mutations = {
  addRefreshTokenId(state, id) {
    state.refreshTokenIds.push(id)
  },
  setCalculatedOffers(state, offers) {
    state.calculatedOffers = offers
  },
  updateCalculatorForm(state, { key, value }) {
    const form = state.calculatorForm
    form[key] = value
    state.calculatorForm = form
  },
}
