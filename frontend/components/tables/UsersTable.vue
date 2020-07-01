<template>
  <v-card>
    <v-card-title>
      <v-text-field
        v-model="search"
        append-icon="mdi-database-search"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table :headers="headers" :items="users" :search="search">
      <template v-slot:item.email="{ item }">
        <nuxt-link
          :to="
            $route.path.endsWith('/')
              ? $route.path + item.id
              : $route.path + '/' + item.id
          "
        >
          {{ item.email }}
        </nuxt-link>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
  name: 'UsersTable',
  props: {
    headers: {
      type: Array,
      default: () => [
        {
          text: 'ID',
          value: 'id',
        },
        {
          text: 'Email',
          value: 'email',
        },
        {
          text: 'Phone',
          value: 'phone',
        },
        {
          text: 'First name',
          value: 'first_name',
        },
        {
          text: 'Last name',
          value: 'last_name',
        },
        {
          text: 'Date joined',
          value: 'date_joined',
        },
        {
          text: 'Bids',
          value: 'bids_count',
        },
        {
          text: 'Cards',
          value: 'cards_count',
        },
      ],
    },
    users: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      search: '',
    }
  },
}
</script>
