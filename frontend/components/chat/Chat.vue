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
    :showEmoji="true"
    :showFile="true"
    :showEdition="true"
    :showDeletion="true"
    :showTypingIndicator="showTypingIndicator"
    :showLauncher="true"
    :showCloseButton="true"
    :colors="colors"
    :alwaysScrollToBottom="alwaysScrollToBottom"
    :messageStyling="messageStyling"
    @onType="handleOnType"
    @edit="editMessage"
  />
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
      titleImageUrl:
        'https://a.slack-edge.com/66f9/img/avatars-teams/ava_0001-34.png',
      messageList: [],
      newMessagesCount: 0,
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
      }, // specifies the color scheme for the component
      alwaysScrollToBottom: false, // when set to true always scrolls the chat to the bottom when new events are in (new message, user starts typing...)
      messageStyling: true, // enables *bold* /emph/ _underline_ and such (more info at github.com/mattezza/msgdown)
    }
  },
  async created() {
    await this.getMessages()

    const chatSocket = new ReconnectingWebSocket(
      this.getWssUrl(`/api/chat/${this.participant.id}`)
    )
    chatSocket.onmessage = (m) => {
      const newMessage = JSON.parse(m.data)
      if (newMessage.author.toString() === this.$auth.user.id.toString()) {
        newMessage.author = 'me'
      }
      this.newMessagesCount += 1
      this.messageList = [...this.messageList, newMessage]
    }
    chatSocket.send(
      JSON.stringify({
        type: 'get_messages',
      })
    )
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
      this.newMessagesCount += this.messageList.filter(
        (_m) => _m.author !== 'me' && _m.isRead === false
      ).length
    },
    getWssUrl(aep) {
      const token = this.$auth.strategies.local.token.get().substring(7)
      return window.location.host.includes('3000')
        ? 'ws://'
        : 'wss://' +
            window.location.host.replace('3000', '8000') +
            `/ws/${aep}/?token=${token}`
    },
    onMessageWasSent(message) {
      const text = message.data.text
      if (text.length > 0) {
        this.newMessagesCount = this.isChatOpen
          ? this.newMessagesCount
          : this.newMessagesCount + 1
        this.chatSocket.send(
          JSON.stringify({
            message: text,
          })
        )
      }
    },
    openChat() {
      this.isChatOpen = true
      this.newMessagesCount = 0
      this.messageList
        .filter((m) => m.isRead === false && m.author !== 'me')
        .map((msg) => {
          msg.isRead = true
          this.msgRead(msg.id)
          return msg
        })
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
      m.isEdited = true
      m.data.text = message.data.text
    },
  },
}
</script>
