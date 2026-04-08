const API_BASE_URL = 'http://localhost:8000'; // Ajustar si FastAPI corre en otro puerto

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('item-form');
    const refreshBtn = document.getElementById('refresh-btn');
    const itemsBody = document.getElementById('items-body');
    const emptyState = document.getElementById('empty-state');
    const tableContainer = document.querySelector('.table-container');

    // Inicial carga de datos
    fetchItems();

    // Event Listeners
    form.addEventListener('submit', handleFormSubmit);
    refreshBtn.addEventListener('click', fetchItems);

    async function fetchItems() {
        refreshBtn.classList.add('loading');
        try {
            const response = await fetch(`${API_BASE_URL}/items/`);
            if (!response.ok) throw new Error('Error en la red');
            const items = await response.json();
            renderItems(items);
        } catch (error) {
            console.error('Error fetching items:', error);
            showMessage('Error al conectar con la base de datos', 'error');
        } finally {
            refreshBtn.classList.remove('loading');
        }
    }

    async function handleFormSubmit(e) {
        e.preventDefault();
        
        const nameInput = document.getElementById('name');
        const descInput = document.getElementById('description');
        const priceInput = document.getElementById('price');
        const submitBtn = document.getElementById('submit-btn');
        const spinner = document.getElementById('loading-spinner');
        const btnText = submitBtn.querySelector('span');

        const newItem = {
            name: nameInput.value,
            description: descInput.value || null,
            price: parseFloat(priceInput.value)
        };

        // UI de carga
        btnText.classList.add('hidden');
        spinner.classList.remove('hidden');
        submitBtn.disabled = true;

        try {
            const response = await fetch(`${API_BASE_URL}/items/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newItem)
            });

            if (!response.ok) throw new Error('Error al guardar el objeto');
            
            showMessage('Objeto guardado exitosamente', 'success');
            form.reset();
            fetchItems(); // Recargar la lista

        } catch (error) {
            console.error('Error:', error);
            showMessage(error.message, 'error');
        } finally {
            // Restaurar UI
            btnText.classList.remove('hidden');
            spinner.classList.add('hidden');
            submitBtn.disabled = false;
        }
    }

    async function deleteItem(id) {
        if (!confirm('¿Estás seguro de que deseas eliminar este objeto?')) return;

        try {
            const response = await fetch(`${API_BASE_URL}/items/${id}`, {
                method: 'DELETE'
            });

            if (!response.ok) throw new Error('Error al eliminar');
            
            fetchItems(); // Recargar la lista
            showMessage('Objeto eliminado', 'success');
        } catch (error) {
            console.error('Error:', error);
            showMessage(error.message, 'error');
        }
    }

    function renderItems(items) {
        itemsBody.innerHTML = '';
        
        if (items.length === 0) {
            emptyState.classList.remove('hidden');
            tableContainer.classList.add('hidden');
            return;
        }

        emptyState.classList.add('hidden');
        tableContainer.classList.remove('hidden');

        items.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>#${item.id}</td>
                <td><strong>${item.name}</strong></td>
                <td>${item.description || '<em style="color:var(--text-muted)">Sin desc.</em>'}</td>
                <td>$${item.price.toFixed(2)}</td>
                <td>
                    <button class="btn-danger" onclick="window.deleteItem(${item.id})">Eliminar</button>
                </td>
            `;
            itemsBody.appendChild(tr);
        });
    }

    function showMessage(text, type) {
        const msgDiv = document.getElementById('form-message');
        msgDiv.textContent = text;
        msgDiv.className = `message ${type}`;
        msgDiv.classList.remove('hidden');
        
        setTimeout(() => {
            msgDiv.classList.add('hidden');
        }, 4000);
    }

    // Exponer deleteItem globalmente para los botones generados dinámicamente
    window.deleteItem = deleteItem;
});
