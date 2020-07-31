<template>
  <beautiful-chat
    v-if="chatSocket"
    :participants="participants"
    :titleImageUrl="titleImageUrl"
    :onMessageWasSent="onMessageWasSent"
    :messageList="messageList"
    :newMessagesCount="newMessagesCount"
    :isOpen="isChatOpen"
    :close="closeChat"
    :icons="icons"
    :open="openChat"
    showEmoji
    showFile
    showEdition
    showDeletion
    showLauncher
    showCloseButton
    alwaysScrollToBottom
    :showTypingIndicator="showTypingIndicator"
    :colors="colors"
    :messageStyling="messageStyling"
    @onType="handleOnType"
    @edit="editMessage"
    @remove="deleteMessage"
  >
  </beautiful-chat>
</template>

<script>
import CloseIcon from 'vue-beautiful-chat/src/assets/close-icon.png'
import OpenIcon from 'vue-beautiful-chat/src/assets/logo-no-bg.svg'
import FileIcon from 'vue-beautiful-chat/src/assets/file.svg'
import CloseIconSvg from 'vue-beautiful-chat/src/assets/close.svg'
import ReconnectingWebSocket from 'reconnecting-websocket'
export default {
  name: 'Chat',
  props: {
    participant: {
      type: Object,
      default: () => {},
    },
  },
  data() {
    return {
      chatSocket: null,
      icons: {
        open: {
          img: OpenIcon,
          name: 'default',
        },
        close: {
          img: CloseIcon,
          name: 'default',
        },
        file: {
          img: FileIcon,
          name: 'default',
        },
        closeSvg: {
          img: CloseIconSvg,
          name: 'default',
        },
      },
      participants: [this.participant],
      titleImageUrl: this.participant.imageUrl || 'null',
      messageList: [],
      isChatOpen: false, // to determine whether the chat window should be open or closed
      showTypingIndicator: '', // when set to a value matching the participant.id it shows the typing indicator for the specific user
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
      messageStyling: true, // enables *bold* /emph/ _underline_ and such (more info at github.com/mattezza/msgdown)
    }
  },
  computed: {
    newMessagesCount() {
      return this.messageList.filter(
        (_m) => _m.author !== 'me' && _m.isRead === false
      ).length
    },
  },
  async created() {
    await this.getMessages()

    const chatSocket = new ReconnectingWebSocket(
      this.getWssUrl(`chat/${this.participant.id}`)
    )
    chatSocket.onmessage = (m) => {
      const newMessage = JSON.parse(m.data)
      if (newMessage.author.toString() === this.$auth.user.id.toString()) {
        newMessage.author = 'me'
      }
      this.messageList = [...this.messageList, newMessage]
    }
    this.chatSocket = chatSocket
  },
  methods: {
    async getMessages() {
      const ids = [this.$auth.user.id, this.participant.id].join()
      const params = { author__in: ids, recipient__in: ids }
      const messages = await this.$axios.$get('chat/messages/', {
        params: params,
      })
      this.messageList = messages.map((m) => {
        return {
          id: m.id,
          type: 'text',
          isRead: m.is_read,
          author:
            m.author.toString() === this.$auth.user.id.toString()
              ? 'me'
              : m.author,
          data: { text: m.text, meta: m.created },
        }
      })
    },
    getWssUrl(aep) {
      const token = this.$auth.strategies.local.token.get().substring(7)
      const ws_scheme = window.location.protocol === 'https:' ? 'wss' : 'ws'
      return (
        ws_scheme +
        '://' +
        window.location.host.replace('3000', '8000') +
        `/ws/${aep}/?token=${token}`
      )
    },
    onMessageWasSent(message) {
      const text = message.data.text
      if (text.length > 0) {
        this.chatSocket.send(
          JSON.stringify({
            message: text,
          })
        )
      }
    },
    openChat() {
      this.isChatOpen = true
      this.messageList
        .filter((m) => m.isRead === false && m.author !== 'me')
        .map((msg) => {
          msg.isRead = true
          this.msgRead(msg.id)
          return msg
        })
      if (window.innerWidth < 400) {
        setTimeout(function () {
          document.getElementsByClassName(
            'sc-chat-window opened'
          )[0].style.maxHeight = '90%'
        }, 1000)
      }
    },
    async msgRead(msgId) {
      await this.$axios.$patch('chat/messages/' + msgId + '/message_read/')
    },
    closeChat() {
      this.isChatOpen = false
    },
    handleScrollToTop() {
      // called when the user scrolls message list to top
      // leverage pagination for loading another page of messages
      console.log('scroll on top')
    },
    handleOnType() {
      console.log('Emit typing event')
    },
    editMessage(message) {
      const m = this.messageList.find((m) => m.id === message.id)
      const text = message.data.text
      m.isEdited = true
      this.$axios
        .$patch(`chat/messages/${message.id}/`, { text: text })
        .then(() => {
          m.data.text = text
        })
    },
    deleteMessage(message) {
      this.$swal({
        title: 'Delete message?',
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      }).then((willDelete) => {
        if (willDelete) {
          this.$axios.$delete(`chat/messages/${message.id}/`)
          this.messageList = this.messageList.filter((m) => m.id !== message.id)
        }
      })
    },
  },
}
</script>
