import createPersistedState from 'vuex-persistedstate'

export default ({ store }) => {
  createPersistedState({
    paths: ['calculatorForm', 'privacyAccepted', 'tarif'],
  })(store)
}
