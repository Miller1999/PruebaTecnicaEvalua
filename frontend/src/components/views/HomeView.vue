<template>
	<div class="container">
		<div v-if="isLoading" class="loader">
			<div class="spinner-border text-primary" role="status">
				<span class="sr-only">Loading...</span>
			</div>
		</div>
		<div v-else>
			<div class="nav">
				<div class="buttons d-flex justify-content-center mb-3">
					<button class="btn btn-success" @click="showModal = true">
						<span>{{ $t("inventory.add") }}</span>
						<i class="bi bi-plus-circle"></i>
					</button>
				</div>
			</div>
			<!-- large screens -->
			<table v-if="isLargeScreen" class="table table-center">
				<thead class="">
					<tr>
						<th scope="col">{{ $t("inventory.name") }}</th>
						<th scope="col">{{ $t("inventory.quantity") }}</th>
						<th scope="col">{{ $t("inventory.price") }}</th>
						<th scope="col">{{ $t("inventory.supplier") }}</th>
						<th scope="col">{{ $t("inventory.action") }}</th>
					</tr>
				</thead>
				<tbody>
					<tr scope="row" v-for="(product, index) in products" :key="index">
						<td>{{ product.name }}</td>
						<td>{{ product.quantity }}</td>
						<td>{{ Math.round(product.price_unit * 100) / 100 }}</td>
						<td>{{ product.supplier }}</td>
						<td class="table-buttons">
							<button
								class="btn btn-primary btn-sm"
								@click="editProduct(product.id_product)"
							>
								<i class="bi bi-pencil"></i>
							</button>
							<button
								class="btn btn-danger btn-sm"
								@click="deleteProduct(product.id_product)"
							>
								<i class="bi bi-trash"></i>
							</button>
						</td>
					</tr>
				</tbody>
			</table>
			<!-- small screens -->
			<section v-else class="row">
				<article v-for="(product, index) in products" :key="index" class="card">
					<div class="card-body"></div>
					<h5 class="card-title">
						{{ $t("inventory.name") }}: {{ product.name }}
					</h5>
					<p class="card-text">
						<strong>{{ $t("inventory.quantity") }}:</strong>
						{{ product.quantity }}
					</p>
					<p class="card-text">
						<span>{{ $t("inventory.price") }}:</span>
						{{ Math.round(product.price_unit * 100) / 100 }}
					</p>
					<p class="card-text">
						<span>{{ $t("inventory.supplier") }}:</span> {{ product.supplier }}
					</p>
					<div class="card__actions">
						<button
							class="btn btn-primary btn-sm"
							@click="editProduct(product.id_product)"
						>
							<i class="bi bi-pencil"></i>
						</button>
						<button
							class="btn btn-danger btn-sm"
							@click="deleteProduct(product.id_product)"
						>
							<i class="bi bi-trash"></i>
						</button>
					</div>
				</article>
			</section>
		</div>

		<ProductCreate
			:isVisible="showModal"
			:isEditing="isEditing"
			:title="formTitle"
			@close="showModal = false"
			@closeEdit="isEditing = false"
			@save="saveProduct"
		>
			<form @submit.prevent="saveProduct">
				<div class="form-group">
					<label for="name">Nombre del producto</label>
					<p v-if="errors.name" class="error">{{ errors.name }}</p>
				</div>
				<input
					id="name"
					type="text"
					class="form-control"
					v-model="newProduct.name"
					placeholder="Nombre del producto"
					@input="clearError('name')"
				/>
				<div class="form-group">
					<label for="quantity">Cantidad</label>
					<p v-if="errors.quantity" class="error">{{ errors.quantity }}</p>
				</div>
				<input
					id="quantity"
					type="number"
					class="form-control"
					v-model="newProduct.quantity"
					placeholder="Cantidad"
					@input="clearError('quantity')"
				/>
				<div class="form-group">
					<label for="price">Precio</label>
					<p v-if="errors.price_unit" class="error">{{ errors.price_unit }}</p>
				</div>
				<input
					id="price"
					type="number"
					class="form-control"
					v-model="newProduct.price_unit"
					placeholder="Precio"
					@input="clearError('price_unit')"
				/>
				<div class="form-group">
					<label for="id_supplier">Proveedor</label>
					<p v-if="errors.id_supplier" class="error">
						{{ errors.id_supplier }}
					</p>
				</div>

				<select
					id="id_supplier"
					class="form-control"
					v-model="newProduct.id_supplier"
				>
					<option value="" disabled selected>Selecciona un proveedor</option>
					<option
						v-for="supplier in suppliers"
						:key="supplier.id_supplier"
						:value="supplier.id_supplier"
					>
						{{ supplier.name }}
					</option>
				</select>

				<button type="submit" class="btn btn-primary mt-3">Añadir</button>
			</form>
		</ProductCreate>
	</div>
</template>

<script>
import VAPI from "@/http_common"; // Importa la configuración de Axios para las peticiones HTTP
import { HTTP_STATUS, SERVICE_NAMES } from "@/app_constants"; // Importa constantes de estado y nombres de servicios
import ProductCreate from "./ProductCreate.vue"; // Importa el componente ProductCreate

export default {
	// Nombre del componente
	name: "HomeView",

	// Componentes hijos utilizados en este componente
	components: {
		ProductCreate,
	},

	data() {
		return {
			// Estado local del componente
			products: [], // Lista de productos
			suppliers: [], // Lista de proveedores
			isLargeScreen: true, // Indica si la pantalla es grande
			isEditing: false, // Indica si se está en modo de edición
			showModal: false, // Indica si el modal debe ser visible
			isLoading: false, // Indica si se está cargando los datos
			// Datos del nuevo producto
			newProduct: {
				name: "", // Nombre del producto
				price_unit: null, // Precio por unidad del producto
				id_supplier: null, // ID del proveedor
				quantity: null, // Cantidad del producto
			},
			errors: {}, // Objeto para almacenar errores de validación
		};
	},
	mounted() {
		// Se ejecuta al montar el componente
		this.getAllSuppliers(); // Obtiene todos los proveedores
		this.getAllProducts(); // Obtiene todos los productos
		this.checkScreenSize(); // Verifica el tamaño de la pantalla
		// Agrega un event listener para verificar el tamaño de la pantalla al redimensionar
		window.addEventListener("resize", this.checkScreenSize);
	},
	computed: {
		// Título del formulario basado en el estado de edición
		formTitle() {
			return this.isEditing
				? this.$t("inventory.edit") // Devuelve "Editar" si está en modo de edición
				: this.$t("inventory.add"); // Devuelve "Agregar" si no está en modo de edición
		},
	},
	methods: {
		// Obtiene todos los productos desde el servidor
		async getAllProducts() {
			this.isLoading = true; // Marca como cargando
			try {
				let response = await VAPI.get(`${SERVICE_NAMES.INVENTORY}/get-all`);
				if (response.status == HTTP_STATUS.OK) {
					this.products = response.data; // Almacena los productos en el estado local
				}
			} catch (error) {
				console.error(error); // Maneja errores de la petición
			} finally {
				this.isLoading = false; // Marca como no cargando
			}
		},
		// Guarda un nuevo producto o actualiza uno existente
		async saveProduct() {
			this.errors = {}; // Resetea los errores
			// Validación de los campos del nuevo producto
			if (!this.newProduct.name) {
				this.errors.name = "El nombre del producto es requerido";
			}
			if (!this.newProduct.quantity || this.newProduct.quantity <= 0) {
				this.errors.quantity = "La cantidad debe ser mayor a 0";
			}
			if (!this.newProduct.price_unit || this.newProduct.price_unit <= 0) {
				this.errors.price_unit = "El precio debe ser mayor a 0";
			}
			if (!this.newProduct.id_supplier) {
				this.errors.id_supplier = "El proveedor es requerido";
			}

			// Si no hay errores, realiza la petición para guardar o actualizar el producto
			if (Object.keys(this.errors).length === 0) {
				try {
					let response;
					if (this.isEditing) {
						// Si se está editando, realiza una petición PUT
						response = await VAPI.put(
							`${SERVICE_NAMES.INVENTORY}/${this.newProduct.id_product}`,
							this.newProduct
						);
					} else {
						// Si se está creando, realiza una petición POST
						response = await VAPI.post(
							`${SERVICE_NAMES.INVENTORY}/`,
							this.newProduct
						);
					}
					if (
						response.status ==
						(this.isEditing ? HTTP_STATUS.OK : HTTP_STATUS.CREATED)
					) {
						this.showModal = false; // Cierra el modal
						// Resetea el objeto newProduct
						this.newProduct = {
							name: "",
							price_unit: null,
							id_supplier: null,
							quantity: null,
						};
						this.isEditing = false; // Resetea el estado de edición
					}
				} catch (error) {
					console.error(error); // Maneja errores de la petición
				}
			}
			await this.getAllProducts(); // Actualiza la lista de productos
		},

		// Abre el modal para editar un producto
		async editProduct(idProduct) {
			this.showModal = true; // Abre el modal
			this.isEditing = true; // Marca como editando
			try {
				let response = await VAPI.get(
					`${SERVICE_NAMES.INVENTORY}/${idProduct}`
				);
				if (response.status == HTTP_STATUS.OK) {
					this.newProduct = {
						...response.data, // Rellena newProduct con los datos del producto
					};
				}
			} catch (error) {
				console.error(error); // Maneja errores de la petición
			}
		},

		// Elimina un producto
		async deleteProduct(idProduct) {
			try {
				let response = await VAPI.delete(
					`${SERVICE_NAMES.INVENTORY}/${idProduct}`
				);
				if (response.status == HTTP_STATUS.NO_CONTENT) {
					await this.getAllProducts(); // Actualiza la lista de productos
				}
			} catch (error) {
				console.error(error); // Maneja errores de la petición
			}
			await this.getAllProducts(); // Asegura que la lista esté actualizada
		},

		// Obtiene todos los proveedores desde el servidor
		async getAllSuppliers() {
			this.isLoading = true; // Marca como cargando
			try {
				let response = await VAPI.get(
					`${SERVICE_NAMES.INVENTORY}/get-all-suppliers`
				);
				if (response.status == HTTP_STATUS.OK) {
					this.suppliers = response.data; // Almacena los proveedores en el estado local
				}
			} catch (error) {
				console.error(error); // Maneja errores de la petición
			} finally {
				this.isLoading = false; // Marca como no cargando
			}
		},

		// Verifica el tamaño de la pantalla
		checkScreenSize() {
			this.isLargeScreen = window.innerWidth > 767; // Establece si la pantalla es grande o pequeña
		},

		// Limpia los errores de un campo específico
		clearError(field) {
			if (this.errors[field]) {
				if (field === "quantity" || field === "price_unit") {
					if (this.newProduct[field] > 0) {
						delete this.errors[field]; // Elimina el error si el valor es válido
					}
				} else if (this.newProduct[field]) {
					delete this.errors[field]; // Elimina el error si el valor es válido
				}
			}
		},
	},
};
</script>

<style lang="scss" scoped>
@import "../../stylessheets/helpers/variables";
.container {
	margin-bottom: 7rem;
	@media (max-width: 767px) {
		margin-top: 100px;
	}
}

.row {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 1rem;
}
.nav {
	justify-content: center;
}
.card {
	width: 90%;
	.card__actions {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 1rem;
		margin: 1rem 0;
	}
}
.table-buttons {
	button:last-child {
		margin-left: 1rem;
	}
}
.error {
	color: red;
}
.buttons {
	position: fixed;
	z-index: 10;
	bottom: 0;
	left: 0;
	right: 0;
	display: flex;
	justify-content: center;
	align-items: center;
	gap: 1rem;
	padding: 1rem;
	button {
		display: flex;
		justify-content: center;
		align-items: center;
		border-radius: 50%;
		width: 50px;
		height: 50px;
		border: 1px solid transparent;
		i {
			font-size: 1.5rem;
		}
	}
	span {
		display: none;
	}
	@media (min-width: 767px) {
		position: inherit;
		button {
			width: 200px;
			border-radius: 10px;
		}
		span {
			display: block;
		}
		i {
			display: none;
		}
	}
}
.form-group {
	margin-bottom: 1rem;
	text-align: left;
	label {
		font-weight: bold;
	}
}
input {
	margin-bottom: 1rem;
}
.loader {
	display: flex;
	justify-content: center;
	align-items: center;
	height: 100vh;
}
</style>
