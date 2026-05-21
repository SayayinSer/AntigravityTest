# Templates de Referencia para el Patrón WorkWith

## 🐍 Backend (FastAPI + SQLModel)
### Lógica de Duplicados en CRUD
```python
def create(self, db: Session, *, obj_in: CreateSchema) -> Model:
    statement = select(Model).where(Model.name == obj_in.name.upper())
    if db.exec(statement).first():
        raise HTTPException(status_code=400, detail="El registro ya existe.")
    return super().create(db, obj_in=obj_in)
```

## ⚛️ Frontend (Next.js + Lucide)
### Estructura de la Tabla Standard
```tsx
<table className="w-full">
  <thead>
    <tr>
      <th>Código</th>
      <th>Descripción</th>
      <th className="text-right">Acciones</th>
    </tr>
  </thead>
  <tbody>
    {paginatedData.map(item => (
      <tr key={item.id} className="hover:bg-slate-50">
        <td>{item.id}</td>
        <td>{item.name}</td>
        <td className="text-right">
           <button onClick={() => edit(item)}><Pencil /></button>
           <button onClick={() => remove(item)}><Trash2 /></button>
        </td>
      </tr>
    ))}
  </tbody>
</table>
```

## 📄 Reporte (jsPDF)
### Generación de Preview
```javascript
const doc = new jsPDF();
doc.text(title, 14, 20);
autoTable(doc, { body: filteredData });
window.open(doc.output("bloburl"), "_blank");
```
