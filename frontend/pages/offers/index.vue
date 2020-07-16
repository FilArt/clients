<template>
  <v-card>
    <v-card-text class="text-center">
      <div class="text-h4">
        Bienvenido a nuestro catálogo de ofertas
      </div>

      <div class="text-h6">
        Hemos recopilado las ofertas más relevantes del mercado energético, que
        los proveedores de luz más respetados de España tienen actualmente
        disponibles
      </div>
    </v-card-text>

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
                <img src="/hogar.svg" />
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
                <img src="/pyme.svg" />
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
