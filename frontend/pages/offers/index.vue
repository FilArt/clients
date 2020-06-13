<template>
  <v-card>
    <v-card-title>Elegir categoria</v-card-title>
    <v-card-text>
      <v-row align="center">
        <v-col>
          <v-hover v-slot:default="{ hover }">
            <v-card
              max-width="400"
              class="mx-auto"
              outlined
              nuxt
              to="/offers/detail?client_type=0"
              :raised="hover"
            >
              <v-card-text>
                <v-img src="/working-at-home.svg" />
              </v-card-text>
              <v-divider />

              <v-card-text class="text-center display-1">
                HOGAR
              </v-card-text>
            </v-card>
          </v-hover>
        </v-col>
        <v-col>
          <v-hover v-slot:default="{ hover }">
            <v-card
              max-width="400"
              class="mx-auto"
              outlined
              nuxt
              to="/offers/detail?client_type=1"
              :raised="hover"
            >
              <v-card-text>
                <v-img src="/market.svg" />
              </v-card-text>
              <v-divider />

              <v-card-text class="text-center display-1">
                PYME
              </v-card-text>
            </v-card>
          </v-hover>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>
