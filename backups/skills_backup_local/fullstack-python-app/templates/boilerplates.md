# Boilerplate HTMX + FastAPI (Integrado)
```text
project/
├── app/
│   ├── main.py        # Rutas y configuración de FastAPI
│   ├── templates/     # Archivos Jinja2 (.html)
│   └── static/        # CSS (Tailwind), JS (Alpine), Assets
└── requirements.txt
```

# Boilerplate React + FastAPI (Desacoplado)
```text
project/
├── backend/           # API REST con FastAPI/Pydantic
│   ├── main.py
│   └── app/
├── frontend/          # Proyecto React + Vite + TS
│   ├── src/
│   ├── index.html
│   └── package.json
└── README.md
```

# Estética Premium (Tailwind Config)
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f9ff',
          500: '#0ea5e9',
          900: '#0c4a6e',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    }
  },
  plugins: [require('@tailwindcss/typography'), require('@tailwindcss/forms')],
}
```
---
*Copia y adapta estas estructuras para arrancar cualquier proyecto Fullstack.*
