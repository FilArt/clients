export default Object.freeze({
  clientRoles: {
    clients: {
      text: 'Clientes',
      value: 'client',
    },
    leeds: {
      text: 'Leeds',
      value: 'leed',
    },
    tramitacion: {
      text: 'Leeds',
      value: 'tramitacion',
    },
  },
  userRoles: {
    admins: {
      text: 'Admins',
      value: 'admin',
    },
    agents: {
      text: 'Agentes',
      value: 'agent',
    },
    affiliates: {
      text: 'Affiliados',
      value: 'affiliate',
    },
    tramitacion: {
      text: 'Tramitacion',
      value: 'support',
    },
  },
  puntoFields: {
    province: {
      text: 'Provincia',
      value: 'province',
      group: {
        text: 'Direccion',
        value: 'direccion',
      },
    },
    locality: {
      text: 'Localidad',
      value: 'locality',
      group: {
        text: 'Direccion',
        value: 'direccion',
      },
    },
    address: {
      text: 'Direccion',
      value: 'address',
      icon: 'mdi-map-marker',
      group: {
        text: 'Direccion',
        value: 'direccion',
      },
    },
    postalcode: {
      text: 'Codigo postal',
      value: 'postalcode',
      group: {
        text: 'Direccion',
        value: 'direccion',
      },
    },
    company_luz: {
      text: 'Comercializadora luz',
      value: 'company_luz',
      onlyAdmin: true,
      group: {
        text: 'Luz',
        value: 'luz',
      },
    },
    cups_luz: {
      text: 'CUPS luz',
      value: 'cups_luz',
      onlyAdmin: true,
      group: {
        text: 'Luz',
        value: 'luz',
      },
    },
    tarif_luz: {
      text: 'Tarif luz',
      value: 'tarif_luz',
      onlyAdmin: true,
      group: {
        text: 'Luz',
        value: 'luz',
      },
    },
    consumo_annual_luz: {
      text: 'Consumo anual luz',
      value: 'consumo_annual_luz',
      onlyAdmin: true,
      group: {
        text: 'Luz',
        value: 'luz',
      },
    },
    last_time_company_luz_changed: {
      text: 'Ultima cambio',
      value: 'last_time_company_luz_changed',
      onlyAdmin: true,
      group: {
        text: 'Luz',
        value: 'luz',
      },
    },
    p1: {
      text: 'P1',
      value: 'p1',
      onlyAdmin: true,
      group: {
        text: 'Luz',
        value: 'luz',
      },
    },
    p2: {
      text: 'P2',
      value: 'p2',
      onlyAdmin: true,
      group: {
        text: 'Luz',
        value: 'luz',
      },
    },
    p3: {
      text: 'P3',
      value: 'p3',
      onlyAdmin: true,
      group: {
        text: 'Luz',
        value: 'luz',
      },
    },
    company_gas: {
      text: 'Comercializadora gas',
      value: 'company_gas',
      onlyAdmin: true,
      group: {
        text: 'Gas',
        value: 'gas',
      },
    },
    cups_gas: {
      text: 'CUPS gas',
      value: 'cups_gas',
      onlyAdmin: true,
      group: {
        text: 'Gas',
        value: 'gas',
      },
    },
    tarif_gas: {
      text: 'Tarif gas',
      value: 'tarif_gas',
      onlyAdmin: true,
      group: {
        text: 'Gas',
        value: 'gas',
      },
    },
    consumo_annual_gas: {
      text: 'Consumo anual gas',
      value: 'consumo_annual_gas',
      onlyAdmin: true,
      group: {
        text: 'Gas',
        value: 'gas',
      },
    },
    last_time_company_gas_changed: {
      text: 'Ultima cambio gas',
      value: 'last_time_company_gas_changed',
      onlyAdmin: true,
      group: {
        text: 'Gas',
        value: 'gas',
      },
    },
    legal_representative: {
      text: 'Representante legal',
      value: 'legal_representative',
      onlyAdmin: true,
      group: {
        text: 'Documentacion',
        value: 'doc',
      },
    },
    dni: {
      text: 'DNI',
      value: 'dni',
      onlyAdmin: true,
      group: {
        text: 'Documentacion',
        value: 'doc',
      },
    },
    cif_dni: {
      text: 'CIF/DNI',
      value: 'cif_dni',
      onlyAdmin: true,
      group: {
        text: 'Documentacion',
        value: 'doc',
      },
    },
    iban: {
      text: 'IBAN',
      value: 'iban',
      icon: 'mdi-bank',
      group: {
        text: 'Documentacion',
        value: 'doc',
      },
    },
  },
  onlyUnique: (value, index, self) => self.indexOf(value) === index,
})
