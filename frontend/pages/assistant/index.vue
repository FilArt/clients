<template>
  <v-card>
    <v-row align="center">
      <v-col class="text-center">
        <v-avatar height="300" width="300">
          <v-img src="market.svg" />
        </v-avatar>
      </v-col>

      <v-col>
        <v-card-title>My personal histor energetica</v-card-title>
        <v-card-title>Isai Secaduras</v-card-title>
        <v-row>
          <v-col>
            <v-btn>
              <v-icon left>
                mdi-phone
              </v-icon>
              611-111-33
            </v-btn>
          </v-col>
          <v-col>
            <v-btn>
              <v-icon left>
                mdi-email
              </v-icon>
              isai@mail.com
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
export default {
  name: 'index',
}
</script>
