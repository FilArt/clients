<template>
  <beautiful-chat
    v-if="participant"
    :participants="participants"
    :title-image-url="titleImageUrl"
    :on-message-was-sent="onMessageWasSent"
    :message-list="messages"
    :new-messages-count="newMessagesCount"
    :is-open="isChatOpen"
    :close="doCloseChat"
    :open="doOpenChat"
    :colors="$vuetify.theme.isDark ? darkColors : colors"
    :show-file="false"
    :show-launcher="showLauncher || isChatOpen"
    show-emoji
    show-edition
    show-deletion
    show-close-button
    always-scroll-to-bottom
    :show-typing-indicator="showTypingIndicator"
    :message-styling="messageStyling"
    @edit="doEditMessage"
    @remove="doDeleteMessage"
  />
</template>

<script>
import ReconnectingWebSocket from 'reconnecting-websocket'
import { mapState, mapActions, mapGetters } from 'vuex'

export default {
  name: 'Chat',
  props: {
    showLauncher: {
      type: Boolean,
      default: true,
    },
    closeSocketOnExit: {
      type: Boolean,
      default: false,
    },
    isChatOpenDefault: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      chatSocket: null,
      showTypingIndicator: '', // when set to a value matching the participant.id it shows the typing indicator for the specific user
      messageStyling: true, // enables *bold* /emph/ _underline_ and such (more info at github.com/mattezza/msgdown)
      colors: {
        header: {
          bg: '#4e8cff',
          text: '#ffffff',
        },
        launcher: {
          bg: '#4e8cff',
        },
        messageList: {
          bg: '#ffffff',
        },
        sentMessage: {
          bg: '#4e8cff',
          text: '#ffffff',
        },
        receivedMessage: {
          bg: '#eaeaea',
          text: '#222222',
        },
        userInput: {
          bg: '#f4f7f9',
          text: '#565867',
        },
      },
      darkColors: {
        header: {
          bg: '#34495e',
          text: '#ecf0f1',
        },
        launcher: {
          bg: '#34495e',
        },
        messageList: {
          bg: '#2c3e50',
        },
        sentMessage: {
          bg: '#7f8c8d',
          text: '#ecf0f1',
        },
        receivedMessage: {
          bg: '#95a5a6',
          text: '#ecf0f1',
        },
        userInput: {
          bg: '#34495e',
          text: '#ecf0f1',
        },
        userList: {
          bg: '#2c3e50',
          text: '#ecf0f1',
        },
      },
    }
  },
  computed: {
    ...mapState({
      participant: (state) => state.chat.participant,
      isChatOpen: (state) => state.chat.isChatOpen,
      messages: (state) => state.chat.messages,
    }),
    ...mapGetters({
      newMessagesCount: 'chat/newMessagesCount',
      participants: 'chat/participants',
      titleImageUrl: 'chat/titleImageUrl',
    }),
  },
  mounted() {
    if (this.isChatOpenDefault && this.participant) {
      this.doOpenChat()
    } else if (this.participant) {
      this.createSocket()
    }
  },
  beforeDestroy() {
    this.$store.commit('chat/setParticipant', null)
  },
  methods: {
    ...mapActions({
      getMessages: 'chat/getMessages',
      setMessages: 'chat/setMessages',
      addMessage: 'chat/addMessage',
      editMessage: 'chat/editMessage',
      openChat: 'chat/openChat',
      closeChat: 'chat/closeChat',
    }),
    createSocket() {
      const token = this.$auth.strategies.local.token.get().substring(7)
      const ws_scheme = window.location.protocol === 'https:' ? 'wss' : 'ws'
      const chatSocket = new ReconnectingWebSocket(
        `${ws_scheme}://${window.location.host.replace('3000', '8000')}/ws/chat/${
          this.participant.id
        }/?token=${token}`,
      )
      chatSocket.onerror = (e) => {
        this.addMessage({ type: 'text', data: { text: `error: ${e.message}` } })
      }
      chatSocket.onmessage = (m) => {
        const msgData = JSON.parse(m.data)
        switch (msgData.type) {
          case 'edit_message':
            this.editMessage(msgData)
            break
          case 'delete_message':
            this.setMessages(this.messages.filter((m) => m.id !== msgData.message_id))
            break
          case 'text':
            this.addMessage(msgData)
            break
          default:
            break
        }
      }
      this.chatSocket = chatSocket
    },
    doOpenChat() {
      this.openChat()

      if (!this.chatSocket) this.createSocket()

      // fix govna na telefonah
      if (window.innerWidth < 400) {
        setTimeout(function () {
          document.getElementsByClassName('sc-chat-window opened')[0].style.maxHeight = '90%'
        }, 1000)
      }
    },
    doCloseChat() {
      this.closeChat()
      if (this.closeSocketOnExit && this.chatSocket) {
        this.chatSocket.close()
        this.chatSocket = null
      }
      this.$emit('close-chat')
    },
    onMessageWasSent(message) {
      const dataToSend = message.data.text || message.data.emoji
      if (!dataToSend) return
      this.chatSocket.send(JSON.stringify({ message: dataToSend }))
    },
    doEditMessage(message) {
      this.chatSocket.send(JSON.stringify({ type: 'edit_message', message_id: message.id, text: message.data.text }))
    },
    doDeleteMessage(message) {
      this.$swal({
        title: 'Delete message?',
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      }).then((willDelete) => {
        if (willDelete) this.chatSocket.send(JSON.stringify({ type: 'delete_message', message_id: message.id }))
      })
    },
  },
}
</script>
