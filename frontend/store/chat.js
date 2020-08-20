export const state = () => ({
  participant: null,
  messages: [],
  isChatOpen: false,
})

export const actions = {
  fetchParticipant({ commit, dispatch }, options) {
    if (options && options.participant) {
      commit('setParticipant', options.participant)
    } else {
      this.$axios.$get('chat/messages/get_participant/').then((p) => {
        commit('setParticipant', p)
      })
    }
    if (options && options.openChat) dispatch('openChat')
  },
  getMessages({ state, rootState, dispatch }) {
    return new Promise((resolve, reject) => {
      const ids = [rootState.auth.user.id, state.participant.id].join()
      this.$axios
        .$get(`chat/messages/?author__in=${ids}&recipient__in=${ids}`)
        .then((messages) => {
          dispatch('setMessages', messages).then(() => resolve())
          resolve()
        })
        .catch((e) => reject(e))
    })
  },
  addMessage({ commit }, message) {
    commit('addMessage', message)
  },
  editMessage({ commit }, message) {
    commit('editMessage', message)
  },
  setMessages({ commit, dispatch }, messages) {
    commit('setMessages', messages)
    dispatch('readMessages')
  },
  readMessages({ state, commit }) {
    return new Promise((resolve, reject) => {
      const readMessagesIds = state.messages.filter((m) => m.author !== 'me' && m.isRead !== true).map((m) => m.id)
      if (readMessagesIds.length && state.isChatOpen) {
        this.$axios
          .$post('chat/messages/messages_read/', { messages_ids: readMessagesIds })
          .then(() => {
            commit('readMessages', readMessagesIds)
            resolve()
          })
          .catch((e) => reject(e))
      } else {
        resolve()
      }
    })
  },
  openChat({ state, commit, dispatch }) {
    if (state.isChatOpen) return
    commit('openChat')
    dispatch('getMessages')
  },
  closeChat({ commit }) {
    commit('closeChat')
  },
}

export const mutations = {
  readMessages(state, messagesIds) {
    const messages = [...state.messages]
    state.messages = messages.map((m) => {
      if (messagesIds.includes(m.id)) {
        m.isRead = true
      }
      return m
    })
  },
  openChat(state) {
    state.isChatOpen = true
  },
  closeChat(state) {
    state.isChatOpen = false
    state.participant = null
  },
  setParticipant(state, p) {
    state.participant = p
  },
  setMessages(state, messages) {
    state.messages = messages
  },
  addMessage(state, message) {
    const messages = [...state.messages]
    messages.push(message)
    state.messages = messages
  },
  editMessage(state, message) {
    state.messages = [...state.messages].map((m) => {
      if (m.id === message.message_id) {
        m.data.text = message.text
        m.isEdited = true
      }
      return m
    })
  },
}

export const getters = {
  newMessagesCount(state) {
    return state.messages.filter((_m) => _m.author !== 'me' && _m.isRead === false).length
  },
  participants(state) {
    return [state.participant]
  },
  titleImageUrl(state) {
    return state.participant.imageUrl || 'null'
  },
}
