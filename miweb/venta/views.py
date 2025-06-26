from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cliente, Producto
from .forms import ClienteCreateForm, ProductoCreateForm, ClienteUpdateForm

def consulta_cliente(request):
    clientes = Cliente.objects.all().order_by('ape_nombre')
    context = {
        'clientes': clientes,
        'titulo': 'Consulta de Clientes',
        'mensaje': 'Listado completo de clientes'
    }
    return render(request, 'venta/lista_clientes.html', context)

def crear_cliente(request):
    dni_duplicado = False
    
    if request.method == 'POST':
        form = ClienteCreateForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Cliente registrado correctamente')
                return redirect('lista_clientes')
            except Exception as e:
                if 'unique constraint' in str(e).lower():
                    dni_duplicado = True
                    messages.error(request, 'Error: El DNI ya está registrado')
        else:
            if 'id_cliente' in form.errors:
                for error in form.errors['id_cliente']:
                    if 'ya existe' in str(error).lower():
                        dni_duplicado = True
                        form.errors['id_cliente'].clear()
                        break
    
    else:
        form = ClienteCreateForm()

    context = {
        'form': form,
        'titulo': 'Crear Cliente',
        'dni_duplicado': dni_duplicado
    }
    return render(request, 'venta/crear_cliente.html', context)

def consulta_producto(request):
    productos = Producto.objects.all().order_by('nom_prod')
    context = {
        'productos': productos,
        'titulo': 'Consulta de Productos',
        'mensaje': 'Listado completo de productos'
    }
    return render(request, 'venta/lista_producto.html', context)

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('lista_producto')
    else:
        form = ProductoCreateForm()
    return render(request, 'venta/crear_producto.html', {
        'form': form,
        'titulo': 'Crear Producto'
    })


def actualizar_cliente(request):
    cliente = None
    dni_buscado = None
    form = None

    if request.method == 'POST':
        if 'buscar' in request.POST:
            dni_buscado = request.POST.get('dni_busqueda')
            if dni_buscado:
                try:
                    cliente = Cliente.objects.get(id_cliente=dni_buscado)
                    initial_data = {
                        'fec_registro': cliente.fec_registro.strftime('%Y-%m-%d') if cliente.fec_registro else None
                    }
                    form = ClienteUpdateForm(instance=cliente, initial=initial_data)
                    messages.success(request, f'Cliente con DNI: {cliente.id_cliente} encontrado.')
                except Cliente.DoesNotExist:
                    messages.error(request, "Cliente no encontrado.")
        elif 'guardar' in request.POST:
            dni_buscado = request.POST.get('dni_busqueda')
            try:
                cliente = Cliente.objects.get(id_cliente=dni_buscado)
                form = ClienteUpdateForm(request.POST, instance=cliente)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Cliente actualizado correctamente.")
                    return redirect('actualizar_cliente')
            except Cliente.DoesNotExist:
                messages.error(request, "Cliente no encontrado.")

    context = {
        'form': form,
        'cliente': cliente,
        'dni_buscado': dni_buscado,
        'cliente_encontrado': cliente is not None,
        'titulo': 'Actualizar Cliente'
    }
    return render(request, 'venta/u_cliente.html', context)

def borrar_cliente(request):
    clientes_encontrados = []
    tipo_busqueda = 'dni'
    termino_busqueda = ''
    total_registros = 0

    if request.method == 'POST':
        if 'consultar' in request.POST:
            tipo_busqueda = request.POST.get('tipo_busqueda', 'dni')
            termino_busqueda = request.POST.get('termino_busqueda', '').strip()
            if termino_busqueda:
                if tipo_busqueda == 'dni':
                    try:
                        cliente = Cliente.objects.get(id_cliente=termino_busqueda)
                        clientes_encontrados = [cliente]
                    except Cliente.DoesNotExist:
                        messages.error(request, "Cliente no encontrado.")
                elif tipo_busqueda == 'nombre':
                    clientes_encontrados = Cliente.objects.filter(ape_nombre__icontains=termino_busqueda).order_by('id_cliente')
                    if not clientes_encontrados:
                        messages.error(request, "No se encontraron clientes con ese nombre.")
                total_registros = len(clientes_encontrados)
                if total_registros > 0:
                    messages.success(request, f"Se encontraron {total_registros} cliente(s).")
            else:
                messages.error(request, "El campo de búsqueda no puede estar vacío.")
        elif 'eliminar' in request.POST:
            dni_eliminar = request.POST.get('dni_eliminar')
            if dni_eliminar:
                try:
                    cliente = Cliente.objects.get(id_cliente=dni_eliminar)
                    cliente.delete()
                    messages.success(request, f"Cliente con DNI {dni_eliminar} eliminado correctamente.")
                    tipo_busqueda = request.POST.get('tipo_busqueda_actual', 'dni')
                    termino_busqueda = request.POST.get('termino_busqueda_actual', '')
                    if termino_busqueda:
                        if tipo_busqueda == 'dni':
                            try:
                                cliente = Cliente.objects.get(id_cliente=termino_busqueda)
                                clientes_encontrados = [cliente]
                            except Cliente.DoesNotExist:
                                clientes_encontrados = []
                        elif tipo_busqueda == 'nombre':
                            clientes_encontrados = Cliente.objects.filter(ape_nombre__icontains=termino_busqueda).order_by('id_cliente')
                    total_registros = len(clientes_encontrados)
                except Cliente.DoesNotExist:
                    messages.error(request, "Cliente no encontrado.")
            else:
                messages.error(request, "Debe seleccionar un cliente para eliminar.")

    context = {
        'clientes_encontrados': clientes_encontrados,
        'tipo_busqueda': tipo_busqueda,
        'termino_busqueda': termino_busqueda,
        'total_registros': total_registros,
        'titulo': 'Borrar Cliente',
    }
    return render(request, 'venta/borrar_cliente.html', context)

def actualizar_producto(request):
    producto = None
    id_buscado = request.GET.get('id') or request.POST.get('id_busqueda')
    form = None

    if request.method == 'POST' and 'guardar' in request.POST:
        try:
            producto = Producto.objects.get(id_producto=id_buscado)
            form = ProductoCreateForm(request.POST, instance=producto)
            if form.is_valid():
                form.save()
                messages.success(request, "Producto actualizado correctamente.")
                return redirect('lista_producto')  # Redirigir a la lista de productos
        except Producto.DoesNotExist:
            messages.error(request, "Producto no encontrado.")
    
    if id_buscado and (request.method == 'GET' or not form):
        try:
            producto = Producto.objects.get(id_producto=id_buscado)
            initial_data = {
                'fec_vencimiento': producto.fec_vencimiento.strftime('%Y-%m-%d') if producto.fec_vencimiento else None
            }
            form = ProductoCreateForm(instance=producto, initial=initial_data)
        except Producto.DoesNotExist:
            messages.error(request, "Producto no encontrado.")

    context = {
        'form': form,
        'producto': producto,
        'id_buscado': id_buscado,
        'producto_encontrado': producto is not None,
        'titulo': 'Actualizar Producto'
    }
    return render(request, 'venta/actualizar_producto.html', context)

def borrar_producto(request):
    productos_encontrados = []
    tipo_busqueda = 'id'
    termino_busqueda = ''
    total_registros = 0

    if request.method == 'POST':
        if 'consultar' in request.POST:
            tipo_busqueda = request.POST.get('tipo_busqueda', 'id')
            termino_busqueda = request.POST.get('termino_busqueda', '').strip()
            if termino_busqueda:
                if tipo_busqueda == 'id':
                    try:
                        producto = Producto.objects.get(id_producto=termino_busqueda)
                        productos_encontrados = [producto]
                    except Producto.DoesNotExist:
                        messages.error(request, "Producto no encontrado.")
                elif tipo_busqueda == 'nombre':
                    productos_encontrados = Producto.objects.filter(nom_prod__icontains=termino_busqueda).order_by('id_producto')
                    if not productos_encontrados:
                        messages.error(request, "No se encontraron productos con ese nombre.")
                total_registros = len(productos_encontrados)
                if total_registros > 0:
                    messages.success(request, f"Se encontraron {total_registros} producto(s).")
            else:
                messages.error(request, "El campo de búsqueda no puede estar vacío.")
        elif 'eliminar' in request.POST:
            id_eliminar = request.POST.get('id_eliminar')
            if id_eliminar:
                try:
                    producto = Producto.objects.get(id_producto=id_eliminar)
                    producto.delete()
                    messages.success(request, f"Producto con ID {id_eliminar} eliminado correctamente.")
                    productos_encontrados = []
                    total_registros = 0
                except Producto.DoesNotExist:
                    messages.error(request, "Producto no encontrado.")
            else:
                messages.error(request, "Debe seleccionar un producto para eliminar.")
    context = {
        'productos_encontrados': productos_encontrados,
        'tipo_busqueda': tipo_busqueda,
        'termino_busqueda': termino_busqueda,
        'total_registros': total_registros,
        'titulo': 'Borrar Producto',
    }
    return render(request, 'venta/borrar_producto.html', context)

def menu_principal(request):
    return render(request, 'venta/menu.html')