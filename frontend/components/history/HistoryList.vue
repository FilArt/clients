<template>
  <v-timeline>
    <v-timeline-item
      v-for="story in history"
      :key="story.id"
      class="text-left"
      :left="story.user === 'me'"
      :right="story.user !== 'me'"
    >
      <span slot="opposite">
        {{ story.dt }}
        <br />
        {{ story.user.fullname || story.user }}
      </span>
      <v-card class="elevation-2">
        <v-card-title class="headline">
          <span>{{ story.status }}</span>
        </v-card-title>

        <v-card-text v-if="story.message || story.internal_message">
          <p>
            {{ story.message }}
          </p>
          <div v-if="story.internal_message">
            <v-divider />
            <small>Mensaje para agente: </small>
            <p>
              {{ story.internal_message }}
            </p>
          </div>
        </v-card-text>

        <v-card-actions>
          <v-tooltip v-if="story.data" bottom>
            <template v-slot:activator="{ on }">
              <v-btn link target="_blank" :href="story.data.attachment" v-on="on">
                {{ story.data.type_verbose_name }}
                <v-icon right>mdi-open-in-new</v-icon>
              </v-btn>
            </template>
            <span>{{ story.data.description }}</span>
          </v-tooltip>

          <delete-button v-else-if="$auth.user.role === 'admin'" @click="deleteComment(story.id)" />
        </v-card-actions>
      </v-card>
    </v-timeline-item>
  </v-timeline>
</template>
<script>
import DeleteButton from '~/components/buttons/deleteButton'
export default {
  name: 'HistoryList',
  components: { DeleteButton },
  props: {
    history: {
      type: Array,
      default: () => [],
    },
  },
  methods: {
    deleteComment(id) {
      this.$swal({
        title: `Eliminar comentario ${id}?`,
        text: 'Una vez borrado, no podrás recuperar este comentario!',
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      }).then((willDelete) => {
        if (willDelete) {
          this.$axios.$delete(`bids/history/${id}/`).then(() => this.$emit('comment-deleted'))
        }
      })
    },
  },
}
</script>
