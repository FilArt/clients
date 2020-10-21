<template>
  <v-card flat :loading="loading">
    <v-snackbar v-model="actionsSnackbar" :timeout="-1" :value="true" color="deep-purple accent-4" elevation="24">
      <v-row align="center">
        <v-col class="flex-grow-1">Acciones</v-col>
        <v-col class="flex-grow-0">
          <close-button @click="actionsSnackbar = false" />
        </v-col>
      </v-row>

      <v-divider />

      <v-row>
        <v-col>
          <delete-button @click="deleteItems" />
        </v-col>
      </v-row>
    </v-snackbar>

    <v-toolbar>
      <v-toolbar-title>Info</v-toolbar-title>
    </v-toolbar>

    <v-card-text>
      <v-sheet>
        <v-data-table
          :headers="headers"
          :items="items"
          :show-select="$auth.user.role === 'admin'"
          @item-selected="onSelect"
          @toggle-select-all="onToggleSelect"
        >
          <template v-slot:[`item.url`]="{ item }">
            <v-btn small outlined :href="item.url" target="_blank">
              {{ item.url }}
            </v-btn>
          </template>

          <template v-slot:[`item.users`]="{ item }">
            <v-chip v-for="user in item.users" :key="user.id" small>
              {{ $store.state.responsibles.find((r) => r.id === user).fullname }}
            </v-chip>
          </template>
        </v-data-table>
      </v-sheet>
    </v-card-text>

    <v-divider />

    <v-form v-if="$auth.user.role === 'admin'" style="max-width: 750px" class="mx-auto" @submit.prevent="submit">
      <v-card-text>
        <v-text-field v-model="newInfo.title" label="Nombre" :error-messages="errorMessages.title" />
        <v-text-field v-model="newInfo.url" label="URL" :error-messages="errorMessages.url" />
        <agents-list v-model="newInfo.users" multiple :error-messages="errorMessages.users" />
      </v-card-text>

      <v-card-actions>
        <submit-button block label="Añadir nuevo" />
      </v-card-actions>
    </v-form>
  </v-card>
</template>

<script>
import AgentsList from '@/components/selects/AgentsList'
import SubmitButton from '@/components/buttons/submitButton'
import DeleteButton from '@/components/buttons/deleteButton'
import CloseButton from '@/components/buttons/closeButton'
export default {
  components: { CloseButton, DeleteButton, SubmitButton, AgentsList },
  async asyncData({ $axios, $auth }) {
    const items = await $axios.$get('info')
    const headers = [
      {
        text: 'Nombre',
        value: 'title',
      },
      {
        text: 'URL',
        value: 'url',
      },
    ]
    if ($auth.user.role === 'admin') {
      headers.push({
        text: 'Usuarios',
        value: 'users',
      })
    }
    return { items, headers }
  },
  data() {
    return {
      editDialog: false,
      deleteRowsDialog: false,
      actionsSnackbar: false,
      selectedRows: [],
      loading: false,
      newInfo: {
        title: '',
        url: '',
        users: [],
      },
      errorMessages: { name: null, url: null, users: null },
    }
  },
  methods: {
    async deleteItems() {
      const willDelete = await this.$swal({
        title: 'Eliminar?',
        text: this.selectedRows.map((i) => i.id).join(', '),
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      })
      if (!willDelete) return
      for await (const row of this.selectedRows) {
        await this.$axios.$delete(`info/${row.id}/`)
      }
      this.selectedRows = []
      this.actionsSnackbar = this.selectedRows.length > 0
      await this.refresh()
    },
    onToggleSelect({ items, value }) {
      this.selectedRows = value ? items : []
      this.actionsSnackbar = this.selectedRows.length > 0
    },
    onSelect({ item, value }) {
      if (value) {
        this.selectedRows.push(item)
      } else {
        this.selectedRows = this.selectedRows.filter((r) => r.id !== item.id)
      }
      this.actionsSnackbar = this.selectedRows.length > 0
    },
    async refresh() {
      this.loading = true
      this.items = await this.$axios.$get('info')
      this.loading = false
    },
    async submit() {
      this.loading = true
      try {
        await this.$axios.$post('info/', this.newInfo)
        await this.refresh()
      } catch (e) {
        this.errorMessages = e?.response?.data || {}
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
